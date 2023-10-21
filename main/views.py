from io import StringIO

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm as BaseCreate
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login

import paramiko

from .models import User, Box

# Create your views here.

class UserCreationForm(BaseCreate):
    class Meta:
        model = User
        fields = BaseCreate.Meta.fields


class HomePageView(TemplateView):
    template_name = 'home.html'

class UserCreationView(FormView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = "/boxes/"   
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        

class BoxList(LoginRequiredMixin, ListView):
    model = Box
    template_name = 'box_list.html'
    context_object_name = 'boxes'

    def get_queryset(self):
        return Box.objects.filter(user=self.request.user)
    

class BoxCreate(LoginRequiredMixin, CreateView):
    model = Box
    fields = ("name",)
    template_name = "form_base.html"
    success_url = reverse_lazy("box_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        key = paramiko.RSAKey.generate(4096)
        form.instance.public_key = key.get_base64()
        temp_str = StringIO()
        key.write_private_key(temp_str)
        temp_str.seek(0)
        form.instance.private_key = temp_str.read()
        return super().form_valid(form)

class BoxDelete(DeleteView):
    model = Box
    success_url = reverse_lazy("box_list")   
    context_object_name = "box"
    template_name = "confirm.html"
    
    def get_queryset(self):
        return Box.objects.filter(user=self.request.user)
  
