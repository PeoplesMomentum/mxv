from django.shortcuts import render, redirect, get_object_or_404
from questions.models import Question, Answer, Candidate, Vote, Category
from questions.forms import QuestionForm, AnswerForm
from mxv.settings import QUESTIONS_VISIBLE_TO_NON_STAFF, NCG_VOTING_URL
from django.contrib.auth.decorators import login_required
from django.db.models import *
from django.db.models.functions import *
import logging
import pprint

pp = pprint.PrettyPrinter()

# TODO: let users cancel their vote, edit their question, edit their answer

# renders the questions index
@login_required
def index(request):
    if not (QUESTIONS_VISIBLE_TO_NON_STAFF or request.user.is_staff):
        return redirect('index')
    if request.method == 'POST':
        if request.POST.get('category_select'):
            current_category = request.POST.get('category_select')
            return show_questions(request, None, current_category)
        elif request.POST.get('answer_display_region'):
            question_pk = request.POST.get('answer_display_question')
            current_region = request.POST.get('answer_display_region')
            if current_region == "None":
                current_region = None
            question = get_object_or_404(Question, pk=question_pk)
            current_category = request.POST.get('category_select')
            return show_answers(request, question, None, current_region)
        else: 
            return handle_question_submission(request)
    else:
        return show_questions(request)


def info(request):
    return render(request, 'questions/info.html')

def check_candidate(request):
    return Candidate.objects.filter(member__id=request.user.id).exists()

def show_questions(request, form=None, current_category=0):
    their_answers = Answer.objects \
        .filter(candidate__member__id=request.user.id) \
        .exclude(status='rejected')
    
    their_answers_for_question = their_answers.filter(question=OuterRef('pk'))
    their_votes_for_question = Vote.objects \
        .filter(member__id=request.user.id) \
        .filter(question=OuterRef('pk'))
    questions = Question.objects \
        .filter(status='approved') \
        .annotate(num_answers=Count('answers')) \
        .annotate(num_votes=Count('votes')) \
        .annotate(answered=Exists(their_answers_for_question)) \
        .annotate(voted=Exists(their_votes_for_question)) \
        .order_by('-num_votes','category__number',)
    num_questions = questions.count()
    categories = Category.objects.all()
    their_questions = Question.objects.filter(author__id=request.user.id)
    pending_question = their_questions.filter(status='pending')
    try:
        reject = their_questions.latest('reject_reason')
    except:
        reject =  None
    has_question = their_questions.exclude(status='rejected').exists()

    is_candidate = check_candidate(request)
    pending_answers = their_answers.filter(status='pending').count()
    if not form:
        form = QuestionForm() 
    
    context = { 
        'form': form,
        'has_question': has_question,
        'is_candidate': is_candidate,
        'pending_question': pending_question,
        'pending_answers': pending_answers,
        'questions': questions,
        'reject': reject,
        'current_category': int(current_category),
        'categories': categories,
        'num_questions': num_questions
    }
    return render(request, 'questions/questions.html', context)

def handle_question_submission(request):
    form = QuestionForm(request.POST)
    if check_candidate(request):
        return redirect('questions:index')
    if Question.objects.filter(author__id=request.user.id).exclude(status='rejected').exists():
        return redirect('questions:index')
    if not form.is_valid():
        return show_questions(request, form)
    question = form.save(commit = False)
    question.author = request.user
    question.save()
    return redirect('questions:index')

@login_required
def vote(request, pk):
    if not check_candidate(request):
        question = Question.objects.get(id=pk)
        Vote.objects.filter(member__id=request.user.id, question__category=question.category).delete() 
        vote = Vote.objects.create(question=question, member=request.user)
        vote.save()
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

def show_answers(request, question, form=None, current_region=None):
    is_candidate = check_candidate(request)
    candidate_answers = Answer.objects.filter(question__id=question.id, candidate__member__id=request.user.id)
    allow_answer = is_candidate and not candidate_answers.exclude(status='rejected').exists()
    has_answered = is_candidate and candidate_answers.filter(status='approved').exists()
    region_list = [
        {'code': None, 'readable' : 'All regions'},
        {'code': 'ysn', 'readable' : 'Yorkshire and the Humber, Cumbria, North East, Scotland, and International'},
        {'code': 'nww', 'readable' : 'North West and Wales'},
        {'code': 'mide', 'readable':  'Midlands and the East'},
        {'code': 'sesw', 'readable':  'South East and South West'},
        {'code': 'lon', 'readable' : 'London'},
        {'code': 'mper', 'readable':  'MPs and elected representatives'},
    ]
    current_region_readable = "All regions"
    for dict in region_list:
        for key, value in dict.items():
            if key=='code' and value == current_region:
                current_region_readable = dict['readable']
    answers = Answer.objects \
        .filter(question__id=question.id, status='approved') \
        .annotate(url=Concat(Value(f'{NCG_VOTING_URL}/nominate/status/'), 'candidate__candidate_code')) \
        .order_by('candidate__position', 'created_at')
    if current_region is not None:
        answers = answers.filter(candidate__position=current_region)
    pending_answers = is_candidate and candidate_answers.filter(status='pending')
    if candidate_answers.filter(status='rejected').order_by('-created_at').count() > 0:
        reject = candidate_answers.filter(status='rejected').order_by('-created_at')[0]
    else:
        reject = None
    if not form:
        form = AnswerForm()
    return render(request, 'questions/answers.html', {
        'allow_answer': allow_answer,
        'answers': answers,
        'form': form,
        'pending_answer': pending_answers,
        'question': question,
        'reject': reject,
        'has_answered': has_answered,
        'region_list': region_list,
        'current_region_code': current_region,
        'current_region_readable': current_region_readable
    })

def handle_answer_submission(request, question):
    candidates = Candidate.objects.filter(member__id=request.user.id)
    if not candidates.exists():
        return redirect('questions:answers', pk=question.id)
    candidate = candidates.get()
    if Answer.objects.filter(candidate=candidate, question=question).exclude(status='rejected').exists():
        return redirect('questions:answers', pk=question.id)
    form = AnswerForm(request.POST)
    if not form.is_valid():
        return show_answers(request, question, form)
    answer = form.save(commit = False)
    answer.candidate = candidate
    answer.question = question
    answer.save()
    return redirect('questions:index')
