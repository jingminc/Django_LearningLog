from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'learning_log.settings')
django.setup()

from learning_logs.models import Topic, Entry
from learning_logs.forms import TopicForm, EntryForm

# Create your views here.
"""学习笔记的主页。"""
def index(request):
    return render(request, 'learning_logs/index.html')

"""显示所有的主题。"""
@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

"""显示单个主题及其所有的条目。"""
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户。
    check_topic_owner(topic,request)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

"""添加新主题。"""
@login_required
def new_topic(request):
    if request.method != 'POST':
        # 未提交数据：创建一个新表单。
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # 显示空表单或指出表单数据无效。
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

"""在特定主题中添加新条目。"""
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)
    if request.method != 'POST':
        # 未提交数据：创建一个空表单。
        form = EntryForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # 显示空表单或指出表单数据无效。
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

"""编辑既有条目。"""
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic,request)
    if request.method != 'POST':
        # 初次请求：使用当前条目填充表单。
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(topic,request):
	if topic.owner != request.user:
		raise Http404