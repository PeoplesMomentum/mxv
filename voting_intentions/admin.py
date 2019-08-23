from django.contrib import admin
from voting_intentions.models import Vote, VoteTag, Choice, ChoiceTag, UrlParameter
from django.utils.safestring import mark_safe
from django.http.response import HttpResponse
import csv
from django.forms import TextInput
from django.db import models
from nested_admin import nested
from mxv.models import DefaultUrlParameter

class ChoiceTagInline(nested.NestedTabularInline):
    model = ChoiceTag
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    
class ChoiceInline(nested.NestedTabularInline):
    model = Choice
    ordering = ['number']
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    inlines = [ChoiceTagInline]
    
class VoteTagInline(nested.NestedTabularInline):
    model = VoteTag
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    
class UrlParameterInline(nested.NestedTabularInline):
    model = UrlParameter
    ordering = ['name']
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 50 })}, 
    }
    
class VoteAdmin(nested.NestedModelAdmin):
    list_display = ('id', 'name', 'redirect_url', 'votes_cast')
    ordering = ('id', )
    fields = (
        'id',
        'name', 
        'redirect_url',
        'nation_builder_urls',
        'votes_cast',
        'results_table',
        'default_url_parameters'
    )
    readonly_fields = ('id', 'nation_builder_urls', 'results_table', 'default_url_parameters', 'votes_cast')
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    inlines = [VoteTagInline, ChoiceInline, UrlParameterInline]
    
    # returns the number of votes
    def votes_cast(self, vote):
        return vote.intentions.count()
    
    # returns the results table as HTML
    def results_table(self, vote):
                
        # header
        header = '<tr><th>Choice</th><th>Count</th><th>%</th><th>NB: unprocessed</th><th>NB: tags written</th><th>NB: unknown email</th></tr>'
        
        # choice rows        
        rows = []
        total = vote.intentions.all().count()
        for choice in vote.choices.all().order_by('number'):
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
    
    # URLs for use in NationBuilder
    def nation_builder_urls(self, vote):
        urls = ''
        for choice in vote.choices.all().order_by('number'):
            parameters = []
            parameters.append(('vote', str(vote.id)))
            parameters.append(('choice', str(choice.number)))
            for param in vote.url_parameters.all().order_by('name'):
                parameters.append((param.name, param.nation_builder_value if param.nation_builder_value else ''))
            urls += '<p>https://my.peoplesmomentum.com/voting_intentions?%s</p>' % '&'.join('='.join(param) for param in parameters)
        return mark_safe(urls)
    nation_builder_urls.short_description = 'NationBuilder email button URLs'
    
    # displays the default URL parameters
    def default_url_parameters(self, vote):
        
        # returns an empty string for None
        def blank(text):
            return text if text else ""
        
        # header
        header = '<tr><th>Name</th><th>Pass On Name</th><th>NationBuilder Value</th></tr>'
        
        # default rows        
        rows = []
        for param in DefaultUrlParameter.objects.all():
            row = '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (param.name, blank(param.pass_on_name), blank(param.nation_builder_value))
            rows.append(row)
        
        # table
        table = '<table>' + header
        for row in rows:
            table += row
        table += '</table>'
        
        return mark_safe(table)
    default_url_parameters.short_description = 'Default URL parameters'
    
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

