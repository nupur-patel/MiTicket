from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from core.models import AppUser
from .models import Ticket,TicketFiles,TicketComment,TicketLogs, get_country_choices,get_status, get_tool_choices,get_criticality_choices
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@login_required
def add_ticket_view(request):
    context = {}
    if request.method == "POST":
        country = request.POST.get('country')
        title = request.POST.get('title')
        issue_type = request.POST.get('issue_type')
        url = request.POST.get('url')
        tool = request.POST.get('tool')
        description = request.POST.get('description')
        urgency = request.POST.get('urgency')
        file_list = request.FILES.getlist('file')
        assign_to = request.POST.get('assign_to')
        assign_user = AppUser.objects.get(user__email = assign_to)
        ticket = Ticket.objects.create(title = title,
                description = description,
                url = url,
                criticality = urgency,
                tools = tool,
                country = country,
                complaint_by = request.AppUser,
                issue_type = issue_type,
                currently_assigned = assign_user
        )
        for obj in file_list:
            TicketFiles.objects.create(ticket = ticket,file = obj)
        
        TicketLogs.objects.create(ticket = ticket,
            change_by = request.AppUser,
            status = ticket.current_status,
            change_msg = 'Ticket Created'
        )

        send_email(type = 'Created',ticket_id=ticket.id)
        return HttpResponseRedirect('/home/')

    users = AppUser.objects.all()
    context['users'] = users
    context['tool_dropdown'] = get_tool_choices()
    context['criticality_dropdown'] = get_criticality_choices()
    context['country_dropdown'] = get_country_choices()
    return render(request,template_name='add_ticket.html',context = context)

@login_required
def home_view(request):
    tickets = Ticket.objects.all()
    context = {}
    context['tickets'] = tickets
    return render(request,template_name = 'home.html',context = context)

@login_required
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        appuser = request.AppUser
        ticket_id = data.get("ticket_id", None) 
        comment = data.get("comment", None)
        TicketComment.objects.create(message = comment,ticket = Ticket.objects.get(id = ticket_id),comment_by = appuser)
        return HttpResponse(status=201)
    
    else:
        return HttpResponse(status = 400)


@login_required
@csrf_exempt
def chagne_status(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        appuser = request.AppUser
        ticket_id = data.get('ticket_id',None)
        status = data.get('status',None)
        obj = Ticket.objects.get(id = ticket_id)
        obj.current_status = status
        obj.save()
        ticket = Ticket.objects.get(id = ticket_id)
        add_to_log(request,ticket = ticket,message = 'Status Changed To ' + status)

        return HttpResponse(status = 201)
    else:
        return HttpResponse(status = 400)

@login_required
@csrf_exempt
def resend_email(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        appuser = request.AppUser
        ticket_id = data.get('ticket_id',None)
        ticket_obj = Ticket.objects.get(id = ticket_id)
        add_to_log(request,ticket = ticket_obj,message = 'Send reminder email for this ticket.')
        # find users and send email
        return HttpResponse(status = 201)
    else:
        return HttpResponse(status = 400)

@login_required
@csrf_exempt
def add_to_archive(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        appUser = request.AppUser
        ticket_id = data.get('ticket_id',None)
        message = data.get('title',None)
        ticket_obj = Ticket.objects.get(id = ticket_id)
        if message == 'archive':
            ticket_obj.is_archived = True
            add_to_log(request,ticket = ticket_obj,message = 'Ticket Archived')
        else:
            ticket_obj.is_archived = False
            add_to_log(request,ticket = ticket_obj,message = 'Ticket UnArchived')
        ticket_obj.save()

        return HttpResponse(status = 201)
    else:
        return HttpResponse(status = 400)

@login_required
def ticket_detail(request,id):
    TicketObj = Ticket.objects.get(id = id)
    context = {}
    context['ticket'] = TicketObj
    context['status_dropdown'] = get_status()
    return render(request,template_name='detail_ticket.html',context = context)


@login_required
def edit_ticket(request,id):
    template_name = 'edit_ticket.html'
    ticket_obj = Ticket.objects.get(id = id)
    context = {}
    context['ticket'] = ticket_obj
    context['country_dropdown'] = get_country_choices()
    context['tool_dropdown'] = get_tool_choices()
    context['criticality_dropdown'] = get_criticality_choices()
    context['status_dropdown'] = get_status()
    users = AppUser.objects.all()
    context['users'] = users
    if request.method == 'POST':
        ticket_obj = Ticket.objects.get(id = id)
        country = request.POST.get('country')
        status = request.POST.get('status')
        title = request.POST.get('title')
        issue_type = request.POST.get('issue_type')
        url = request.POST.get('url')
        tool = request.POST.get('tool')
        assign_to = request.POST.get('assign_to')
        description = request.POST.get('description')
        urgency = request.POST.get('urgency')
        file_list = request.FILES.getlist('file')
        if ticket_obj.country != country:
            ticket_obj.country = country
        if ticket_obj.tools != tool:
            ticket_obj.tools = tool
        if ticket_obj.title != title:
            ticket_obj.title = title
        if ticket_obj.url != url:
            ticket_obj.url = url
        if ticket_obj.criticality != urgency:
            ticket_obj.criticality = urgency
        if ticket_obj.current_status != status:
            ticket_obj.current_status = status
        if ticket_obj.issue_type != issue_type:
            ticket_obj.issue_type = issue_type
        if ticket_obj.description != description:
            ticket_obj.description = description
        if ticket_obj.currently_assigned.user.email != assign_to:
            appuser = AppUser.objects.get(user__email = assign_to)
            ticket_obj.currently_assigned = appuser        
        ticket_obj.save()
        add_to_log(request,ticket = ticket_obj,message = 'Ticket Edited')
        for obj in file_list:
            TicketFiles.objects.create(ticket = ticket_obj,file = obj)        
    return render(request,template_name=template_name,context = context)



@login_required
def archvie_view(request):
    template_name = 'archive_view.html'
    ticket_objs = Ticket.objects.all()#filter(is_archived = True)
    context = {}
    context['tickets'] = ticket_objs
    return render(request, template_name=template_name,context = context)

def send_email(type,ticket_id):
    print(type)
    print(ticket_id)

def add_to_log(request,ticket,message,user=None):
    if user == None:
        user = request.AppUser

    TicketLogs.objects.create(ticket = ticket,
        change_by = user,
        status = ticket.current_status,
        change_msg = message,
    )
