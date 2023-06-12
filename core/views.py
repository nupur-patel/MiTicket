from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http.response import HttpResponse, HttpResponseRedirect

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            HttpResponseRedirect('/home/')
        else:
            return render(request, template_name='login.html',context = {'error_msg':'Invalid username or password'})

    return render(request, template_name='login.html',context = {})

def add_ticket_view(request):
    return render(request,template_name='login.html',context = {})
