# My Village App - Entity Relationship Diagram

This document provides a text-based description of the Entity Relationship Diagram (ERD) for the My Village application.

## User Management Module

```
User (1) ----< UserProfile (1)
UserProfile (N) ----< Village (1)
```

## Location Hierarchy Module

```
State (1) ----< District (N)
District (1) ----< Block (N)
Block (1) ----< PoliceStation (N)
PoliceStation (1) ----< PostOffice (N)
PostOffice (1) ----< Panchayat (N)
Panchayat (1) ----< Village (N)
```

## Community Events Module

```
Village (1) ----< CommunityEvent (N)
UserProfile (1) ----< CommunityEvent (N) [created_by]
CommunityEvent (1) ----< EventContribution (N)
UserProfile (1) ----< EventContribution (N) [contributor]
```

## Village Services Module

```
Village (1) ----< VillageService (N)
```

## Relationships Module

```
UserProfile (1) ----< Relationship (N) [user]
UserProfile (1) ----< Relationship (N) [related_user]
UserProfile (1) ----< RelationshipRequest (N) [from_user]
UserProfile (1) ----< RelationshipRequest (N) [to_user]
```

## Aadhaar Verification Module

```
User (1) ----< AadhaarVerification (N)
User (1) ----< AadhaarVerification (N) [reviewed_by]
```

## Complete ERD Description

The My Village application database consists of six main modules, each handling a specific aspect of the application:

1. **User Management Module**: Manages user accounts and profiles, with a one-to-one relationship between User and UserProfile, and a many-to-one relationship between UserProfile and Village.

2. **Location Hierarchy Module**: Represents the administrative hierarchy from state down to village, with each level having a one-to-many relationship with the level below it.

3. **Community Events Module**: Manages village events and contributions, with many-to-one relationships between events and villages, events and users (created_by), contributions and events, and contributions and users (contributor).

4. **Village Services Module**: Tracks services available in villages, with a many-to-one relationship between services and villages.

5. **Relationships Module**: Manages connections between users, with many-to-one relationships between relationships and users (both user and related_user), and between relationship requests and users (both from_user and to_user).

6. **Aadhaar Verification Module**: Handles user verification using Aadhaar cards, with many-to-one relationships between verifications and users (both user and reviewed_by).

These modules interact with each other to provide a comprehensive view of village life and community connections. For example, the User Management module connects users to villages, which are managed by the Location Hierarchy module. The Community Events module links events to villages, and users can create events and contribute to events, connecting the User Management and Community Events modules.

## Key Relationships

- **User-Village**: Users belong to villages, which are part of the administrative hierarchy.
- **Event-Village**: Events are associated with villages.
- **Service-Village**: Services are available in villages.
- **User-Event**: Users can create events and contribute to events.
- **User-User**: Users can have relationships with other users.
- **User-Verification**: Users can verify their identity using Aadhaar cards.

## Cardinality

- **One-to-One**: User to UserProfile
- **One-to-Many**: Each level in the location hierarchy to the level below it
- **Many-to-One**: UserProfile to Village, CommunityEvent to Village, EventContribution to CommunityEvent, VillageService to Village, Relationship to UserProfile, RelationshipRequest to UserProfile, AadhaarVerification to User

This ERD provides a clear understanding of how the different entities in the My Village application relate to each other, facilitating database design, implementation, and maintenance. 