from django.urls import path
from .views import *

urlpatterns = [
    path('new_soal/',SoalView.as_view()),
    
    ]