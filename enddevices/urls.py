from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "endnode"

urlpatterns = [

    path('', views.EndNodes, name="endnodes"),
    path('addendnode/', views.AddEndNode, name="addendnode"),
    path("state/<int:id>/", views.EditEndnode, name="editendnode"),
    path("delete/<int:id>/", views.DeleteEndnode, name="deleteendnode"),
    path("details/<int:id>/", views.GetEndnodeDetails, name="getendnodedetails"),
    path("all/", views.GetAllEndnodesFunc, name = "allendnodesfromapi"),
    path("add/activation/<int:id>/", views.AddEndNodeActivation, name = "addendnodeactivation"),
    path("activation/<int:id>/", views.GetEndNodeActivation, name = "getendnodeactivation"),
    path("delete/activation/<int:id>/", views.DeleteEndNodeActivation, name = "deleteendnodeactivation"),

]