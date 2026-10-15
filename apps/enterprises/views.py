from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Enterprise
from .forms import EnterpriseForm, EnterpriseAdminForm



def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='dashboard')(view_func)


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect('dashboard')



@superuser_required
def create_enterprise(request):
    forms = EnterpriseForm()
    if request.method == 'POST':
        forms = EnterpriseForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('enterprise-list')
    context = {
        'form': forms
    }
    return render(request, 'enterprises/add_enterprise.html', context)


class EnterpriseListView(SuperuserRequiredMixin, ListView):
    model = Enterprise
    template_name = 'enterprises/enterprise_list.html'
    context_object_name = 'enterprises'
    ordering = ['-id']


@superuser_required
def edit_enterprise(request, pk):
    enterprise = get_object_or_404(Enterprise, id=pk)
    forms = EnterpriseForm(instance=enterprise)
    if request.method == 'POST':
        forms = EnterpriseForm(request.POST, instance=enterprise)
        if forms.is_valid():
            forms.save()
            return redirect('enterprise-list')
    context = {
        'form': forms,
        'enterprise': enterprise
    }
    return render(request, 'enterprises/edit_enterprise.html', context)


@superuser_required
def delete_enterprise(request, pk):
    enterprise = get_object_or_404(Enterprise, id=pk)
    enterprise.delete()
    return redirect('enterprise-list')


@superuser_required
def create_enterprise_admin(request):
    forms = EnterpriseAdminForm()
    if request.method == 'POST':
        forms = EnterpriseAdminForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('enterprise-list')
    context = {
        'form': forms
    }
    return render(request, 'enterprises/add_admin.html', context)

