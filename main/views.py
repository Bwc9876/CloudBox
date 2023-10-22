from io import StringIO

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm as BaseCreate
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login
from django.conf import settings

import paramiko

from .models import User, Box
from .gcp_api import create, delete


class FormNameMixin(ContextMixin):
    form_name = "Form"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super(FormNameMixin, self).get_context_data(**kwargs)
        context["formName"] = self.form_name
        return context


class UserCreationForm(BaseCreate, FormNameMixin):
    class Meta:
        model = User
        fields = BaseCreate.Meta.fields


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class ContactPageView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["emails"] = ("BC1016579", "HC946859", "MK1020769", "EW1023319")

        return context


class UserCreationView(FormView, FormNameMixin):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    form_name = "Register"
    success_url = "/boxes/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class BoxList(LoginRequiredMixin, ListView):
    model = Box
    template_name = "box_list.html"
    context_object_name = "boxes"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context

    def get_queryset(self):
        return Box.objects.filter(user=self.request.user)


class BoxCreate(LoginRequiredMixin, CreateView, FormNameMixin):
    model = Box
    fields = ("name",)
    template_name = "form_base.html"
    success_url = reverse_lazy("box_list")
    form_name = "New Box"

    def form_valid(self, form):
        form.instance.user = self.request.user
        key = paramiko.RSAKey.generate(4096)
        form.instance.public_key = f"{key.get_name()} {key.get_base64()}"
        temp_str = StringIO()
        key.write_private_key(temp_str)
        temp_str.seek(0)
        form.instance.private_key = temp_str.read()

        form.instance.ip = create(f"C:{self.request.user.username}-{form.instance.name}", form.instance.public_key)
        return super().form_valid(form)


class BoxDelete(DeleteView):
    model = Box
    success_url = reverse_lazy("box_list")
    context_object_name = "box"
    template_name = "confirm.html"
    
    def delete(self, request, *args, **kwargs):
        box = self.get_object()
        delete(f"C:{box.user.username}-{box.name}")
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Box.objects.filter(user=self.request.user)
