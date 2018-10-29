from django.contrib import admin
from consultations.models import Consultation
from django.utils.safestring import mark_safe
from django.http.response import HttpResponse
import csv

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'pre_questions_text', 'post_questions_text', 'voting_start', 'voting_end', 'visible_to_non_staff')
    fields = (        
        ('name'), 
        ('description'), 
        ('pre_questions_text', 'post_questions_text'),
        ('voting_start', 'voting_end'),
        ('visible_to_non_staff'),
        ('results_table')
    )
    readonly_fields = ('results_table',)
    
    # returns the results table as HTML (separate header per question as the choices are all different)
    def results_table(self, consultation):
        rows = []
        
        # for each question...
        for question in consultation.questions.order_by('number'):

            # write the choices as a header
            choices = question.choices.all().order_by('display_order')
            header = '<tr><th>%s</th><th></th>' % ('Question' if question.number == 1 else '')
            for choice in choices:
                header += '<th>%s (%%)</th>' % choice
            header += '</tr>'
            rows.append(header)
            
            # write count (%) as a row
            row = '<tr><td>%d</td><td>%s</td>' % (question.number, question.text)
            for choice in choices:
                count = question.answers.filter(choice__text = choice).count()
                total = question.answers.count()
                row += '<td>%d (%d)</td>' % (count, count / total * 100 if total > 0 else 0)
            row += '</tr>'
            rows.append(row)
        
        # write a table 
        table = '<table>'
        for row in rows:
            table += row
        table += '</table>'
            
        return mark_safe(table)
    results_table.short_description = 'results'

    # returns the results table as a CSV response (separate header per question as the choices are all different)
    def response_change(self, request, obj):
        if 'export_results_as_csv' in request.POST:
            consultation = obj

            # create the response and CSV
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s.csv' % consultation.name
            writer = csv.writer(response, quoting = csv.QUOTE_ALL)
            
            # for each question...
            for question in consultation.questions.order_by('number'):
        
                # write the choices as a header
                headers = ['question_number', 'question_text']
                choices = question.choices.all().order_by('display_order')
                for choice in choices:
                    headers.append('%s_count' % choice)
                    headers.append('%s_percent' % choice)
                writer.writerow(headers)
                
                # write count and % as a row
                fields = [question.number, question.text]
                total = question.answers.count()
                for choice in choices:
                    count = question.answers.filter(choice__text = choice).count()
                    fields.append(count)
                    fields.append(count / total * 100 if total > 0 else 0)
                writer.writerow(fields)
                
            return response
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)

admin.site.register(Consultation, ConsultationAdmin)
