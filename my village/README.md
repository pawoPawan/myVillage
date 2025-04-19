# My Village App

A web application to manage village profiles, community events, and local services in Bihar.

## Features

- Village profile management with complete administrative hierarchy
- User profiles with education, profession, and achievements
- Community events and contributions tracking
- Village services directory
- Relationship mapping between village members

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation and Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd my-village
```

2. Make the setup script executable:
```bash
chmod +x setup_and_run.sh
```

3. Run the setup script:
```bash
./setup_and_run.sh
```

The script will:
- Create a virtual environment
- Install required dependencies
- Set up the database
- Load initial village data
- Offer to create a superuser
- Start the development server

## Manual Setup (if script fails)

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Load initial data:
```bash
python manage.py load_villages data/bihar_villages.json
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `village/` - Main Django app directory
  - `models.py` - Database models for villages, users, events, etc.
  - `views.py` - View functions for handling requests
  - `templates/` - HTML templates
  - `management/commands/` - Custom management commands
- `data/` - Data files including village information
- `setup_and_run.sh` - Setup and run script

## Administrative Hierarchy

The application follows this hierarchy:
1. State (Bihar)
2. Districts
3. Blocks
4. Police Stations
5. Post Offices
6. Panchayats
7. Villages

## Usage

1. Access the application at http://127.0.0.1:8000/
2. Log in as superuser to access admin interface at http://127.0.0.1:8000/admin/
3. Create your village profile
4. Add members, events, and services
5. Explore other villages and connect with members

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 