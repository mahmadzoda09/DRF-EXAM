from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.CharField(max_length=150)
    bio = models.TextField()
    city = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    avatar = models.FileField(upload_to='avatars/', max_length=100)
    
    def __str__(self):
        return self.user