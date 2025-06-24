from django.shortcuts import render

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

    