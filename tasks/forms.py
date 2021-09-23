from django import forms
from django.forms.widgets import DateInput

from .models import Task, Tag

class TaskForm(forms.ModelForm):
	title = forms.CharField(label=u'Título')
	do_date = forms.DateField(label=u'Data de entrega',widget=DateInput(format='%d/%m/%Y',attrs={'maxlength':'10'}),input_formats=['%d/%m/%Y',],)
	description = forms.Textarea()
	class Meta:
		model = Task
		fields = ('title','do_date','description',)


class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
		fields = ('tag',)
		