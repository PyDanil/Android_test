from django.shortcuts import render
import requests
from .models import Skill
from .models import CityStatistic
from .models import YearStatistic
from datetime import datetime, timedelta
from django.core.cache import cache  # Добавляем импорт cache
from django.conf import settings

def home(request):
    # Статическое описание профессии
    profession_title = "Android-разработчик"
    profession_description = """
    <p>Android-разработчик — это специалист по созданию мобильных приложений для операционной системы Android. 
    Эта профессия находится на стыке дизайна и программирования, требуя как технических навыков, так и понимания 
    пользовательского опыта.</p>
    
    <h3>Основные обязанности:</h3>
    <ul>
        <li>Разработка архитектуры мобильного приложения</li>
        <li>Написание чистого и поддерживаемого кода на Kotlin/Java</li>
        <li>Интеграция с backend-сервисами и API</li>
        <li>Тестирование и отладка приложений</li>
        <li>Оптимизация производительности приложения</li>
        <li>Следование принципам Material Design</li>
    </ul>
    
    <h3>Необходимые навыки:</h3>
    <ul>
        <li>Знание Kotlin и Java</li>
        <li>Опыт работы с Android SDK</li>
        <li>Понимание жизненного цикла Activity и Fragment</li>
        <li>Работа с базами данных (Room, SQLite)</li>
        <li>Знание популярных библиотек (Retrofit, Dagger/Hilt, Coroutines)</li>
        <li>Опыт работы с Git</li>
    </ul>
    
    <p>Средняя зарплата Android-разработчика в России варьируется от 120 000 до 250 000 рублей в зависимости 
    от опыта и региона. Профессия остается востребованной благодаря постоянному росту мобильного рынка 
    и увеличению количества Android-устройств.</p>
    """
    
    # Путь к статическому изображению (добавьте свое изображение в static/main/img/android_dev.jpg)
    image_url = "main/img/android_dev.jpg"
    image_description = "Андроидик"
    
    context = {
        'profession_title': profession_title,
        'profession_description': profession_description,
        'image_url': image_url,
        'image_description': image_description,
    }
    return render(request, 'main/home.html', context)

def general_stats(request):
    # Общая статистика
    years = YearStatistic.objects.all().order_by('year')
    cities_salary = CityStatistic.objects.all().order_by('-avg_salary')[:10]
    cities_share = CityStatistic.objects.all().order_by('-vacancy_share')[:10]
    skills = Skill.objects.filter(is_android=False).order_by('-year', '-count')[:20]
    
    # Подготовка данных для графиков
    years_labels = [str(y.year) for y in years]
    salary_data = [y.avg_salary for y in years]
    vacancy_data = [y.vacancy_count for y in years]
    
    cities_labels = [c.city for c in cities_salary]
    cities_salary_data = [c.avg_salary for c in cities_salary]
    cities_share_data = [c.vacancy_share for c in cities_share]
    
    context = {
        'years': years,
        'cities_salary': cities_salary,
        'cities_share': cities_share,
        'skills': skills,
        'years_labels': years_labels,
        'salary_data': salary_data,
        'vacancy_data': vacancy_data,
        'cities_labels': cities_labels,
        'cities_salary_data': cities_salary_data,
        'cities_share_data': cities_share_data,
    }
    return render(request, 'main/general_stats.html', context)

def demand(request):
    # Востребованность (для Android)
    years = YearStatistic.objects.all().order_by('year')
    
    # Подготовка данных для графиков
    years_labels = [str(y.year) for y in years]
    salary_data = [y.avg_salary_android for y in years]
    vacancy_data = [y.vacancy_count_android for y in years]
    
    context = {
        'years': years,
        'years_labels': years_labels,
        'salary_data': salary_data,
        'vacancy_data': vacancy_data,
    }
    return render(request, 'main/demand.html', context)

def geography(request):
    # География (для Android)
    cities_salary = CityStatistic.objects.exclude(avg_salary_android=None).order_by('-avg_salary_android')[:10]
    cities_share = CityStatistic.objects.exclude(vacancy_share_android=None).order_by('-vacancy_share_android')[:10]
    
    # Подготовка данных для графиков
    cities_labels = [c.city for c in cities_salary]
    cities_salary_data = [c.avg_salary_android for c in cities_salary]
    cities_share_data = [c.vacancy_share_android for c in cities_share]
    
    context = {
        'cities_salary': cities_salary,
        'cities_share': cities_share,
        'cities_labels': cities_labels,
        'cities_salary_data': cities_salary_data,
        'cities_share_data': cities_share_data,
    }
    return render(request, 'main/geography.html', context)

def skills(request):
    # Навыки (для Android)
    skills = Skill.objects.filter(is_android=True).order_by('-year', '-count')[:20]
    
    # Группировка по годам
    skills_by_year = {}
    for skill in skills:
        if skill.year not in skills_by_year:
            skills_by_year[skill.year] = []
        skills_by_year[skill.year].append(skill)
    
    context = {
        'skills_by_year': skills_by_year,
    }
    return render(request, 'main/skills.html', context)

def latest_vacancies(request):
    # Проверяем, включен ли режим DEBUG для использования кэша
    use_cache = not settings.DEBUG  # В DEBUG-режиме кэш отключаем для удобства разработки
    
    if use_cache:
        vacancies = cache.get('hh_vacancies_cache')
        if vacancies:
            context = {'vacancies': vacancies}
            return render(request, 'main/latest_vacancies.html', context)
    
    # Параметры запроса к API HH
    params = {
        'text': 'Android разработчик',
        'search_field': 'name',
        'per_page': 10,
        'order_by': 'publication_time',
        'date_from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    }
    
    try:
        # Получаем список вакансий
        response = requests.get('https://api.hh.ru/vacancies', params=params, timeout=10)
        response.raise_for_status()  # Проверяем на ошибки HTTP
        vacancies_data = response.json().get('items', [])[:10]
        
        vacancies = []
        for item in vacancies_data:
            try:
                # Дополнительный запрос для получения полного описания
                vacancy_response = requests.get(
                    f'https://api.hh.ru/vacancies/{item["id"]}',
                    timeout=5
                )
                vacancy_response.raise_for_status()
                vacancy_details = vacancy_response.json()
                
                # Обработка зарплаты
                salary = vacancy_details.get('salary')
                salary_str = "Не указана"
                if salary:
                    if salary.get('from') and salary.get('to'):
                        salary_str = f"{salary['from']} - {salary['to']} {salary['currency']}"
                    elif salary.get('from'):
                        salary_str = f"от {salary['from']} {salary['currency']}"
                    elif salary.get('to'):
                        salary_str = f"до {salary['to']} {salary['currency']}"
                
                # Обработка навыков
                skills = [skill['name'] for skill in vacancy_details.get('key_skills', [])]
                
                # Форматирование даты
                published_at = datetime.strptime(
                    item['published_at'], 
                    '%Y-%m-%dT%H:%M:%S%z'
                ).strftime('%d.%m.%Y %H:%M')
                
                # Внутри функции latest_vacancies, где формируем вакансии:
                vacancies.append({
                    'title': vacancy_details.get('name', 'Без названия'),
                    'description': vacancy_details.get('description', 'Описание отсутствует'),
                    'skills': skills,  # Это уже список, а не строка
                    'company': vacancy_details.get('employer', {}).get('name', 'Компания не указана'),
                    'salary': salary_str,
                    'region': vacancy_details.get('area', {}).get('name', 'Регион не указан'),
                    'published_at': published_at,
                    'url': vacancy_details.get('alternate_url', '#'),
                })
            except Exception as e:
                print(f"Ошибка обработки вакансии {item.get('id')}: {str(e)}")
                continue
        
        if use_cache:
            cache.set('hh_vacancies_cache', vacancies, timeout=3600)  # Кэшируем на 1 час
        
        context = {'vacancies': vacancies}
        return render(request, 'main/latest_vacancies.html', context)
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API HH: {str(e)}")
        error_message = "Не удалось загрузить данные. Попробуйте обновить страницу позже."
        return render(request, 'main/latest_vacancies.html', {'error': error_message})