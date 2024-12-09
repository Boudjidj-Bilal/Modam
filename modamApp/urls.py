from django.urls import path 

from modamApp import views

urlpatterns = [
    path('',views.viewFormulaire,name='pageFormulaire'),
]