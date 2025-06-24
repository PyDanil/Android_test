from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('general-stats/', views.general_stats, name='general_stats'),
    path('demand/', views.demand, name='demand'),
    path('geography/', views.geography, name='geography'),
    path('skills/', views.skills, name='skills'),
    path('latest-vacancies/', views.latest_vacancies, name='latest_vacancies'),
]