from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    UNIT_CHOICES = [
        ('minutes', 'Minutes'),
        ('count', 'Count'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises', null= True)
    exercise_name = models.CharField(max_length=50)
    exercise_unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    exercise_target = models.IntegerField()
    preset_type = models.CharField(max_length=20, blank=False, null=True)  # Optional field to store the preset type
    completed = models.IntegerField(default=0)
    

    def __str__(self):
        return self.exercise_name