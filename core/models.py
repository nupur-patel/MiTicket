from django.db import models
from django.contrib.auth.models import User

ROLE_TYPES = (
    ('ADMIN','ADMIN'),
    ('SUPPORT','SUPPORT'),
    ('DEVELOPER','DEVELOPER'),
    ('DEVELOPER MANAGER','DEVELOPER MANAGEAR'),
    ('MANAGER','MANAGER')
)


# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=100,choices=ROLE_TYPES)
    company = models.CharField(max_length= 100)

    def __str__(self):
        return self.user.email + self.role
    
    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def allow_type(self):
        return ['DEVELOPER','DEVELOPER MANAGER']