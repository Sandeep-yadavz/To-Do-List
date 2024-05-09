from django.urls import path

from .views import Tasklist,Taskdetail,Taskcreate,Taskupdate,Taskdelete,Customlogin,CustomLogout,Registerpage


from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/',Customlogin.as_view(),name="login"),
    path('logout/',LogoutView.as_view(next_page="tasks"),name="logout"),
    path('register/',Registerpage.as_view(),name="register"),
    
    path('',Tasklist.as_view(),name="tasks"),
    path('task/<int:pk>/',Taskdetail.as_view(),name="task"),
    path('create-task/',Taskcreate.as_view(),name="create-task"),
    path('task-update/<int:pk>/',Taskupdate.as_view(),name="task-update"),
    path('task-delete/<int:pk>/',Taskdelete.as_view(),name="task-delete")
]