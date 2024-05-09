from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm # to create new account
from django.contrib.auth.mixins import LoginRequiredMixin # to ask login whenever open the app we use LoginRequiredMixin
from django.contrib.auth import login # to enable after creating account to directly enter the account
from .models import Task



# Create your views here.
class Registerpage(FormView):
    template_name = "todoapp/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)


class Customlogin(LoginView):
    template_name="todoapp/login.html"
    fields='__all__'
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks') #after submission redirect to tasks page
    
    def get_success_url(self):
        return reverse_lazy("tasks")

class CustomLogout(LogoutView):
    next_page = reverse_lazy('login')

class Tasklist(LoginRequiredMixin,ListView):
    model = Task
    context_object_name="tasks"
    
    def get_context_data(self, **kwargs):
        #for user specific data we need to override the get_context_data
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False)
        
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        context['search_input']=search_input
        return context
    
    
    
class Taskdetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name="task"
    template_name="todoapp/task.html"
    
class Taskcreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks') #after submission redirect to tasks page
    
    def form_valid(self, form):# for default save to the current customer tasks
        form.instance.user=self.request.user
        return super(Taskcreate,self).form_valid(form)
    
    
class Taskupdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')
    
class Taskdelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy('tasks')
    
