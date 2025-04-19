# My Village App - Module Descriptions

This document provides detailed explanations of each module in the My Village application database design.

## 1. User Management Module

The User Management module handles all aspects of user accounts and profiles in the application.

### Purpose
- Manage user authentication and authorization
- Store user profile information
- Link users to villages
- Track user verification status

### Key Functionality
- User registration and login
- Profile creation and management
- Profile picture upload
- Personal information storage
- Village association

### Models
- **User**: Django's built-in user model for authentication
- **UserProfile**: Extended profile with additional user information

### Relationships
- One-to-one relationship between User and UserProfile
- Many-to-one relationship between UserProfile and Village

## 2. Location Hierarchy Module

The Location Hierarchy module manages the administrative structure from state down to village level.

### Purpose
- Represent the administrative hierarchy of locations
- Organize villages within their administrative units
- Support location-based queries and filtering

### Key Functionality
- Hierarchical organization of locations
- Location-based search and filtering
- Administrative boundary representation

### Models
- **State**: Top-level administrative unit
- **District**: Second-level administrative unit
- **Block**: Third-level administrative unit
- **PoliceStation**: Fourth-level administrative unit
- **PostOffice**: Fifth-level administrative unit
- **Panchayat**: Sixth-level administrative unit
- **Village**: Seventh-level administrative unit

### Relationships
- Each level has a foreign key to the level above it
- Villages belong to a Panchayat
- Panchayats belong to a PostOffice
- And so on up the hierarchy

## 3. Community Events Module

The Community Events module manages village events and contributions.

### Purpose
- Track community events in villages
- Manage event details and registrations
- Record contributions to events

### Key Functionality
- Event creation and management
- Event type categorization
- Registration management
- Contribution tracking
- Budget management

### Models
- **CommunityEvent**: Stores information about village events
- **EventContribution**: Records contributions to events

### Relationships
- Many-to-one relationship between CommunityEvent and Village
- Many-to-one relationship between CommunityEvent and UserProfile (created_by)
- Many-to-one relationship between EventContribution and CommunityEvent
- Many-to-one relationship between EventContribution and UserProfile (contributor)

## 4. Village Services Module

The Village Services module manages services available in villages.

### Purpose
- Track services available in villages
- Categorize services by type
- Provide contact information for services

### Key Functionality
- Service registration
- Service categorization
- Contact information management

### Models
- **VillageService**: Stores information about village services

### Relationships
- Many-to-one relationship between VillageService and Village

## 5. Relationships Module

The Relationships module manages connections between users.

### Purpose
- Track relationships between village members
- Manage relationship requests
- Support social networking features

### Key Functionality
- Relationship creation and management
- Relationship request handling
- Relationship type categorization
- Social network visualization

### Models
- **Relationship**: Stores established relationships between users
- **RelationshipRequest**: Manages pending relationship requests

### Relationships
- Many-to-one relationship between Relationship and UserProfile (user)
- Many-to-one relationship between Relationship and UserProfile (related_user)
- Many-to-one relationship between RelationshipRequest and UserProfile (from_user)
- Many-to-one relationship between RelationshipRequest and UserProfile (to_user)

## 6. Aadhaar Verification Module

The Aadhaar Verification module manages the verification of user identities using Aadhaar cards.

### Purpose
- Verify user identities
- Link users to their villages
- Ensure security and authenticity

### Key Functionality
- Aadhaar card submission
- Verification process management
- Status tracking
- Rejection handling

### Models
- **AadhaarVerification**: Stores Aadhaar verification information

### Relationships
- Many-to-one relationship between AadhaarVerification and User
- Many-to-one relationship between AadhaarVerification and User (reviewed_by)

## Module Interactions

The modules interact with each other in various ways:

1. **User-Village Connection**: The User Management module connects users to villages, which are managed by the Location Hierarchy module.

2. **Event-Village Connection**: The Community Events module links events to villages, which are managed by the Location Hierarchy module.

3. **Service-Village Connection**: The Village Services module links services to villages, which are managed by the Location Hierarchy module.

4. **User-Event Connection**: Users can create events and contribute to events, connecting the User Management and Community Events modules.

5. **User-User Connection**: The Relationships module connects users to each other, all managed by the User Management module.

6. **User Verification**: The Aadhaar Verification module verifies users, which affects their village association in the User Management module.

These interactions ensure that the application can provide a comprehensive view of village life and community connections. 