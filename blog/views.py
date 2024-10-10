# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * ## import the models (e.g., Article)
from .forms import * ## import the forms (i.e. CreateCommentForm)
from django.urls import reverse
from typing import Any

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object method
    def get_object(self):
        '''Return one Article chosed at random.'''

        # explicitly add an error to generate a call stack trace:
        # y = 3 / 0

        # retrieve all of the articles
        all_articles = Article.objects.all()
        # pick one at random
        article = random.choice(all_articles)
        return article

class ArticleView(DetailView):
    '''Display one Article selected by PK'''
    model = Article # the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

class CreateCommentView(CreateView):
    """
    A view to create a comment on the article
    - on GET: send back the form to display
    - on POST: read/process the form, and save new Comment to the database
    """
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        """
        return the URL to redirect on success
        """
        #article = Article.objects.get(pk=self.kwargs['pk'])

        # return "show_all" 
        # return reverse('article', kwargs={'pk':article.pk}) # look up the URL whose name is "show_all"

        return reverse('article', kwargs=self.kwargs)
    
    def form_valid(self,form):
        """
        this method is called as part of the form processing steps
        form_valid is called after the form is validated,
        BEFORE saving data to the database
        """

        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid() self.kwargs={self.kwargs}')
        # Here is what printed out:
        """
        CreateCommentView.form_valid() form={'author': 'Truc', 'text': 'print self.kwargs of the CreateCommentView.form_valid()'}
        CreateCommentView.form_valid() self.kwargs={'pk': 2}
        => NOTE: anything that is specified in the URL pattern, we have access to it
        """
        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach this Article to the instance  of the Comment to set its PK
        form.instance.article = article # like comment.article = article
        """
        Note: form.instance = 1 comment
        """

        # delegate work to superclass version
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #return super().get_context_data(**kwargs)

        # get all context data from the superclass
        context = super().get_context_data(**kwargs)

        # add the Article referred to by the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        context['article'] = article # this is the actual object of type article
        return context