# run locally to reset member names in the live database from their NationBuilder full names
# ./manage.py reset_member_names_from_nation_builder log_filename

import django
django.setup()

from django.core.management.base import BaseCommand
from mxv.nation_builder import NationBuilder
from members.models import Member

class Command(BaseCommand):

    # sets up the parameters
    def add_arguments(self, parser):
        parser.add_argument('log_filename', type = str)
    
    # logs to the console and the log file
    log_filename = ''
    def log(self, text = '', new = False):
        print(text)
        if self.log_filename != '':
            log_file = open(self.log_filename, mode = 'w' if new else 'a')
            print(text, file = log_file)
            log_file.close()

    # updates the members' names
    def handle(self, *args, **options):      
        nb = NationBuilder()
        dry_run = False
        
        # returns the field's value or an empty string
        def field_path_value(fields, field_path):
            values = [field[1] for field in fields if field[0] == field_path]
            return values[0] if len(values) > 0 else ''

        # set up logging
        self.log_filename = options['log_filename']
        self.log('Log file: %s' % self.log_filename, new = True)
        self.log('Dry run:  %s' % 'True' if dry_run else 'False')
        self.log()
        
        # for each member...
        processed = 0
        no_person = 0
        no_nation_builder_id = 0
        identical = 0
        different = 0
        members = Member.objects.using('live').all()
        total = members.count()
        for member in members:
            try:
                result = ''
                
                # get the NationBuilder id
                person = member.nation_builder_person
                if not person:
                    no_person += 1
                    raise Exception('no person record')
                nation_builder_id = person.nation_builder_id
                if not nation_builder_id:
                    no_nation_builder_id += 1
                    raise Exception('no NationBuilder id')
                
                # get the NationBuilder record
                nb_record = nb.PersonFieldsAndValues(nation_builder_id)
                
                # compare the names and update if required
                name = member.name
                nb_name = field_path_value(nb_record, 'person.full_name')
                if name == nb_name:
                    identical += 1
                    result = 'Names identical'
                else:
                    different += 1
                    if not dry_run:
                        member.name = nb_name
                        member.save()
                    result = 'Names different, member name set to %s' % nb_name
                
            except Exception as e:
                result = 'Error: %s' % repr(e)

            # progress
            processed += 1
            self.log('%d of %d - %s, %s, %s: %s' % (processed, total, member.email, name, '' if nation_builder_id == None else str(nation_builder_id), result))
        
        # print total processed
        self.log()
        self.log('Processed:           %d' % processed)
        self.log('No person record:    %d' % no_person)
        self.log('No NationBuilder id: %d' % no_nation_builder_id)
        self.log('Identical:           %d' % identical)
        self.log('Different:           %d' % different)
        self.log()
        
# entry point when debugging - comment out when running with manage.py
# command = Command()
# command.handle(log_filename = '/Users/[username redacted]/Desktop/reset_member_names_from_nation_builder.log')