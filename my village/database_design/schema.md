# My Village App - Complete Database Schema

This document provides a detailed description of all database tables and their relationships in the My Village application.

## 1. User Management Module

### User (Django's built-in model)
| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique username for login |
| email | EmailField | User's email address |
| password | CharField | Hashed password |
| first_name | CharField | User's first name |
| last_name | CharField | User's last name |
| is_active | BooleanField | Whether the user account is active |
| is_staff | BooleanField | Whether the user has staff permissions |
| date_joined | DateTimeField | When the user joined |
| last_login | DateTimeField | When the user last logged in |

### UserProfile
| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Link to User model |
| village | ForeignKey | Link to Village model |
| education | TextField | User's educational background |
| profession | CharField | User's profession |
| hobbies | TextField | User's hobbies and interests |
| achievements | TextField | User's achievements |
| social_contributions | TextField | User's contributions to society |
| aadhaar_verified | BooleanField | Whether Aadhaar is verified |
| banner_dismissed | BooleanField | Whether verification banner is dismissed |
| age | PositiveIntegerField | User's age |
| gender | CharField | User's gender (choices) |
| father_name | CharField | User's father's name |
| mother_name | CharField | User's mother's name |
| nickname | CharField | User's nickname |
| profile_picture | ImageField | User's profile picture |
| created_at | DateTimeField | When the profile was created |
| updated_at | DateTimeField | When the profile was last updated |

## 2. Location Hierarchy Module

### State
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | State name |
| code | CharField | State code |
| created_at | DateTimeField | When the state was created |
| updated_at | DateTimeField | When the state was last updated |

### District
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | District name |
| state | ForeignKey | Link to State model |
| created_at | DateTimeField | When the district was created |
| updated_at | DateTimeField | When the district was last updated |

### Block
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Block name |
| district | ForeignKey | Link to District model |
| created_at | DateTimeField | When the block was created |
| updated_at | DateTimeField | When the block was last updated |

### PoliceStation
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Police station name |
| block | ForeignKey | Link to Block model |
| created_at | DateTimeField | When the police station was created |
| updated_at | DateTimeField | When the police station was last updated |

### PostOffice
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Post office name |
| police_station | ForeignKey | Link to PoliceStation model |
| created_at | DateTimeField | When the post office was created |
| updated_at | DateTimeField | When the post office was last updated |

### Panchayat
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Panchayat name |
| post_office | ForeignKey | Link to PostOffice model |
| created_at | DateTimeField | When the panchayat was created |
| updated_at | DateTimeField | When the panchayat was last updated |

### Village
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Village name |
| code | CharField | Village code |
| panchayat | ForeignKey | Link to Panchayat model |
| created_at | DateTimeField | When the village was created |
| updated_at | DateTimeField | When the village was last updated |

## 3. Community Events Module

### CommunityEvent
| Field | Type | Description |
|-------|------|-------------|
| title | CharField | Event title |
| description | TextField | Event description |
| event_type | CharField | Type of event (choices) |
| start_date | DateTimeField | When the event starts |
| end_date | DateTimeField | When the event ends |
| village | ForeignKey | Link to Village model |
| created_by | ForeignKey | Link to UserProfile model |
| location | CharField | Specific location within village |
| expected_attendees | PositiveIntegerField | Expected number of attendees |
| is_public | BooleanField | Whether event is open to all |
| requires_registration | BooleanField | Whether registration is required |
| registration_deadline | DateTimeField | Registration deadline |
| budget | DecimalField | Estimated budget |
| contact_person | CharField | Contact person name |
| contact_phone | CharField | Contact phone number |
| notes | TextField | Additional notes |
| created_at | DateTimeField | When the event was created |
| updated_at | DateTimeField | When the event was last updated |

### EventContribution
| Field | Type | Description |
|-------|------|-------------|
| event | ForeignKey | Link to CommunityEvent model |
| contributor | ForeignKey | Link to UserProfile model |
| amount | DecimalField | Contribution amount |
| description | TextField | Contribution description |
| created_at | DateTimeField | When the contribution was created |
| updated_at | DateTimeField | When the contribution was last updated |

## 4. Village Services Module

### VillageService
| Field | Type | Description |
|-------|------|-------------|
| village | ForeignKey | Link to Village model |
| name | CharField | Service name |
| service_type | CharField | Type of service (choices) |
| description | TextField | Service description |
| address | TextField | Service address |
| contact_number | CharField | Contact number |
| created_at | DateTimeField | When the service was created |
| updated_at | DateTimeField | When the service was last updated |

## 5. Relationships Module

### Relationship
| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey | Link to UserProfile model |
| related_user | ForeignKey | Link to UserProfile model |
| relationship_type | CharField | Type of relationship (choices) |
| status | CharField | Relationship status (choices) |
| description | TextField | Relationship description |
| created_at | DateTimeField | When the relationship was created |
| updated_at | DateTimeField | When the relationship was last updated |

### RelationshipRequest
| Field | Type | Description |
|-------|------|-------------|
| from_user | ForeignKey | Link to UserProfile model |
| to_user | ForeignKey | Link to UserProfile model |
| relationship_type | CharField | Type of relationship (choices) |
| status | CharField | Request status (choices) |
| message | TextField | Request message |
| created_at | DateTimeField | When the request was created |
| updated_at | DateTimeField | When the request was last updated |

## 6. Aadhaar Verification Module

### AadhaarVerification
| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey | Link to User model |
| aadhaar_number | CharField | Aadhaar number |
| front_image | ImageField | Front image of Aadhaar card |
| back_image | ImageField | Back image of Aadhaar card |
| status | CharField | Verification status (choices) |
| submitted_at | DateTimeField | When verification was submitted |
| reviewed_at | DateTimeField | When verification was reviewed |
| reviewed_by | ForeignKey | Link to User model |
| rejection_reason | TextField | Reason for rejection if applicable |
| created_at | DateTimeField | When the verification was created | 