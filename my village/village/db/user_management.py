"""
User Management module for database operations.

This module provides functionality for interacting with user-related models.
"""

from django.contrib.auth.models import User
from django.db.models import Q
from typing import List, Dict, Any, Optional, Union, Tuple
from .base import BaseDB
from ..models import UserProfile

class UserManagementDB(BaseDB):
    """
    Class for interacting with user-related models.
    """
    
    @classmethod
    def get_user_by_id(cls, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve.
            
        Returns:
            The user if found, None otherwise.
        """
        return cls.get_by_id(User, user_id)
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[User]:
        """
        Get a user by their username.
        
        Args:
            username: The username of the user to retrieve.
            
        Returns:
            The user if found, None otherwise.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[User]:
        """
        Get a user by their email.
        
        Args:
            email: The email of the user to retrieve.
            
        Returns:
            The user if found, None otherwise.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, 
                   first_name: str = "", last_name: str = "") -> User:
        """
        Create a new user.
        
        Args:
            username: The username for the new user.
            email: The email for the new user.
            password: The password for the new user.
            first_name: The first name for the new user.
            last_name: The last name for the new user.
            
        Returns:
            The created user.
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user
    
    @classmethod
    def update_user(cls, user: User, **kwargs) -> User:
        """
        Update a user.
        
        Args:
            user: The user to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated user.
        """
        return cls.update(user, **kwargs)
    
    @classmethod
    def delete_user(cls, user: User) -> bool:
        """
        Delete a user.
        
        Args:
            user: The user to delete.
            
        Returns:
            True if the user was deleted, False otherwise.
        """
        return cls.delete(user)
    
    @classmethod
    def get_user_profile(cls, user: User) -> Optional[UserProfile]:
        """
        Get a user's profile.
        
        Args:
            user: The user whose profile to retrieve.
            
        Returns:
            The user's profile if found, None otherwise.
        """
        try:
            return user.userprofile
        except UserProfile.DoesNotExist:
            return None
    
    @classmethod
    def create_user_profile(cls, user: User, **kwargs) -> UserProfile:
        """
        Create a new user profile.
        
        Args:
            user: The user to create a profile for.
            **kwargs: Profile attributes.
            
        Returns:
            The created user profile.
        """
        return UserProfile.objects.create(user=user, **kwargs)
    
    @classmethod
    def update_user_profile(cls, profile: UserProfile, **kwargs) -> UserProfile:
        """
        Update a user profile.
        
        Args:
            profile: The profile to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated user profile.
        """
        return cls.update(profile, **kwargs)
    
    @classmethod
    def delete_user_profile(cls, profile: UserProfile) -> bool:
        """
        Delete a user profile.
        
        Args:
            profile: The profile to delete.
            
        Returns:
            True if the profile was deleted, False otherwise.
        """
        return cls.delete(profile)
    
    @classmethod
    def get_users_by_village(cls, village_id: int) -> List[User]:
        """
        Get all users in a village.
        
        Args:
            village_id: The ID of the village.
            
        Returns:
            A list of users in the village.
        """
        return User.objects.filter(userprofile__village_id=village_id)
    
    @classmethod
    def get_verified_users(cls) -> List[User]:
        """
        Get all users with verified Aadhaar.
        
        Returns:
            A list of users with verified Aadhaar.
        """
        return User.objects.filter(userprofile__aadhaar_verified=True)
    
    @classmethod
    def search_users(cls, query: str) -> List[User]:
        """
        Search for users by the given query.
        
        Args:
            query: The search query.
            
        Returns:
            A list of users matching the query.
        """
        if not query:
            return []
        
        q_objects = Q(username__icontains=query) | Q(email__icontains=query) | \
                   Q(first_name__icontains=query) | Q(last_name__icontains=query)
        
        return list(User.objects.filter(q_objects))
    
    @classmethod
    def search_user_profiles(cls, query: str) -> List[UserProfile]:
        """
        Search for user profiles by the given query.
        
        Args:
            query: The search query.
            
        Returns:
            A list of user profiles matching the query.
        """
        fields = ['education', 'profession', 'hobbies', 'achievements', 
                 'social_contributions', 'father_name', 'mother_name', 'nickname']
        return cls.search(UserProfile, query, fields)
    
    @classmethod
    def get_user_with_profile(cls, user_id: int) -> Tuple[Optional[User], Optional[UserProfile]]:
        """
        Get a user and their profile by the user's ID.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            A tuple containing the user and their profile, or (None, None) if not found.
        """
        user = cls.get_user_by_id(user_id)
        if not user:
            return None, None
        
        profile = cls.get_user_profile(user)
        return user, profile 