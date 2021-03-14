from django.shortcuts import render
from collections import ChainMap
from django.views import generic
from .models import Word
from django.db.models import Q, F
import random

def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={},
    )
  
class TranGView(generic.ListView):
    """Generic class-based view for the dictionary."""
    model = Word
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TranGView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['lang'] = self.kwargs['lang']
        return context

class TranEView(generic.ListView):
    """Generic class-based view for the dictionary."""
    model = Word
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TranEView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['lang'] = self.kwargs['lang']
        return context

class TranGResultsView(generic.ListView):
    """Generic class-based view for the German-English translation."""
    model = Word
    template_name = 'translator/trang_results.html'
    
    def get_queryset(self):
        gword = self.request.GET.get('getword','')
        object_list = Word.objects.filter(
            Q(german__icontains=gword)
            )
        return object_list

class TranEResultsView(generic.ListView):
    """Generic class-based view for the English-Germna translation."""
    model = Word
    template_name = 'translator/trane_results.html'
        
    def get_queryset(self):
        eword = self.request.GET.get('getword','')
        object_list = Word.objects.filter(
            Q(english__icontains=eword)
            )
        return object_list
        
def quiz(request):
    """View for the quiz entry form (language and number of questions)."""
    # initialize queryset and make it a session variable
    qs = []
    correct = 0
    resp = ''
    request.session['qs'] = qs
    request.session['correct'] = correct
    request.session['resp'] = resp

    # Render the HTML template quiz.html with the data in the context variable.
    return render(
        request,
        'quiz.html',
        context={},
    )

class QuizDetailView(generic.ListView):
    """Generic class-based view for the quiz."""
    model = Word
    template_name = 'translator/quiz_detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        qs = self.request.session.get('qs')
        context['correct'] = self.request.session.get('correct')
        if qs == []:
            inumber = 1
            lang = self.request.GET.get('lang')
            qnumber = int(self.request.GET.get('qnumber'))
            context['inumber'] = inumber
            context['lang'] = lang
            context['qnumber'] = int(qnumber)
            self.request.session['inumber'] = inumber
            self.request.session['lang'] = lang
            self.request.session['qnumber'] = int(qnumber)
            word_list = Word.objects.all().values_list('german', 'english', 'count') 
            qs = random.sample(list(word_list), qnumber)
            self.request.session['qs'] = qs
            context.update({'qs': qs})
            iofqs = qs[inumber-1]
            context['iofqs'] = qs[inumber-1]
            self.request.session['iofqs'] = qs[inumber-1]
        else:
            inumber = self.request.session.get('inumber')
            inumber += 1
            context.update({'inumber': inumber})
            self.request.session['inumber'] = inumber
            iofqs = qs[inumber-1]
            context.update({'iofqs': iofqs})
            self.request.session['iofqs'] = iofqs
            context['lang'] = self.request.session.get('lang')
            context['qnumber'] = self.request.session.get('qnumber')
            context['qs'] = self.request.session.get('qs')
        return context

class QuizResultView(generic.ListView):
    """Generic class-based view for the quiz."""
    model = Word
    template_name = 'translator/quiz_result.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(QuizResultView, self).get_context_data(**kwargs)

        # Check answer
        lang = self.request.session.get('lang')
        answer = self.request.GET.get('answer')
        iofqs = self.request.session.get('iofqs')
        inumber = self.request.session.get('inumber')
        correct = self.request.session.get('correct')
        resp = self.request.session.get('resp')
        if lang == 'g':
            if answer == iofqs[1]:
                resp = 'Richtig'
                correct += 1
                context.update({'correct': correct})
                context.update({'resp': resp})
                self.request.session['correct'] = correct
                self.request.session['resp'] = resp
            else:
                resp = 'Falsch'
                context.update({'resp': resp})
                self.request.session['resp'] = resp
                context['correct'] = self.request.session.get('correct')
        else:
            if answer == iofqs[0]:
                resp = 'Correct'
                correct = self.request.session.get('correct')
                correct += 1
                context.update({'correct': correct})
                context.update({'resp': resp})
                self.request.session['correct'] = correct
                self.request.session['resp'] = resp
            else:
                resp = 'Incorrect'
                context.update({'resp': resp})
                self.request.session['resp'] = resp
                context['correct'] = self.request.session.get('correct')
        context['resp'] = resp

        # Update count field in database
        Word.objects.filter(german=iofqs[0]).update(count=F('count') +1)

        # Create data and add it to the context
        context['inumber'] = self.request.session.get('inumber')
        context['lang'] = self.request.session.get('lang')
        context['qnumber'] = self.request.session.get('qnumber')
        context['qs'] = self.request.session.get('qs')
        context['iofqs'] = self.request.session.get('iofqs')
        return context
        
