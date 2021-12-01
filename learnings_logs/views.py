from django.shortcuts import render
from .models import Topic
from django.http import HttpResponseRedirect

from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .forms import TopicForm, EntryForm, Entry
# Create your views here.

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

def index(request):
    """Жомашняя страница приложения LL"""
    return render(request, 'learnings_logs/index.html')

@login_required
def topics(request):
    '''Выводим список тем'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learnings_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    ''' Выводит одну тему и все ее записи'''
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    # знак - сортирует запсии в обратном порядке
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learnings_logs/topic.html', context)

@login_required
def new_topics(request):
    # Орпдееляет новую тему
    if request.method != 'POST':
        # Данные не отпрвалялись, создается форма
        form = TopicForm()
    else:
        # Отправлены данные ПОСТ , обработать данные
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learnings_logs:topics'))
    context = {'form': form}
    return render(request, 'learnings_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # Добавляет новую запись по конкретной теме
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != 'POST':
        #Данные не отправлялись, создается пустая форма
        form = EntryForm()
    else:
        # Отправляем данные ПОСТ , обработтаь данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learnings_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learnings_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # Редактирует существующую запись
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # исходный апрос. форма заполеняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправка данных пост. обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learnings_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learnings_logs/edit_entry.html', context)