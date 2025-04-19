"""
Location Hierarchy module for database operations.

This module provides functionality for interacting with location-related models.
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from .base import BaseDB
from ..models import State, District, Block, PoliceStation, PostOffice, Panchayat, Village

class LocationHierarchyDB(BaseDB):
    """
    Class for interacting with location-related models.
    """
    
    @classmethod
    def get_state_by_id(cls, state_id: int) -> Optional[State]:
        """
        Get a state by its ID.
        
        Args:
            state_id: The ID of the state to retrieve.
            
        Returns:
            The state if found, None otherwise.
        """
        return cls.get_by_id(State, state_id)
    
    @classmethod
    def get_state_by_name(cls, state_name: str) -> Optional[State]:
        """
        Get a state by its name.
        
        Args:
            state_name: The name of the state to retrieve.
            
        Returns:
            The state if found, None otherwise.
        """
        try:
            return State.objects.get(name=state_name)
        except State.DoesNotExist:
            return None
    
    @classmethod
    def get_all_states(cls) -> List[State]:
        """
        Get all states.
        
        Returns:
            A list of all states.
        """
        return cls.get_all(State)
    
    @classmethod
    def create_state(cls, name: str, code: str = None) -> State:
        """
        Create a new state.
        
        Args:
            name: The name of the state.
            code: The code of the state.
            
        Returns:
            The created state.
        """
        return cls.create(State, name=name, code=code)
    
    @classmethod
    def get_district_by_id(cls, district_id: int) -> Optional[District]:
        """
        Get a district by its ID.
        
        Args:
            district_id: The ID of the district to retrieve.
            
        Returns:
            The district if found, None otherwise.
        """
        return cls.get_by_id(District, district_id)
    
    @classmethod
    def get_districts_by_state(cls, state_id: int) -> List[District]:
        """
        Get all districts in a state.
        
        Args:
            state_id: The ID of the state.
            
        Returns:
            A list of districts in the state.
        """
        return cls.filter(District, state_id=state_id)
    
    @classmethod
    def create_district(cls, name: str, state_id: int) -> District:
        """
        Create a new district.
        
        Args:
            name: The name of the district.
            state_id: The ID of the state.
            
        Returns:
            The created district.
        """
        state = cls.get_state_by_id(state_id)
        if not state:
            raise ValueError(f"State with ID {state_id} not found.")
        
        return cls.create(District, name=name, state=state)
    
    @classmethod
    def get_block_by_id(cls, block_id: int) -> Optional[Block]:
        """
        Get a block by its ID.
        
        Args:
            block_id: The ID of the block to retrieve.
            
        Returns:
            The block if found, None otherwise.
        """
        return cls.get_by_id(Block, block_id)
    
    @classmethod
    def get_blocks_by_district(cls, district_id: int) -> List[Block]:
        """
        Get all blocks in a district.
        
        Args:
            district_id: The ID of the district.
            
        Returns:
            A list of blocks in the district.
        """
        return cls.filter(Block, district_id=district_id)
    
    @classmethod
    def create_block(cls, name: str, district_id: int) -> Block:
        """
        Create a new block.
        
        Args:
            name: The name of the block.
            district_id: The ID of the district.
            
        Returns:
            The created block.
        """
        district = cls.get_district_by_id(district_id)
        if not district:
            raise ValueError(f"District with ID {district_id} not found.")
        
        return cls.create(Block, name=name, district=district)
    
    @classmethod
    def get_police_station_by_id(cls, police_station_id: int) -> Optional[PoliceStation]:
        """
        Get a police station by its ID.
        
        Args:
            police_station_id: The ID of the police station to retrieve.
            
        Returns:
            The police station if found, None otherwise.
        """
        return cls.get_by_id(PoliceStation, police_station_id)
    
    @classmethod
    def get_police_stations_by_block(cls, block_id: int) -> List[PoliceStation]:
        """
        Get all police stations in a block.
        
        Args:
            block_id: The ID of the block.
            
        Returns:
            A list of police stations in the block.
        """
        return cls.filter(PoliceStation, block_id=block_id)
    
    @classmethod
    def create_police_station(cls, name: str, block_id: int) -> PoliceStation:
        """
        Create a new police station.
        
        Args:
            name: The name of the police station.
            block_id: The ID of the block.
            
        Returns:
            The created police station.
        """
        block = cls.get_block_by_id(block_id)
        if not block:
            raise ValueError(f"Block with ID {block_id} not found.")
        
        return cls.create(PoliceStation, name=name, block=block)
    
    @classmethod
    def get_post_office_by_id(cls, post_office_id: int) -> Optional[PostOffice]:
        """
        Get a post office by its ID.
        
        Args:
            post_office_id: The ID of the post office to retrieve.
            
        Returns:
            The post office if found, None otherwise.
        """
        return cls.get_by_id(PostOffice, post_office_id)
    
    @classmethod
    def get_post_offices_by_police_station(cls, police_station_id: int) -> List[PostOffice]:
        """
        Get all post offices in a police station.
        
        Args:
            police_station_id: The ID of the police station.
            
        Returns:
            A list of post offices in the police station.
        """
        return cls.filter(PostOffice, police_station_id=police_station_id)
    
    @classmethod
    def create_post_office(cls, name: str, police_station_id: int) -> PostOffice:
        """
        Create a new post office.
        
        Args:
            name: The name of the post office.
            police_station_id: The ID of the police station.
            
        Returns:
            The created post office.
        """
        police_station = cls.get_police_station_by_id(police_station_id)
        if not police_station:
            raise ValueError(f"Police station with ID {police_station_id} not found.")
        
        return cls.create(PostOffice, name=name, police_station=police_station)
    
    @classmethod
    def get_panchayat_by_id(cls, panchayat_id: int) -> Optional[Panchayat]:
        """
        Get a panchayat by its ID.
        
        Args:
            panchayat_id: The ID of the panchayat to retrieve.
            
        Returns:
            The panchayat if found, None otherwise.
        """
        return cls.get_by_id(Panchayat, panchayat_id)
    
    @classmethod
    def get_panchayats_by_post_office(cls, post_office_id: int) -> List[Panchayat]:
        """
        Get all panchayats in a post office.
        
        Args:
            post_office_id: The ID of the post office.
            
        Returns:
            A list of panchayats in the post office.
        """
        return cls.filter(Panchayat, post_office_id=post_office_id)
    
    @classmethod
    def create_panchayat(cls, name: str, post_office_id: int) -> Panchayat:
        """
        Create a new panchayat.
        
        Args:
            name: The name of the panchayat.
            post_office_id: The ID of the post office.
            
        Returns:
            The created panchayat.
        """
        post_office = cls.get_post_office_by_id(post_office_id)
        if not post_office:
            raise ValueError(f"Post office with ID {post_office_id} not found.")
        
        return cls.create(Panchayat, name=name, post_office=post_office)
    
    @classmethod
    def get_village_by_id(cls, village_id: int) -> Optional[Village]:
        """
        Get a village by its ID.
        
        Args:
            village_id: The ID of the village to retrieve.
            
        Returns:
            The village if found, None otherwise.
        """
        return cls.get_by_id(Village, village_id)
    
    @classmethod
    def get_villages_by_panchayat(cls, panchayat_id: int) -> List[Village]:
        """
        Get all villages in a panchayat.
        
        Args:
            panchayat_id: The ID of the panchayat.
            
        Returns:
            A list of villages in the panchayat.
        """
        return cls.filter(Village, panchayat_id=panchayat_id)
    
    @classmethod
    def create_village(cls, name: str, panchayat_id: int, code: str = None) -> Village:
        """
        Create a new village.
        
        Args:
            name: The name of the village.
            panchayat_id: The ID of the panchayat.
            code: The code of the village.
            
        Returns:
            The created village.
        """
        panchayat = cls.get_panchayat_by_id(panchayat_id)
        if not panchayat:
            raise ValueError(f"Panchayat with ID {panchayat_id} not found.")
        
        return cls.create(Village, name=name, panchayat=panchayat, code=code)
    
    @classmethod
    def get_location_hierarchy(cls, village_id: int) -> Dict[str, Any]:
        """
        Get the complete location hierarchy for a village.
        
        Args:
            village_id: The ID of the village.
            
        Returns:
            A dictionary containing the complete location hierarchy.
        """
        village = cls.get_village_by_id(village_id)
        if not village:
            return {}
        
        panchayat = village.panchayat
        post_office = panchayat.post_office
        police_station = post_office.police_station
        block = police_station.block
        district = block.district
        state = district.state
        
        return {
            'village': village,
            'panchayat': panchayat,
            'post_office': post_office,
            'police_station': police_station,
            'block': block,
            'district': district,
            'state': state
        }
    
    @classmethod
    def search_locations(cls, query: str) -> Dict[str, List[Any]]:
        """
        Search for locations by the given query.
        
        Args:
            query: The search query.
            
        Returns:
            A dictionary containing lists of matching locations for each level.
        """
        if not query:
            return {
                'states': [],
                'districts': [],
                'blocks': [],
                'police_stations': [],
                'post_offices': [],
                'panchayats': [],
                'villages': []
            }
        
        return {
            'states': cls.search(State, query, ['name', 'code']),
            'districts': cls.search(District, query, ['name']),
            'blocks': cls.search(Block, query, ['name']),
            'police_stations': cls.search(PoliceStation, query, ['name']),
            'post_offices': cls.search(PostOffice, query, ['name']),
            'panchayats': cls.search(Panchayat, query, ['name']),
            'villages': cls.search(Village, query, ['name', 'code'])
        } 