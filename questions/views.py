from django.shortcuts import render, redirect, get_object_or_404
from questions.models import Question, Answer, Candidate, Vote
from questions.forms import QuestionForm, AnswerForm
from mxv.settings import QUESTIONS_VISIBLE_TO_NON_STAFF
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import logging

# TODO: let users cancel their vote, edit their question, edit their answer

# renders the questions index
@login_required
def index(request):
    if not (QUESTIONS_VISIBLE_TO_NON_STAFF or request.user.is_staff):
        return redirect('index')
    if request.method == 'POST':
        return handle_question_submission(request)
    else:
        return show_questions(request)

def can_vote_for_question(question, request):
    return Vote.objects \
        .filter(question__category=question.category, member__id=request.user.id) \
        .count() < 1

def show_questions(request):
    questions = Question.objects \
        .filter(status='approved') \
        .annotate(num_votes=Count('votes')) \
        .order_by('category__number', '-num_votes')
    pending_count = Question.objects.filter(author__id=request.user.id, status='pending').count()
    rejects = Question.objects \
        .filter(author__id=request.user.id, status='rejected') \
        .order_by('created_at')
    for question in questions:
        question.can_vote = can_vote_for_question(question, request)
    return render(request, 'questions/questions.html', { 
        'questions': questions,
        'pending_count': pending_count,
        'rejects': rejects,
        'form': QuestionForm() 
    })

def handle_question_submission(request):
    form = QuestionForm(request.POST)
    # TODO check word length, etc
    if not form.is_valid():
        # TODO show error message, return user's original answer so they can edit
        return show_questions(request)
    question = form.save(commit = False)
    question.author = request.user
    question.save()
    return redirect('questions:index')

@login_required
def vote(request, pk):
    # TODO some kind of warning repeat votes not allowed
    question = Question.objects.get(id=pk)
    if can_vote_for_question(question, request) and \
        Vote.objects.filter(question=question, member__id=request.user.id).count() == 0:
        vote = Vote.objects.create(question=question, member=request.user)
        vote.save()
    # TODO tell the user their vote is recorded
    return redirect('questions:index')


@login_required
def answers(request, pk):
    if not (QUESTIONS_VISIBLE_TO_NON_STAFF or request.user.is_staff):
        return redirect('index')
    question = get_object_or_404(Question, pk = pk)

    if request.method == 'POST':
        return handle_answer_submission(request, question)
    else:
        return show_answers(request, question)

def show_answers(request, question):
    answers = Answer.objects.filter(question__id=question.id).filter(status='approved').order_by('candidate__position', 'created_at')
    is_candidate = Candidate.objects.filter(member__id=request.user.id).count() > 0
    candidate_answers = Answer.objects.filter(question__id=question.id, candidate__id=request.user.id)
    allow_answer = is_candidate and candidate_answers.exclude(status='rejected').count() == 0
    has_pending = is_candidate and candidate_answers.filter(status='pending').count() > 0
    rejects =  candidate_answers.filter(status='rejected')
    if rejects.count() > 0:
        reject = rejects[0]
    else:
        reject = None
    return render(request, 'questions/answers.html', {
        'answers': answers,
        'question': question,
        'allow_answer': allow_answer,
        'has_pending': has_pending,
        'reject': reject,
        'form': AnswerForm()
    })

def handle_answer_submission(request, question):
    candidates = Candidate.objects.filter(member__id=request.user.id)
    if not candidates.count():
        # TODO show error message - user isn't a candidate
        return show_questions(request, question)
    form = AnswerForm(request.POST)
    # TODO check word length, etc
    if not form.is_valid():
        # TODO show error message, return user's original answer so they can edit
        return show_questions(request, question)
    answer = form.save(commit = False)
    answer.candidate = candidates.get()
    answer.question = question
    answer.save()
    return redirect('questions:index')
