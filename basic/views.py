from re import template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, createForm
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from .models import Vehicle
from django.urls import reverse


#User login page with login form
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pswd = form.cleaned_data['password']
            user = authenticate(request, username = uname, password = pswd)
            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                form = LoginForm()
                messages.error(request,'Invalid username or password')
                return render(request,'basic/login.html',{'form':form})      
    else:
        context_data = {}
        context_data['form'] = LoginForm
        return render(request, 'basic/login.html', context_data)

#Home page
class homeView(LoginRequiredMixin, ListView): 
    model = Vehicle
    template_name = 'basic/home.html'

# Create a new Vehicle record
class CreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'basic/create.html'
    form_class = createForm
    def get_success_url(self):
        return reverse('create')

# Show a perticular record
class VehicleView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'basic/detail.html'
    context_object_name = 'object'







