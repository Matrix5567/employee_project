from django.urls import path
from.views import Home,Login,Dashboard,Users,Addemployee,Saveemployee,Employeeattendence,Savingtime,Buttonstate,Totaltiming,Leavings,Reports,Reportsemployee,Pdf
from. import views




app_name = 'employeapp'

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('console',Login.as_view(),name='console'),
    path('dashboard',Dashboard.as_view(),name='dash'),
    path('employeelist',Users.as_view(),name='employeelist'),
    path("logout", views.logout_request, name="logout"),
    path("addemployee",Addemployee.as_view(),name="addemployee"),
    path("saveemployee",Saveemployee.as_view(),name="saveemployee"),
    path("employeeattendence",Employeeattendence.as_view(),name="employeeattendence"),
    path("savingtime",Savingtime.as_view() , name="savingtime"),
    path("buttonstate",Buttonstate.as_view() , name="buttonstate"),
    path("totaltimings",Totaltiming.as_view() , name="totaltimings"),
    path("leave",Leavings.as_view() , name="leave"),
    path("reportsemployee", Reportsemployee.as_view(), name="reportsemployee"),
    path("reports",Reports.as_view() , name="reports"),
    path("pdf", Pdf.as_view(),name="pdf"),



]