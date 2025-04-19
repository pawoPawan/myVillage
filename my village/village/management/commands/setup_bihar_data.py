from django.core.management.base import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Set up Bihar districts and villages data'

    def add_arguments(self, parser):
        parser.add_argument('--villages-per-district', type=int, default=10, 
                            help='Number of sample villages to generate per district')

    def handle(self, *args, **options):
        self.stdout.write('Starting to set up Bihar data...')
        
        # First, import the districts
        self.stdout.write('Step 1: Importing Bihar districts...')
        call_command('import_bihar_districts')
        
        # Then, generate sample villages
        self.stdout.write('Step 2: Generating sample villages...')
        call_command('generate_bihar_villages', villages_per_district=options['villages_per-district'])
        
        self.stdout.write(self.style.SUCCESS('Successfully set up Bihar data')) 