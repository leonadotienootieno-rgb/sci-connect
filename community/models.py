from django.db import models
from accounts.models import CustomUser


class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('template', 'CV Template'),
        ('protocol', 'Lab Protocol'),
        ('guide', 'Interview Guide'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='uploaded_resources')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title

class Topic(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='topics')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Post on {self.topic.name}"