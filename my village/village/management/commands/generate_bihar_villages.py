from django.core.management.base import BaseCommand
from village.models import Village
import random
import time

class Command(BaseCommand):
    help = 'Generate sample villages for each district in Bihar'

    def add_arguments(self, parser):
        parser.add_argument('--villages-per-district', type=int, default=10, 
                            help='Number of sample villages to generate per district')

    def handle(self, *args, **options):
        villages_per_district = options['villages_per-district']
        self.stdout.write(f'Starting to generate {villages_per_district} sample villages per district in Bihar...')
        
        # List of districts in Bihar with their village counts
        bihar_districts = [
            ("Araria", 745),
            ("Arwal", 317),
            ("Aurangabad", 1853),
            ("Banka", 2113),
            ("Begusarai", 1150),
            ("Bhagalpur", 1525),
            ("Bhojpur", 1223),
            ("Buxar", 1136),
            ("Darbhanga", 1251),
            ("Gaya", 2893),
            ("Gopalganj", 1539),
            ("Jamui", 1508),
            ("Jehanabad", 586),
            ("Kaimur (Bhabua)", 1698),
            ("Katihar", 1543),
            ("Khagaria", 303),
            ("Kishanganj", 774),
            ("Lakhisarai", 474),
            ("Madhepura", 442),
            ("Madhubani", 1116),
            ("Munger", 865),
            ("Muzaffarpur", 1795),
            ("Nalanda", 1061),
            ("Nawada", 1089),
            ("Pashchim Champaran", 1491),
            ("Patna", 1411),
            ("Purba Champaran", 1303),
            ("Purnia", 1276),
            ("Rohtas", 2082),
            ("Saharsa", 469),
            ("Samastipur", 1254),
            ("Saran", 1770),
            ("Sheikhpura", 316),
            ("Sheohar", 204),
            ("Sitamarhi", 842),
            ("Siwan", 1533),
            ("Supaul", 554),
            ("Vaishali", 1572)
        ]
        
        # Common village name prefixes and suffixes in Bihar
        prefixes = ["Dakshin", "Uttar", "Purba", "Pashchim", "Madhya", "Naya", "Purana", "Chota", "Bada", "Raj"]
        suffixes = ["pur", "nagar", "ganj", "bazar", "tola", "chak", "dih", "patti", "kothi", "tand"]
        
        # Common block names in Bihar
        block_names = ["Sadar", "Barh", "Bikram", "Dalsinghsarai", "Hilsa", "Islampur", "Jehanabad", "Kako", "Mokama", "Rajgir"]
        
        total_villages = 0
        
        for district_name, village_count in bihar_districts:
            self.stdout.write(f'Processing district: {district_name}')
            
            # Get or create the district
            try:
                district = Village.objects.get(name=district_name, district=district_name)
            except Village.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'District {district_name} not found. Skipping.'))
                continue
            
            # Generate sample villages for this district
            for i in range(villages_per_district):
                # Generate a random village name
                prefix = random.choice(prefixes)
                suffix = random.choice(suffixes)
                village_name = f"{prefix} {suffix}"
                
                # Generate a random block name
                block_name = random.choice(block_names)
                
                # Create the village
                try:
                    village, created = Village.objects.get_or_create(
                        name=village_name,
                        defaults={
                            'district': district_name,
                            'state': 'Bihar',
                            'country': 'India',
                            'police_station': block_name,
                            'description': f'Sample village in {district_name} district, {block_name} block'
                        }
                    )
                    
                    if created:
                        total_villages += 1
                        self.stdout.write(f'Created village: {village_name} in {district_name}, {block_name}')
                    else:
                        self.stdout.write(f'Village already exists: {village_name}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating village {village_name}: {str(e)}'))
            
            # Be nice to the database
            time.sleep(0.1)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {total_villages} sample villages in Bihar')) 