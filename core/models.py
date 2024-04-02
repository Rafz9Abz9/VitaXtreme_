from django.db import models
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=250)
    message = models.CharField(max_length=1050)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
