from django.urls import path
from.views import Home,Login,Dashboard,Users,Addemployee
from. import views




app_name = 'employeapp'

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('console',Login.as_view(),name='console'),
    path('dashboard',Dashboard.as_view(),name='dash'),
    path('employeelist',Users.as_view(),name='employeelist'),
    path("logout", views.logout_request, name="logout"),
    path("addemployee",Addemployee.as_view(),name="addemployee")

]