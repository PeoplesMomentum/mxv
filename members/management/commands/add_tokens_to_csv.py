# run locally to update the live database
# ./manage.py add_tokens_to_csv <CSV file>

# the input CSV file should contain nationbuilder_id and email exported from NationBuilder

import django
django.setup()

from django.core.management.base import BaseCommand
import csv
from members.models import NationBuilderPerson

class Command(BaseCommand):

    # sets up the parameters
    def add_arguments(self, parser):
        parser.add_argument('in_csv_filename', type = str)
    
    # logs to the console and the log file
    log_filename = ''
    def log(self, text = '', new = False):
        print(text)
        if self.log_filename != '':
            log_file = open(self.log_filename, mode = 'w' if new else 'a')
            print(text, file = log_file)
            log_file.close()

    # processed the CSV file
    def handle(self, *args, **options):        

        # setup
        in_csv_filename = options['in_csv_filename']
        
        # set up logging
        self.log_filename = '%s.log' % in_csv_filename
        self.log('Log file: %s' % (self.log_filename), new = True)
        
        # read from the CSV
        self.log('CSV: %s' % in_csv_filename)
        self.log()
        in_csv = open(in_csv_filename, mode = 'r')
        reader = csv.DictReader(in_csv)
         
        # write to the same filename but with .out.csv appended and with the token instead of the email
        out_csv_filename = '%s.out.csv' % in_csv_filename
        out_csv = open(out_csv_filename, mode = 'w')
        writer = csv.DictWriter(out_csv, fieldnames = ['nationbuilder_id', 'my_momentum_unique_token'])
        writer.writeheader()
         
        # for each row in CSV...
        processed = 0
        for row in reader:
            nationbuilder_id = row['nationbuilder_id']
            email = row['email']
         
            # find by email or create a record in mxv
            person = NationBuilderPerson.objects.using('live').filter(email = email).first()
            if not person:
                person = NationBuilderPerson.objects.using('live').create(nation_builder_id = nationbuilder_id, email = email)
                
            # update person's NationBuilder id if missing
            if not person.nation_builder_id or person.nation_builder_id == '':
                person.nation_builder_id = nationbuilder_id
                person.save()
             
            # read the token from the record
            my_momentum_unique_token = person.unique_token
                 
            # write the id and token to the output CSV
            writer.writerow({ 'nationbuilder_id': nationbuilder_id, 'my_momentum_unique_token': my_momentum_unique_token })
             
            # debug
            self.log(person)
            processed += 1
        
        # close the files
        in_csv.close()
        out_csv.close()
        
        # print total processed
        self.log()
        self.log('Processed: %d into %s' % (processed, out_csv_filename))
        self.log()
        
# entry point when debugging - comment out when running with manage.py
#command = Command()
#command.handle(csv_filename = '/Users/[username redacted]/Downloads/test.csv')