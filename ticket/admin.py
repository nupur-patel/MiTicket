from django.contrib import admin
from .models import Ticket, TicketFiles,TicketComment,TicketLogs
# Register your models here.

admin.site.register(Ticket)
admin.site.register(TicketFiles)
admin.site.register(TicketComment)
admin.site.register(TicketLogs)