from django.urls import path
from . import views


urlpatterns = [
    path("",views.adminlogin,name="adminlogin"),
    path("adminhome/",views.adminhome,name="adminhome"),
    path("adminlogout/",views.adminlogout,name="adminlogout"),
    path("admindelete/<int:id>/",views.delete,name="delete"),
    path("adminupdate/<int:id>/",views.update,name="update"),
    path("add/",views.add,name="add"),
    path("adminsearch/",views.search,name="search"),

    


]