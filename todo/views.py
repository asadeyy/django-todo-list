from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Folder, Task
from .forms import FolderForm, TaskForm

def index(request, id):
    #すべてのフォルダを取得する
    folders = Folder.objects.filter(created_at__lte=timezone.now()).order_by('created_at')
    #選ばれたフォルダを取得する
    current_folder = get_object_or_404(Folder, id=id)
    #選ばれたフォルダのタスクを取得する
    tasks = Task.objects.filter(folder_id = current_folder.id)

    return render(request, 'index.html', {
        'folders':folders,
        'tasks':tasks,
        'current_folder_id': current_folder.id,
    })

def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.created_at = timezone.now()
            folder.save()
            return redirect('tasks.index', id=folder.id)
    else:
        form = FolderForm()
    return render(request, 'create_folders.html', {'form': form})

def create_task(request, id):
    #選ばれたフォルダを取得する
    current_folder = get_object_or_404(Folder, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_at = timezone.now()
            task.folder_id = current_folder
            task.save()
            return redirect('tasks.index', id=current_folder.id)
    else:
        form = TaskForm()
    return render(request, 'create_tasks.html', {'form': form, 'id':current_folder.id})

def edit_task(request, id, task_id):
    #選ばれたタスクを取得する
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('tasks.index', id=task.folder_id.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit.html', {'form': form, 'task':task})

def home(request):
    return render(request, 'home.html', {})