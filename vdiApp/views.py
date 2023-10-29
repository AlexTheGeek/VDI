# vm_management/views.py
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .models import Template, VM, User
from django.contrib.auth.forms import AuthenticationForm #add this
import test


url = []
conn = test.conn


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/student/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


@login_required
def admin_page(request):
    templates = Template.objects.all()
    vms = VM.objects.all()
    
    if request.method == 'POST':
        if 'create_template' in request.POST:
            template_name = request.POST.get('template_name')
            template_description = request.POST.get('template_description')
            template = Template.objects.create(name=template_name, description=template_description)
            messages.success(request, 'Le Template a été créé avec succès.')

        elif 'create_vm' in request.POST:
            vm_name = request.POST.get('vm_name')
            vm_template_id = request.POST.get('template')
            vm_template = Template.objects.get(id=vm_template_id)
            vm = VM.objects.create(name=vm_name, template=vm_template, templat_id=vm_template_id)
            test.create_instance(conn, vm_name, vm_template)
            messages.success(request, 'La VM a été créée avec succès.')

        elif 'start_vm' in request.POST:
            vm_name = request.POST.get('vm_name')
            print(f"Starting {vm_name}")
            #envoyer sur une page en mode "chargement vm"
            test.create_instance(conn, vm_name, vm_image="kali")
            url.append(test.get_console_url(conn, vm_name))
            #envoyer sur VNC
            return redirect("console_page")
        
        elif 'remove_vm' in request.POST:
            vm_name = request.POST.get('vm_name')
            print(f'Removing {vm_name}')
            test.remove_instance(conn, vm_name)
            vm_to_remove = VM.objects.get(name=vm_name)
            vm_to_remove.remove_vm()

        return redirect("admin_page")
    
    return render(request, 'admin_page.html', {'templates': templates, 'vms': vms})


@login_required
def professor_page(request):
    templates = Template.objects.all()
    vms = VM.objects.all()

    return render(request, 'professor_page.html', {'templates': templates, 'vms': vms})

@login_required
def student_page(request):
    
    is_authenticated = request.user.is_authenticated
    first_name = request.user.first_name
    last_name = request.user.last_name
    
    context = {
        'is_authenticated': is_authenticated,
    }
    
    templates = Template.objects.all()
    vms = VM.objects.all()

    if request.method == "POST":
        if 'instance_vm' in request.POST:
            print(request.POST)
            vm_name = request.POST.get('vm_name')
            vm_template_id = request.POST.get('template')
            vm_template = Template.objects.get(id=vm_template_id)
            existing_vm = VM.objects.filter(template_id=vm_template_id).first()

            if existing_vm:
                print(f"Une VM existe déjà pour le template {existing_vm.template.name}")
            else:
                vm = VM.objects.create(name=vm_name, template=vm_template, templat_id=vm_template_id)
                messages.success(request, 'La VM a été instanciée avec succès.')
                print(f"Instance de {vm_name} en utilisant le modèle {vm_template.name}")

        elif 'start_vm' in request.POST:
            print(request.POST)
            vm_name = request.POST.get('vm_name')
            print(f"Starting {vm_name}")

        context = {
            'templates': templates, 
            'vms': vms,
            'is_authenticated': is_authenticated,
            'user_last_name': last_name,
            'user_first_name': first_name,
        }

        return redirect('student_page')
    
    return render(request, 'student_page.html', context)

@login_required
def data_page(request):
    vms = VM.objects.all()
    templates = Template.objects.all()
    users = User.objects.all()

    template_data = [{'name': template.name, 'id': template.id, 'description': template.description} for template in templates]
    vm_data = [{'name': vm.name, 'id': vm.id, 'template': vm.template.name, 'template_id': vm.templat_id, 'created_at': vm.created_at, 'last_interaction': vm.last_interaction} for vm in vms]
    user_data = [{'name': user.name, 'id': user.id, 'email': user.email} for user in users]
    data_json = {'templates': template_data, 'vms': vm_data}

    return JsonResponse(data_json)

@login_required
def console_page(request):
    return redirect(url.pop())