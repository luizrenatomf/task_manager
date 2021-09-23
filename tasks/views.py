from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
import datetime

from .models import Task, Tag
from .forms import TaskForm, TagForm

@login_required
def taskList(request):
	search = request.GET.get('search')
	filter = request.GET.get('filter')

	# Para contagem no cabeçalho
	tasksDoneRecently = Task.objects.filter(done='done',updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30),user=request.user).count() 
	tasksDone = Task.objects.filter(done='done',user=request.user).count() 
	tasksDoing = Task.objects.filter(done='doing',user=request.user).count()

	# Para enviar ao template
	filtros = dict(Task.STATUS).keys()
	now = datetime.date.today()

	if search:
		tasks = Task.objects.filter(title__icontains=search,user=request.user)
	elif filter:
		tasks = Task.objects.filter(done=filter,user=request.user)
	else:
		tasks = Task.objects.all().order_by('-created_at').filter(user=request.user)
		paginator = Paginator(tasks,7)
		page = request.GET.get('page')
		tasks = paginator.get_page(page)
	
	return render(request,'tasks/list.html',{'tasks':tasks,'tasksrecently':tasksDoneRecently,'tasksdone':tasksDone,'tasksdoing':tasksDoing,'now':now,'filtros':filtros})


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

		form_tag = TagForm(request.POST,instance=form_task)
		if form_tag.is_valid():
			form_tag = form_tag.save(commit=False)
			form_tag.task = form_task.id
			form_tag.save()
			
		return redirect('/')
	else:	
		form_task = TaskForm()
		form_tag = TagForm()
		return render(request,'tasks/addtask.html',{'form1':form_task,'form2':form_tag})


@login_required
def editTask(request,id):
	task = get_object_or_404(Task,pk=id)
	form = TaskForm(instance=task)
	if request.method == 'POST':
		form = TaskForm(request.POST,instance=task)
		if form.is_valid():
			task.save()
			return redirect('/')
		else:
			return render(request,'tasks/edittask.html',{'form':form,'task':task})
	else:
		return render(request,'tasks/edittask.html',{'form':form,'task':task})


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
	return redirect('/')


@login_required
def dashboard(request):
	pass
	