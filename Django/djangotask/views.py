# views.py
from django.shortcuts import render
from django.db.models import Avg, Count, Q, F, FloatField
from django.db.models.functions import Substr, Cast, ExtractYear
from .models import SiteUser, Vacancy
from django.http import JsonResponse


def hello(request):
    if request.method == 'GET':
        return render(request, 'hello.html', {'name': 'пользователь'})
    elif request.method == 'POST':
        user_id = request.POST.get('id')
        user = SiteUser.objects.get(id=user_id)
        name = user.get_name()
        return render(request, 'hello.html', {'name': name})
    else:
        return JsonResponse({'error': True})


def all_vacancies(request):
    data = Vacancy.objects.all()
    return render(request, 'vacancies_table.html', {'data': data})


def filter_vacancies(request):
    vacancies = Vacancy.objects.all()

    name_start = request.GET.get('name_start')
    if name_start:
        vacancies = vacancies.filter(name__istartswith=name_start)

    salary = request.GET.get('salary')
    if salary:
        try:
            salary = float(salary)
            vacancies = vacancies.filter(salary=salary)
        except ValueError:
            pass

    city_start = request.GET.get('city_start')
    if city_start:
        vacancies = vacancies.filter(area_name__istartswith=city_start)

    return render(request, 'vacancies_table.html', {'data': vacancies})


def annotate_year(queryset):
    from django.db.models import IntegerField
    return queryset.annotate(
        year=Cast(Substr('published_at', 1, 4), output_field=IntegerField())
    )


def get_salary_year_dynamic(request):
    vacancies = Vacancy.objects.filter(salary__isnull=False, salary__gt=0)
    vacancies = annotate_year(vacancies)
    data = (
        vacancies.values('year')
        .annotate(first=Avg('salary'))
        .values('first', second=F('year'))
        .order_by('year')
    )
    return render(request, 'dynamics_table.html', {
        'first_parameter': 'Avg salary',
        'second_parameter': 'Year',
        'data': list(data)
    })


def get_count_year_dynamic(request):
    vacancies = Vacancy.objects.filter(salary__isnull=False, salary__gt=0)
    vacancies = annotate_year(vacancies)
    data = (
        vacancies.values('year')
        .annotate(first=Count('id'))
        .values('first', second=F('year'))
        .order_by('year')
    )
    return render(request, 'dynamics_table.html', {
        'first_parameter': 'Count',
        'second_parameter': 'Year',
        'data': list(data)
    })


def get_top_10_salary_city(request):
    total_count = Vacancy.objects.filter(salary__isnull=False, salary__gt=0).count()
    if total_count == 0:
        data = []
    else:
        city_stats = (
            Vacancy.objects.filter(salary__isnull=False, salary__gt=0)
            .values('area_name')
            .annotate(
                avg_salary=Avg('salary'),
                city_count=Count('id')
            )
        )
        data = []
        for item in city_stats:
            percentage = (item['city_count'] * 100.0) / total_count
            if percentage > 1:
                data.append({
                    'first': item['avg_salary'],
                    'second': item['area_name']
                })
        data.sort(key=lambda x: x['first'])
        data = data[:10]

    return render(request, 'dynamics_table.html', {
        'first_parameter': 'Avg salary',
        'second_parameter': 'City',
        'data': data
    })


def get_top_10_vac_city(request):
    total_count = Vacancy.objects.filter(salary__isnull=False, salary__gt=0).count()
    if total_count == 0:
        data = []
    else:
        city_stats = (
            Vacancy.objects.filter(salary__isnull=False, salary__gt=0)
            .values('area_name')
            .annotate(
                city_count=Count('id')
            )
        )
        data = []
        for item in city_stats:
            percentage = (item['city_count'] * 100.0) / total_count
            data.append({
                'first': percentage,
                'second': item['area_name']
            })
        data.sort(key=lambda x: x['first'], reverse=True)
        data = data[:10]

    return render(request, 'dynamics_table.html', {
        'first_parameter': 'Percentage',
        'second_parameter': 'City',
        'data': data
    })