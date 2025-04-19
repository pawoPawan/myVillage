"""
Base module for database operations.

This module provides common functionality for all database modules.
"""

from django.db import models
from django.db.models import Q
from typing import List, Dict, Any, Optional, Union, Type, TypeVar

T = TypeVar('T', bound=models.Model)

class BaseDB:
    """
    Base class for all database modules.
    
    This class provides common functionality for interacting with Django models.
    """
    
    @staticmethod
    def get_by_id(model_class: Type[T], id: int) -> Optional[T]:
        """
        Get a model instance by its ID.
        
        Args:
            model_class: The model class to query.
            id: The ID of the model instance to retrieve.
            
        Returns:
            The model instance if found, None otherwise.
        """
        try:
            return model_class.objects.get(id=id)
        except model_class.DoesNotExist:
            return None
    
    @staticmethod
    def get_all(model_class: Type[T]) -> List[T]:
        """
        Get all instances of a model.
        
        Args:
            model_class: The model class to query.
            
        Returns:
            A list of all model instances.
        """
        return list(model_class.objects.all())
    
    @staticmethod
    def filter(model_class: Type[T], **kwargs) -> List[T]:
        """
        Filter model instances by the given criteria.
        
        Args:
            model_class: The model class to query.
            **kwargs: Filter criteria.
            
        Returns:
            A list of model instances matching the criteria.
        """
        return list(model_class.objects.filter(**kwargs))
    
    @staticmethod
    def create(model_class: Type[T], **kwargs) -> T:
        """
        Create a new model instance.
        
        Args:
            model_class: The model class to create.
            **kwargs: Model attributes.
            
        Returns:
            The created model instance.
        """
        return model_class.objects.create(**kwargs)
    
    @staticmethod
    def update(instance: T, **kwargs) -> T:
        """
        Update a model instance.
        
        Args:
            instance: The model instance to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated model instance.
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    @staticmethod
    def delete(instance: T) -> bool:
        """
        Delete a model instance.
        
        Args:
            instance: The model instance to delete.
            
        Returns:
            True if the instance was deleted, False otherwise.
        """
        try:
            instance.delete()
            return True
        except Exception:
            return False
    
    @staticmethod
    def search(model_class: Type[T], query: str, fields: List[str]) -> List[T]:
        """
        Search for model instances by the given query in the specified fields.
        
        Args:
            model_class: The model class to query.
            query: The search query.
            fields: The fields to search in.
            
        Returns:
            A list of model instances matching the query.
        """
        if not query:
            return []
        
        q_objects = Q()
        for field in fields:
            q_objects |= Q(**{f"{field}__icontains": query})
        
        return list(model_class.objects.filter(q_objects))
    
    @staticmethod
    def count(model_class: Type[T], **kwargs) -> int:
        """
        Count model instances by the given criteria.
        
        Args:
            model_class: The model class to query.
            **kwargs: Filter criteria.
            
        Returns:
            The number of model instances matching the criteria.
        """
        return model_class.objects.filter(**kwargs).count()
    
    @staticmethod
    def exists(model_class: Type[T], **kwargs) -> bool:
        """
        Check if any model instances match the given criteria.
        
        Args:
            model_class: The model class to query.
            **kwargs: Filter criteria.
            
        Returns:
            True if any model instances match the criteria, False otherwise.
        """
        return model_class.objects.filter(**kwargs).exists() 