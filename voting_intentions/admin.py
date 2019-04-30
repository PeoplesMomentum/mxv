from django.contrib import admin
from voting_intentions.models import Vote
from django.utils.safestring import mark_safe
from django.http.response import HttpResponse
import csv
from django.forms import TextInput
from django.db import models

class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'redirect_url')
    ordering = ('id', )
    fields = (
        'id',
        'name', 
        'redirect_url',
        'results_table'
    )
    readonly_fields = ('id', 'results_table', )
    formfield_overrides = { 
        models.TextField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    
    # returns the results table as HTML
    def results_table(self, vote):
                
        # header
        header = '<tr><th>Choice</th><th>Count</th><th>%</th><th>NB: unprocessed</th><th>NB: tags written</th><th>NB: unknown email</th></tr>'
        
        # choice rows        
        rows = []
        total = vote.intentions.all().count()
        for choice in vote.choices.all():
            count = choice.intentions.all().count()
            unprocessed = choice.intentions.filter(processed_at = None).count()
            tags_written = choice.intentions.filter(tags_written_to_nation_builder = True).count()
            unknown_email = choice.intentions.filter(email_unknown_in_nation_builder = True).count()
            row = '<tr><td>%d - %s</td><td>%d</td><td>%.2f</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (choice.number, choice.text, count, count / total * 100 if total > 0 else 0, unprocessed, tags_written, unknown_email)
            rows.append(row)
        
        # table
        table = '<table>' + header
        for row in rows:
            table += row
        table += '</table>'
        
        return mark_safe(table)
    results_table.short_description = 'results'
    
    # returns the intentions as a CSV response
    def response_change(self, request, obj):
        if 'export_intentions_as_csv' in request.POST:
            vote = obj

            # create the response and CSV
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s.csv' % vote.name
            writer = csv.writer(response, quoting = csv.QUOTE_ALL)
            
            # header
            writer.writerow(['email', 
                             'nation_builder_id', 
                             'time', 
                             'vote_id', 
                             'choice_number', 
                             'tags_written_to_nation_builder', 
                             'email_unknown_in_nation_builder' ])
            
            # intentions
            for intention in vote.intentions.all():
                writer.writerow([intention.email, 
                                 intention.nation_builder_id, 
                                 intention.recorded_at, 
                                 intention.vote_id, 
                                 intention.choice.number, 
                                 intention.tags_written_to_nation_builder,
                                 intention.email_unknown_in_nation_builder])
                
            return response
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)


admin.site.register(Vote, VoteAdmin)
