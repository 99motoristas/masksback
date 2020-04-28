from django.db import models

class Driver(models.Model):
    hashed_phone = models.TextField()
    hashed_cpf = models.TextField()
    date = models.TextField()
    city = models.TextField()
