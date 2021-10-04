from django import forms
from django.forms.widgets import DateInput

from .models import Task
from taggit.forms import *

class TaskForm(forms.ModelForm):
	title = forms.CharField(label=u'Título')
	do_date = forms.DateField(label=u'Data de entrega',widget=DateInput(format='%d/%m/%Y',attrs={'maxlength':'10'}),input_formats=['%d/%m/%Y',],required=False)
	description = forms.CharField(label=u'Descrição',widget=forms.Textarea,required=False)
	tags = forms.CharField(label=u'Marcadores',widget=TagWidget,required=False)

	class Meta:
		model = Task
		fields = ('title','do_date','description','tags')

