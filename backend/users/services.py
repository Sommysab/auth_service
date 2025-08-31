from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from typing import Optional, Tuple

User = get_user_model()


class UserService:
    """Service class to handle User-related operations that are actually used"""
    
    @staticmethod
    def create_user(email: str, password: str, full_name: str = '') -> User:
        """Create a new user - used in RegisterSerializer"""
        return User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name
        )
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email - used in PasswordResetService"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID - used in PasswordResetService"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def update_user_password(user: User, new_password: str) -> User:
        """Update user password - used in PasswordResetService"""
        user.set_password(new_password)
        user.save()
        return user


class PasswordResetService:
    """Service class to handle password reset operations that are actually used"""
    
    CACHE_PREFIX = 'pwdreset:'
    TOKEN_LENGTH = 32
    TOKEN_TIMEOUT = 10 * 60  # 10 minutes
    
    @staticmethod
    def generate_reset_token() -> str:
        """Generate a random reset token - used in process_password_reset_request"""
        return get_random_string(PasswordResetService.TOKEN_LENGTH)
    
    @staticmethod
    def store_reset_token(token: str, user_id: int) -> None:
        """Store reset token in cache - used in process_password_reset_request"""
        cache_key = f"{PasswordResetService.CACHE_PREFIX}{token}"
        cache.set(cache_key, user_id, timeout=PasswordResetService.TOKEN_TIMEOUT)
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[int]:
        """Get user ID from reset token - used in process_password_reset"""
        cache_key = f"{PasswordResetService.CACHE_PREFIX}{token}"
        return cache.get(cache_key)
    
    @staticmethod
    def invalidate_reset_token(token: str) -> None:
        """Remove reset token from cache - used in process_password_reset"""
        cache_key = f"{PasswordResetService.CACHE_PREFIX}{token}"
        cache.delete(cache_key)
    
    @staticmethod
    def process_password_reset_request(email: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Process password reset request - used in forgot_password view
        Returns: (success, error_message, token)
        """
        user = UserService.get_user_by_email(email)
        if not user:
            return False, "User not found", None
        
        token = PasswordResetService.generate_reset_token()
        PasswordResetService.store_reset_token(token, user.id)
        
        return True, None, token
    
    @staticmethod
    def process_password_reset(token: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Process password reset with token - used in reset_password view
        Returns: (success, error_message)
        """
        user_id = PasswordResetService.get_user_id_from_token(token)
        if not user_id:
            return False, "Invalid or expired token"
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False, "Invalid token"
        
        UserService.update_user_password(user, new_password)
        PasswordResetService.invalidate_reset_token(token)
        
        return True, None

