"""
Community Events module for database operations.

This module provides functionality for interacting with event-related models.
"""

from django.utils import timezone
from typing import List, Dict, Any, Optional, Union, Tuple
from .base import BaseDB
from ..models import CommunityEvent, EventContribution, UserProfile

class CommunityEventsDB(BaseDB):
    """
    Class for interacting with event-related models.
    """
    
    @classmethod
    def get_event_by_id(cls, event_id: int) -> Optional[CommunityEvent]:
        """
        Get an event by its ID.
        
        Args:
            event_id: The ID of the event to retrieve.
            
        Returns:
            The event if found, None otherwise.
        """
        return cls.get_by_id(CommunityEvent, event_id)
    
    @classmethod
    def get_events_by_village(cls, village_id: int) -> List[CommunityEvent]:
        """
        Get all events in a village.
        
        Args:
            village_id: The ID of the village.
            
        Returns:
            A list of events in the village.
        """
        return cls.filter(CommunityEvent, village_id=village_id)
    
    @classmethod
    def get_upcoming_events(cls, village_id: int = None) -> List[CommunityEvent]:
        """
        Get all upcoming events.
        
        Args:
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of upcoming events.
        """
        now = timezone.now()
        if village_id:
            return list(CommunityEvent.objects.filter(
                village_id=village_id,
                start_date__gte=now
            ).order_by('start_date'))
        else:
            return list(CommunityEvent.objects.filter(
                start_date__gte=now
            ).order_by('start_date'))
    
    @classmethod
    def get_past_events(cls, village_id: int = None) -> List[CommunityEvent]:
        """
        Get all past events.
        
        Args:
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of past events.
        """
        now = timezone.now()
        if village_id:
            return list(CommunityEvent.objects.filter(
                village_id=village_id,
                end_date__lt=now
            ).order_by('-end_date'))
        else:
            return list(CommunityEvent.objects.filter(
                end_date__lt=now
            ).order_by('-end_date'))
    
    @classmethod
    def get_events_by_type(cls, event_type: str, village_id: int = None) -> List[CommunityEvent]:
        """
        Get all events of a specific type.
        
        Args:
            event_type: The type of event to retrieve.
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of events of the specified type.
        """
        if village_id:
            return cls.filter(CommunityEvent, event_type=event_type, village_id=village_id)
        else:
            return cls.filter(CommunityEvent, event_type=event_type)
    
    @classmethod
    def create_event(cls, title: str, description: str, event_type: str, 
                    start_date: timezone.datetime, end_date: timezone.datetime,
                    village_id: int, created_by_id: int, **kwargs) -> CommunityEvent:
        """
        Create a new event.
        
        Args:
            title: The title of the event.
            description: The description of the event.
            event_type: The type of event.
            start_date: The start date of the event.
            end_date: The end date of the event.
            village_id: The ID of the village.
            created_by_id: The ID of the user creating the event.
            **kwargs: Additional event attributes.
            
        Returns:
            The created event.
        """
        from .user_management import UserManagementDB
        from .location_hierarchy import LocationHierarchyDB
        
        village = LocationHierarchyDB.get_village_by_id(village_id)
        if not village:
            raise ValueError(f"Village with ID {village_id} not found.")
        
        user_profile = UserManagementDB.get_user_profile(
            UserManagementDB.get_user_by_id(created_by_id)
        )
        if not user_profile:
            raise ValueError(f"User profile for user with ID {created_by_id} not found.")
        
        return cls.create(
            CommunityEvent,
            title=title,
            description=description,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            village=village,
            created_by=user_profile,
            **kwargs
        )
    
    @classmethod
    def update_event(cls, event: CommunityEvent, **kwargs) -> CommunityEvent:
        """
        Update an event.
        
        Args:
            event: The event to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated event.
        """
        return cls.update(event, **kwargs)
    
    @classmethod
    def delete_event(cls, event: CommunityEvent) -> bool:
        """
        Delete an event.
        
        Args:
            event: The event to delete.
            
        Returns:
            True if the event was deleted, False otherwise.
        """
        return cls.delete(event)
    
    @classmethod
    def get_contribution_by_id(cls, contribution_id: int) -> Optional[EventContribution]:
        """
        Get a contribution by its ID.
        
        Args:
            contribution_id: The ID of the contribution to retrieve.
            
        Returns:
            The contribution if found, None otherwise.
        """
        return cls.get_by_id(EventContribution, contribution_id)
    
    @classmethod
    def get_contributions_by_event(cls, event_id: int) -> List[EventContribution]:
        """
        Get all contributions for an event.
        
        Args:
            event_id: The ID of the event.
            
        Returns:
            A list of contributions for the event.
        """
        return cls.filter(EventContribution, event_id=event_id)
    
    @classmethod
    def get_contributions_by_user(cls, user_profile_id: int) -> List[EventContribution]:
        """
        Get all contributions by a user.
        
        Args:
            user_profile_id: The ID of the user profile.
            
        Returns:
            A list of contributions by the user.
        """
        return cls.filter(EventContribution, contributor_id=user_profile_id)
    
    @classmethod
    def create_contribution(cls, event_id: int, contributor_id: int, 
                          amount: float, description: str = "") -> EventContribution:
        """
        Create a new contribution.
        
        Args:
            event_id: The ID of the event.
            contributor_id: The ID of the user profile contributing.
            amount: The amount of the contribution.
            description: The description of the contribution.
            
        Returns:
            The created contribution.
        """
        event = cls.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found.")
        
        contributor = cls.get_by_id(UserProfile, contributor_id)
        if not contributor:
            raise ValueError(f"User profile with ID {contributor_id} not found.")
        
        return cls.create(
            EventContribution,
            event=event,
            contributor=contributor,
            amount=amount,
            description=description
        )
    
    @classmethod
    def update_contribution(cls, contribution: EventContribution, **kwargs) -> EventContribution:
        """
        Update a contribution.
        
        Args:
            contribution: The contribution to update.
            **kwargs: Updated attributes.
            
        Returns:
            The updated contribution.
        """
        return cls.update(contribution, **kwargs)
    
    @classmethod
    def delete_contribution(cls, contribution: EventContribution) -> bool:
        """
        Delete a contribution.
        
        Args:
            contribution: The contribution to delete.
            
        Returns:
            True if the contribution was deleted, False otherwise.
        """
        return cls.delete(contribution)
    
    @classmethod
    def get_total_contributions_for_event(cls, event_id: int) -> float:
        """
        Get the total amount of contributions for an event.
        
        Args:
            event_id: The ID of the event.
            
        Returns:
            The total amount of contributions.
        """
        contributions = cls.get_contributions_by_event(event_id)
        return sum(contribution.amount for contribution in contributions)
    
    @classmethod
    def search_events(cls, query: str, village_id: int = None) -> List[CommunityEvent]:
        """
        Search for events by the given query.
        
        Args:
            query: The search query.
            village_id: The ID of the village to filter by, or None for all villages.
            
        Returns:
            A list of events matching the query.
        """
        fields = ['title', 'description', 'location', 'contact_person', 'notes']
        events = cls.search(CommunityEvent, query, fields)
        
        if village_id:
            return [event for event in events if event.village_id == village_id]
        
        return events 