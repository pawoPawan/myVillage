import json
import os
from django.core.management.base import BaseCommand
from village.models import Village

class Command(BaseCommand):
    help = 'Load Bihar villages from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='data/bihar_villages.json',
                            help='Path to the JSON file containing Bihar village data')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Loading villages from {file_path}...'))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            state = data.get('state', 'Bihar')
            districts = data.get('districts', [])
            
            villages_created = 0
            
            for district in districts:
                district_name = district.get('name', '')
                villages = district.get('villages', [])
                
                self.stdout.write(f'Processing district: {district_name} with {len(villages)} villages')
                
                for village_data in villages:
                    village_name = village_data.get('name', '')
                    village_code = village_data.get('code', '')
                    
                    # Check if village already exists
                    if not Village.objects.filter(name=village_name, district=district_name).exists():
                        Village.objects.create(
                            name=village_name,
                            district=district_name,
                            state=state,
                            country='India',
                            description=f'Village code: {village_code}'
                        )
                        villages_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created {villages_created} villages'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading villages: {str(e)}')) 