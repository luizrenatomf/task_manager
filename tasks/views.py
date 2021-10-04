from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
import datetime

from .models import Task
from .forms import TaskForm

@login_required
def taskList(request):
	search = request.GET.get('search')
	filter = request.GET.get('filter')

	# Para enviar ao template
	filtros = dict(Task.STATUS).keys()
	now = datetime.date.today()

	if search:
		tasks = Task.objects.filter(title__icontains=search,user=request.user)
	elif filter:
		tasks = Task.objects.filter(done=filter,user=request.user)
	else:
		tasks = Task.objects.all().order_by('-created_at').filter(user=request.user)
		paginator = Paginator(tasks,10)
		page = request.GET.get('page')
		tasks = paginator.get_page(page)
	
	return render(request,'tasks/list.html',{'tasks':tasks,'now':now,'filtros':filtros})


@login_required
def taskView(request,id):
	task = get_object_or_404(Task,pk=id)
	return render(request,'tasks/task.html',{'task':task})


@login_required
def newTask(request):
	if request.method == 'POST':
		form_task = TaskForm(request.POST)
		
		if form_task.is_valid():
			form_task = form_task.save(commit=False)
			form_task.user = request.user
			form_task.done = 'doing'
			form_task.save()

		messages.success(request,'Tarefa criada com sucesso')
		return redirect('/')
	else:	
		form_task = TaskForm()
		return render(request,'tasks/addtask.html',{'form1':form_task,})


@login_required
def editTask(request,id):
	task = get_object_or_404(Task,pk=id)
	form_task = TaskForm(instance=task)
	if request.method == 'POST':
		form_task = TaskForm(request.POST,instance=task)
		if form_task.is_valid():
			task.save()
			messages.success(request,'Tarefa atualizada com sucesso')
			return HttpResponseRedirect(reverse_lazy('task-list'))
		else:
			return render(request,'tasks/edittask.html',{'form_task':form_task,'task':task})
	else:
		return render(request,'tasks/edittask.html',{'form_task':form_task,'task':task})


@login_required
def deleteTask(request,id):
	task = get_object_or_404(Task,pk=id)
	task.delete()
	messages.info(request,'Tarefa deletada com sucesso.')
	return redirect('/')


@login_required
def changeStatus(request,id):
	task = get_object_or_404(Task,pk=id)
	if task.done == 'doing':
		task.done = 'done'
	else:
		task.done = 'doing'
	task.save()
	messages.success(request,'Tarefa atualizada com sucesso')
	return redirect('/')

