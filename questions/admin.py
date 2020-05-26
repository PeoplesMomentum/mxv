from django.contrib import admin
from questions.models import *

admin.site.register(Category)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ('member',)
    autocomplete_fields = ('member',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ('text', 'category', 'status' )
  fields = ('author', 'created_at', 'text', 'status', 'reject_reason')
  readonly_fields = ('text', 'author', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
  list_display = ('text', 'status')
  fields = ('candidate', 'created_at', 'question', 'text', 'status', 'reject_reason')
  readonly_fields = ('candidate', 'text', 'created_at', 'question')