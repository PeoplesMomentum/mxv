from django import test
from questions.models import *
from members.models import Member
import logging
import pprint

pp = pprint.PrettyPrinter()

class TestQuestions(test.TestCase):
    def _create_member(self, email, name, is_candidate):
        member = Member.objects.create_member(email, name, 'password')
        member.is_active = True
        member.save()
        if is_candidate:
            candidate = Candidate.objects.create(member=member)
            return candidate
        else:
            return member


    def setUp(self):
        self.client = test.Client()
        self.voter = self._create_member('voter@voter.com', 'My Voter', False)
        self.voter2 = self._create_member('voter2@voter.com', 'My Voter 2', False)
        self.candidate = self._create_member('candidate@candidate.com', 'Candidate', True)
        self.category1 = Category.objects.create(number=1, title='Category 1')
        self.category2 = Category.objects.create(number=2, title='Category 2')

    def tearDown(self):
        Vote.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Category.objects.all().delete()

    # Writing convention for these tests 
    # Setup, blank line, code under test, blank line, assertions

    def test_users(self):
        self.assertTrue(Member.objects.filter(name='My Voter').exists())
        self.assertTrue(Member.objects.filter(name='Candidate').exists())

    def test_questions_appear(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.voter)

        resp = self.client.get('/questions/')
        
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp.context)
        self.assertFalse(resp.context['is_candidate'])
        questions = resp.context['questions']
        self.assertEqual(1, len(questions))
        self.assertEqual('What is the meaning of life?', questions[0].text)

    def test_new_question(self):
        self.client.force_login(self.voter)

        resp = self.client.post('/questions/', { 'category': self.category1.id, 'text': 'Question text'}, follow=True)

        questions = resp.context['questions']
        self.assertEqual(0, len(questions))
        self.assertEqual(1, Question.objects.all().count())
        self.assertEqual('Question text', Question.objects.get(author=self.voter).text)

    def test_candidate_cannot_ask(self):
        self.client.force_login(self.candidate.member)

        resp = self.client.post('/questions/', { 'category': self.category1.id, 'text': 'Question text'}, follow=True)

        self.assertFalse(Question.objects.filter(author=self.candidate.member).exists())

    def test_cannot_ask_twice(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='pending', text='What is the meaning of life?')
        self.client.force_login(self.voter)

        resp = self.client.post('/questions/', { 'category': self.category2.id, 'text': 'Question text'}, follow=True)

        self.assertEqual(1, Question.objects.filter(author=self.voter).count())

    def test_vote(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.voter)

        resp = self.client.get(f'/questions/vote/{question1.id}/')

        self.assertEqual(1, Vote.objects.filter(member=self.voter, question=question1).count())

    def test_multi_vote_does_nothing(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.voter)

        resp = self.client.get(f'/questions/vote/{question1.id}/')
        resp = self.client.get(f'/questions/vote/{question1.id}/')

        self.assertEqual(1, Vote.objects.filter(member=self.voter, question=question1).count())
        self.assertEqual(question1.id, Vote.objects.get(member=self.voter, question__category=self.category1).question.id)

    def test_change_vote(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        question2 = Question.objects.create(category=self.category1, author=self.voter2, status='approved', text='What is your favourite colour?')
        self.client.force_login(self.voter)

        resp = self.client.get(f'/questions/vote/{question1.id}/')
        resp = self.client.get(f'/questions/vote/{question2.id}/')

        self.assertEqual(1, Vote.objects.filter(member=self.voter, question__category=self.category1).count())
        self.assertEqual(question2.id, Vote.objects.get(member=self.voter, question__category=self.category1).question.id)

    def test_candidate_cant_vote(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.candidate.member)

        resp = self.client.get(f'/questions/vote/{question1.id}/')

        self.assertEqual(0, Vote.objects.filter(member=self.candidate.member).count())

    def test_answers_appear(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        answer1 = Answer.objects.create(candidate=self.candidate, question=question1, status='approved', text='Forty-two')
        self.client.force_login(self.voter)

        resp = self.client.get(f'/questions/question/{question1.id}/')

        self.assertFalse(resp.context['allow_answer'])
        self.assertEqual('What is the meaning of life?', resp.context['question'].text)
        self.assertEqual(1, len(resp.context['answers']))
        self.assertEqual('Forty-two', resp.context['answers'][0].text)

    def test_answer(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.candidate.member)

        resp = self.client.post(f'/questions/question/{question1.id}/', {'text': 'Who cares?'}, follow=True)
     
        self.assertEqual('Who cares?', Answer.objects.get(question=question1, candidate=self.candidate, status='pending').text)
        
    def test_non_candidate_cannot_answer(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        answer1 = Answer.objects.create(candidate=self.candidate, question=question1, status='approved', text='Forty-two')
        self.client.force_login(self.voter)

        resp = self.client.post(f'/questions/question/{question1.id}/', {'text': 'I say different'}, follow=True)
     
        self.assertFalse(Answer.objects.filter(candidate__member__id=self.voter.id).exists())
        
    def test_can_see_answer_form(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        self.client.force_login(self.candidate.member)

        resp = self.client.get(f'/questions/question/{question1.id}/')

        self.assertTrue(resp.context['allow_answer'])

    def test_candidate_cannot_see_answer_form_twice(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        answer1 = Answer.objects.create(candidate=self.candidate, question=question1, status='pending', text='Forty-two')
        self.client.force_login(self.candidate.member)

        resp = self.client.get(f'/questions/question/{question1.id}/')

        self.assertFalse(resp.context['allow_answer'])

    def test_cannot_answer_twice(self):
        question1 = Question.objects.create(category=self.category1, author=self.voter, status='approved', text='What is the meaning of life?')
        answer1 = Answer.objects.create(candidate=self.candidate, question=question1, status='pending', text='Forty-two')
        self.client.force_login(self.candidate.member)

        resp = self.client.post(f'/questions/question/{question1.id}/', {'text': 'I changed my mind'}, follow=True)
     
        self.assertEqual('Forty-two', Answer.objects.get(question=question1, candidate=self.candidate).text)
