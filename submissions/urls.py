from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_code, name='submit_code'),
    path('result/<int:pk>/', views.submission_result, name='submission_result'),
    path('history/', views.submission_history, name='submission_history'),
]
