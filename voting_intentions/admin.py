from django.contrib import admin
from voting_intentions.models import Vote
from django.utils.safestring import mark_safe
from django import forms
from django.http.response import HttpResponse
import csv

class VoteAdminForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('name', 'redirect_url')
    name = forms.CharField(widget = forms.TextInput(attrs = { 'style': 'width:500px' }))
    redirect_url = forms.CharField(widget = forms.TextInput(attrs = { 'style': 'width:500px' }))

class VoteAdmin(admin.ModelAdmin):
    form = VoteAdminForm
    list_display = ('name', 'redirect_url')
    fields = (
        'name', 
        'redirect_url',
        'results_table'
    )
    readonly_fields = ('results_table', )
    
    # returns the results table as HTML
    def results_table(self, vote):
        
        # header
        header = '<tr><th>Choice</th><th>Count</th><th>%</th></tr>'
        
        # choice rows        
        rows = []
        total = vote.intentions.all().count()
        for choice in vote.choices.all():
            count = choice.intentions.all().count()#vote.intentions.filter(choice = choice).count()
            row = '<tr><td>%d - %s</td><td>%d</td><td>%.2f</td></tr>' % (choice.number, choice.text, count, count / total * 100 if total > 0 else 0)
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
            writer.writerow(['email', 'nation_builder_id', 'time', 'vote_id', 'choice_number' ])
            
            # intentions
            for intention in vote.intentions.all():
                writer.writerow([intention.email, intention.nation_builder_id, intention.recorded_at, intention.vote_id, intention.choice.number])
                
            return response
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)


admin.site.register(Vote, VoteAdmin)
