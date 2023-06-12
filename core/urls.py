from django.urls import path
from core.views import *
urlpatterns = [
    path('login/',login_view,name = 'login'),
    # path('add_ticket/',add_ticket_view,name = 'add-ticket'),
]
