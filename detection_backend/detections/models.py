from django.db import models

# Create your models here.
class DetectionStats (models.Model):
    frame_count = models.IntegerField(default = 0)
    people_count = models.IntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add = True)