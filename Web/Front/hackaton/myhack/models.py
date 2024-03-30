from django.db import models



class AnonUser(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    server_id = models.CharField(max_length=60, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
