import json
import os
from django.core.management.base import BaseCommand
from village.models import District, Block, PoliceStation, PostOffice, Panchayat, Village

class Command(BaseCommand):
    help = 'Load village data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing village data')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'File {json_file} does not exist'))
            return
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            state_name = data.get('state')
            
            for district_data in data.get('districts', []):
                district_name = district_data.get('name')
                district, _ = District.objects.get_or_create(
                    name=district_name,
                    defaults={'state': state_name}
                )
                
                for block_data in district_data.get('blocks', []):
                    block_name = block_data.get('name')
                    block, _ = Block.objects.get_or_create(
                        name=block_name,
                        district=district
                    )
                    
                    for ps_data in block_data.get('police_stations', []):
                        ps_name = ps_data.get('name')
                        police_station, _ = PoliceStation.objects.get_or_create(
                            name=ps_name,
                            block=block
                        )
                        
                        for po_data in ps_data.get('post_offices', []):
                            po_name = po_data.get('name')
                            post_office, _ = PostOffice.objects.get_or_create(
                                name=po_name,
                                police_station=police_station
                            )
                            
                            for panchayat_data in po_data.get('panchayats', []):
                                panchayat_name = panchayat_data.get('name')
                                panchayat, _ = Panchayat.objects.get_or_create(
                                    name=panchayat_name,
                                    post_office=post_office
                                )
                                
                                for village_data in panchayat_data.get('villages', []):
                                    village_name = village_data.get('name')
                                    village_code = village_data.get('code')
                                    village, created = Village.objects.get_or_create(
                                        name=village_name,
                                        panchayat=panchayat,
                                        defaults={'code': village_code}
                                    )
                                    
                                    if created:
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f'Created village: {village_name} in {panchayat_name}, {po_name}, {ps_name}, {block_name}, {district_name}'
                                            )
                                        )
                                    else:
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f'Updated village: {village_name} in {panchayat_name}, {po_name}, {ps_name}, {block_name}, {district_name}'
                                            )
                                        )
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded village data'))
        
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading village data: {str(e)}')) 