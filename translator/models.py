from django.db import models

# Create your models here.

class Word(models.Model):
    """Model representing a word and its translation"""
    german = models.CharField(max_length=100)
    english = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.german

