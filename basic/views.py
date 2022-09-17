from multiprocessing import get_context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, createForm
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from .models import Vehicle
from django.urls import reverse
from django.core.paginator import Paginator

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

    def get_context_data(self):
        context = {}
        objects = Vehicle.objects.all()
        #Pagination
        page_obj = Paginator(objects, 2)
        page = self.request.GET.get('page')
        context['objects'] = page_obj.get_page(page)
        return context


# Create a new vehicle record
class CreateView( LoginRequiredMixin, CreateView):
    premission_required = 'vehicle.add_vehicle'
    model = Vehicle
    template_name = 'basic/create.html'
    form_class = createForm

    def get_success_url(self):
        messages.success(self.request, 'Record created Successfully')
        return reverse('create')

    

# Show a perticular vehicle record
class VehicleView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'basic/detail.html'
    context_object_name = 'object'

# Edit a particular vehicle record
class VehicleEditView( LoginRequiredMixin, UpdateView):
    # permission_required = 'Vehicle.change_vehicle'
    model = Vehicle
    template_name = 'basic/edit.html'
    form_class = createForm

    def get_success_url(self):
        messages.success(self.request, 'Record Updated Successfully')
        return super().get_success_url()

# Delete a particular vehicle record 
class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    
    def get_success_url(self):
        messages.success(self.request, 'Record Deleted')
        return '/home'
    









