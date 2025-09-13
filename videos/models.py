from django.db import models

class Status(models.TextChoices):
	PENDING = "PENDING", "Pending"
	PROCESSING = "PROCESSING", "Processing"
	READY = "READY", "Ready"
	FAILED = "FAILED", "Failed"


class Video(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, max_length=1000)
	file_original = models.FileField(upload_to='uploads/')
	file_converted = models.FileField(upload_to='converted/', null=True, blank=True)
	status = models.CharField(
		max_length=120,
		choices=Status.choices,
		default="Pending",
	)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=120, unique=True)
	
	def __str__(self):
		return self.title
	