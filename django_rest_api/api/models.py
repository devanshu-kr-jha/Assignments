from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    company_name = models.CharField(max_length=70)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zip = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    web = models.URLField()
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
