from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"
