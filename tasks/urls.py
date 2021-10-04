from django.urls import path

from . import views

urlpatterns = [
	path('',views.taskList,name='task-list'),
	path('task/<int:id>',views.taskView,name='task-view'),
	path('newtask/',views.newTask,name='nova-task'),
	path('edit/<int:id>',views.editTask,name='edit-task'),
	path('delete/<int:id>',views.deleteTask,name='delete-task'),
	path('changestatus/<int:id>',views.changeStatus,name='change-status'),
	path('tag/<slug:tag_slug>/',views.taskList,name='task_list_by_tag'),
]
