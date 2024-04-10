from django.urls import path
from . import views

app_name = "gateway"

urlpatterns = [
    path('', views.ListGateways, name="listgateways"),
    path("add/", views.AddGateway, name="addgateway"),
    path("state/<int:id>/", views.EditGateway, name="editgateway"),
    path("delete/<int:id>/", views.DeleteGateway, name="deletegateway"),
    path("details/<str:id>/", views.GetGatewayDetails, name="getgatewaydetails"),
]