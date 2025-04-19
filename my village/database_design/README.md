# My Village App - Database Design

This folder contains the database design documentation for the My Village application.

## Overview

The My Village app uses a modular database design to store and manage information about villages, users, events, services, and relationships. The design is organized into logical modules that handle specific aspects of the application.

## Design Documents

- [Complete Database Schema](schema.md) - Detailed description of all database tables and relationships
- [Entity Relationship Diagram](erd.md) - Visual representation of the database structure
- [Module Descriptions](modules.md) - Explanation of each module's purpose and functionality

## Key Features

1. **Modularity**: Each module handles a specific aspect of the application
2. **Hierarchical Location Structure**: Follows administrative hierarchy from state to village
3. **User Profiles**: Extended user profiles with personal information
4. **Community Events**: Comprehensive event management with contribution tracking
5. **Village Services**: Tracking of various services available in villages
6. **Relationship Management**: Both direct relationships and relationship requests
7. **Aadhaar Verification**: Secure verification process with proper status tracking

## Implementation

The database design is implemented using Django models. Each module corresponds to a set of related models in the Django application.

To apply this design to a new Django project:

1. Create the necessary models in your Django app
2. Run migrations to create the database tables
3. Implement the views and forms to interact with the data

## Maintenance

When updating the database design:

1. Update the relevant documentation files
2. Modify the Django models accordingly
3. Create and apply migrations
4. Update any affected views, forms, and templates 