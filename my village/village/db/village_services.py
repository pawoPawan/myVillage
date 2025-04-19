"""
Village Services module for database operations.

This module provides functionality for interacting with service-related models.
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from .base import BaseDB
from ..models import VillageService, UserProfile

class VillageServicesDB(BaseDB):
    """
    Class for interacting with service-related models.
    """
    
    @classmethod
    def get_service_by_id(cls, service_id: int) -> Optional[VillageService]:
        """
        Get a service by its ID.
        
        Args:
            service_id: The ID of the service to retrieve.
            
        Returns:
            The service if found, None otherwise.
        """
        return cls.get_by_id(VillageService, service_id)
    
    @classmethod
    def get_services_by_village(cls, village_id: int) -> List[VillageService]:
        """
        Get all services in a village.
        
        Args:
            village_id: The ID of the village.
            
        Returns:
            A list of services in the village.
        """
        return cls.filter(VillageService, village_id=village_id)
    
    @classmethod
    def get_services_by_category(cls, category: str, village_id: int = None) -> List[VillageService]:
        """
        Get all services of a specific category.
        
        Args:
            category: The category of service to retrieve.
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of services of the specified category.
        """
        if village_id:
            return cls.filter(VillageService, category=category, village_id=village_id)
        else:
            return cls.filter(VillageService, category=category)
    
    @classmethod
    def create_service(cls, name: str, description: str, category: str,
                      village_id: int, contact_person_id: int, **kwargs) -> VillageService:
        """
        Create a new service.
        
        Args:
            name: The name of the service.
            description: The description of the service.
            category: The category of the service.
            village_id: The ID of the village.
            contact_person_id: The ID of the user profile for the contact person.
            **kwargs: Additional service attributes.
            
        Returns:
            The created service.
        """
        from .user_management import UserManagementDB
        from .location_hierarchy import LocationHierarchyDB
        
        village = LocationHierarchyDB.get_village_by_id(village_id)
        if not village:
            raise ValueError(f"Village with ID {village_id} not found.")
        
        contact_person = cls.get_by_id(UserProfile, contact_person_id)
        if not contact_person:
            raise ValueError(f"User profile with ID {contact_person_id} not found.")
        
        return cls.create(
            VillageService,
            name=name,
            description=description,
            category=category,
            village=village,
            contact_person=contact_person,
            **kwargs
        )
    
    @classmethod
    def update_service(cls, service: VillageService, **kwargs) -> VillageService:
        """
        Update a service.
        
        Args:
            service: The service to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated service.
        """
        return cls.update(service, **kwargs)
    
    @classmethod
    def delete_service(cls, service: VillageService) -> bool:
        """
        Delete a service.
        
        Args:
            service: The service to delete.
            
        Returns:
            True if the service was deleted, False otherwise.
        """
        return cls.delete(service)
    
    @classmethod
    def get_services_by_contact_person(cls, contact_person_id: int) -> List[VillageService]:
        """
        Get all services managed by a contact person.
        
        Args:
            contact_person_id: The ID of the user profile.
            
        Returns:
            A list of services managed by the contact person.
        """
        return cls.filter(VillageService, contact_person_id=contact_person_id)
    
    @classmethod
    def search_services(cls, query: str, village_id: int = None) -> List[VillageService]:
        """
        Search for services by the given query.
        
        Args:
            query: The search query.
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of services matching the query.
        """
        fields = ['name', 'description', 'category', 'contact_person__user__username', 'notes']
        services = cls.search(VillageService, query, fields)
        
        if village_id:
            return [service for service in services if service.village_id == village_id]
        
        return services 