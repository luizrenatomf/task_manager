from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

class Task(models.Model):
	STATUS = (('doing','Doing'),('done','Done'),('delivered','Delivered'),('late','Late'))

	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	done = models.CharField(max_length=9,choices=STATUS)
	user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	do_date = models.DateField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	tags = TaggableManager()

	def __str__(self):
		return self.title

