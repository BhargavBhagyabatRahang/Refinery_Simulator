from django.urls import path
from . import views

urlpatterns = [

    path("thickness/", views.latest_thickness, name="Latest Thickness"),
    path("dcs/", views.latest_DCS, name="DCS Thickness"),
    path("lab/", views.latest_LAB, name="LAB Thickness"),
    path("simulator/",views.simulator_UI, name="simulator_UI")

]