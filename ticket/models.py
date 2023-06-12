from django.db import models
from core.models import AppUser

def get_status():
    return (
        ('NOT ACKNOLEDGE','Not Acknoledge'),
        ('ACKNOLEDGE','Acknoledge'),
        ('IN DEVELOPMENT','In Development'),
        ('TESTING','Testing'),
        ('DEPLOYED','Deployed'),
        ('CLOSED','Closed'),
    )

def get_criticality_choices():
    CRITICALITY_CHOICES = (
        ('LIGHT','Light'),
        ('MODERATE','Moderate'),
        ('URGENT','Urgent'),
        ('CRITICAL','Critical'),
    )
    return CRITICALITY_CHOICES

def get_tool_choices():
    TOOL_CHOICES = (
        ('MIDELIVERY','MIDELIVERY'),
        ('MISHOWROOM','MISHOWROOM'),
        ('HUB','HUB'),
    )
    return TOOL_CHOICES
def get_country_choices():
    COUNTRY_CHOICES = (
        ('US','US'),
        ('CANADA','CANADA'),
        ('PR','PR'),
        )
    return COUNTRY_CHOICES


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField('Error URL',blank=True,null=  True)
    criticality = models.CharField(max_length=100,choices=get_criticality_choices())
    current_status = models.CharField(max_length=100, default='NOT ACKNOLEDGE',choices=get_status())
    tools = models.CharField(max_length=100, choices=get_tool_choices())
    country = models.CharField(max_length=100, choices=get_country_choices())
    complaint_by = models.ForeignKey(AppUser,on_delete=models.PROTECT, related_name='created_by',blank=True,null=True)
    currently_assigned = models.ForeignKey(AppUser,on_delete=models.PROTECT,related_name = 'assigned_to', blank=True, null= True)
    is_archived = models.BooleanField(default=False)
    issue_type = models.TextField(default = '')
    # Timestamps
    deadline = models.DateTimeField(blank=True,null= True)
    completed = models.DateTimeField(blank=True,null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class TicketFiles(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.PROTECT,related_name='ticket_files')
    file = models.FileField(upload_to='media/')    


class TicketLogs(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.PROTECT)    
    change_by = models.ForeignKey(AppUser,on_delete=models.PROTECT)
    status = models.CharField(blank=True,null=True,choices=get_status(),max_length=100)
    change_msg = models.TextField(blank= True,null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.ticket.id) + ':' + self.change_msg
    class Meta:
        ordering = ['-created_at']

class TicketComment(models.Model):
    message = models.TextField()
    comment_by = models.ForeignKey(AppUser,on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket,on_delete= models.PROTECT, related_name = 'get_comments')
    commented_at = models.DateTimeField(auto_now_add=True,blank = True, null= True)

    class Meta:
        ordering = ['-commented_at']