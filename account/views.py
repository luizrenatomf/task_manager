from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from tasks.models import Task

@login_required
def dashboard(request):
	tasksDoneRecently = Task.objects.filter(done='done',updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30),user=request.user).count() 
	tasksDone = Task.objects.filter(done='done',user=request.user).count() 
	tasksDoing = Task.objects.filter(done='doing',user=request.user).count()

	return render(request,'account/dashboard.html',{'tasksrecently':tasksDoneRecently,'tasksdone':tasksDone,'tasksdoing':tasksDoing,})


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			# Cria um objeto para o novo usuário, mas não o salva ainda
			new_user = user_form.save(commit=False)
			# Define a senha escolhida
			new_user.set_password(user_form.cleaned_data['password'])
			# Salva o objeto User
			new_user.save()
			# Cria o perfil do usuário
			Profile.objects.create(user=new_user)
			return render(request,'account/register_done.html',{'new_user':new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request,'account/register.html',{'user_form':user_form})
	

@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request,'Profile updated successfully')
		else:
			messages.error(request,'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})

