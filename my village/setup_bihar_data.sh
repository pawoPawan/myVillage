#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the setup command
python manage.py setup_bihar_data --villages-per-district=20

echo "Bihar data setup completed!" 