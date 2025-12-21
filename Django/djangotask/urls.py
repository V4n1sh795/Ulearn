
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('vacancies/', views.all_vacancies, name='all_vacancies'),
    path('vacancies/filter/', views.filter_vacancies, name='filter_vacancies'),
    path('vacancies/dynamic/salary-year/', views.get_salary_year_dynamic, name='get_salary_year_dynamic'),
    path('vacancies/dynamic/count-year/', views.get_count_year_dynamic, name='get_count_year_dynamic'),
    path('vacancies/statistic/top10-salary-city/', views.get_top_10_salary_city, name='get_top_10_salary_city'),
    path('vacancies/statistic/top10-vac-city/', views.get_top_10_vac_city, name='get_top_10_vac_city'),
]
