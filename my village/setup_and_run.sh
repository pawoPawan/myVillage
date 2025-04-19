#!/bin/bash

echo "Setting up My Village App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install django
pip install python-dotenv

# Create requirements.txt
echo "django" > requirements.txt
echo "python-dotenv" >> requirements.txt

# Make migrations
echo "Making migrations..."
python manage.py makemigrations
python manage.py migrate

# Load initial data
echo "Loading village data..."
python manage.py load_villages data/bihar_villages.json

# Create superuser if it doesn't exist
echo "Would you like to create a superuser? (y/n)"
read create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Run the development server
echo "Starting development server..."
python manage.py runserver

# Note: The script will end here when the server is stopped with Ctrl+C 