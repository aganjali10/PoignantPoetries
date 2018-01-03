from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from poetries.models import Poetry, Comment
from django.utils import timezone
from poetries.forms import PoetryForm, CommentForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request,'poetries/index.html')

class PoetryListView(ListView):
    model = Poetry

    def get_queryset(self):
        return Poetry.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PoetryDetailView(DetailView):
    model = Poetry


class CreatePoetryView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'poetries/poetry_detail.html'

    form_class = PoetryForm

    model = Poetry


class PoetryUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'poetries/poetry_detail.html'

    form_class = PoetryForm

    model = Poetry


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'poetries/poetry_list.html'

    model = Poetry

    def get_queryset(self):
        return Poetry.objects.filter(published_date__isnull=True).order_by('create_date')


class PoetryDeleteView(LoginRequiredMixin,DeleteView):
    model = Poetry
    success_url = reverse_lazy('poetry_list')


@login_required
def poetry_publish(request, pk):
    poetry = get_object_or_404(Poetry, pk=pk)
    poetry.publish()
    return redirect('poetry_detail', pk=pk)

def add_comment_to_poetry(request, pk):
    poetry = get_object_or_404(Poetry, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.poetry = poetry
            comment.save()
            return redirect('poetry_detail', pk=poetry.pk)
    else:
        form = CommentForm()
    return render(request, 'poetries/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('poetry_detail', pk=comment.poetry.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    poetry_pk = comment.poetry.pk
    comment.delete()
    return redirect('poetry_detail', pk=poetry_pk)
