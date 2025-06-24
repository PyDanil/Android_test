from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

class Profession(models.Model):
    """Модель для главной страницы (описание профессии)"""
    title = models.CharField('Заголовок', max_length=200, db_index=True)
    slug = models.SlugField('URL-адрес', max_length=100, unique=True, blank=True)
    description = models.TextField(
        'Описание профессии',
        validators=[MinLengthValidator(10)]
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("main:profession_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProfessionImage(models.Model):
    """Изображения для профессии"""
    profession = models.ForeignKey(
        Profession, 
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Профессия'
    )
    image = models.ImageField('Изображение', upload_to='profession_images/%Y/%m/%d')
    description = models.CharField('Описание изображения', max_length=255, blank=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Изображение профессии'
        verbose_name_plural = 'Изображения профессии'

    def __str__(self):
        return f"Изображение для {self.profession.title}"

class YearStatistic(models.Model):
    """Статистика по годам"""
    year = models.IntegerField('Год', unique=True)
    avg_salary = models.FloatField('Средняя зарплата (руб)')
    vacancy_count = models.IntegerField('Количество вакансий')
    avg_salary_android = models.FloatField(
        'Средняя зарплата Android (руб)', 
        null=True, 
        blank=True
    )
    vacancy_count_android = models.IntegerField(
        'Количество вакансий Android', 
        null=True, 
        blank=True
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Статистика по годам'
        verbose_name_plural = 'Статистика по годам'

    def __str__(self):
        return f"Статистика за {self.year} год"

class CityStatistic(models.Model):
    """Статистика по городам"""
    city = models.CharField('Город', max_length=100, unique=True)
    slug = models.SlugField('URL-адрес', max_length=100, unique=True, blank=True)
    avg_salary = models.FloatField('Средняя зарплата (руб)')
    vacancy_share = models.FloatField('Доля вакансий (%)')
    avg_salary_android = models.FloatField(
        'Средняя зарплата Android (руб)', 
        null=True, 
        blank=True
    )
    vacancy_share_android = models.FloatField(
        'Доля вакансий Android (%)', 
        null=True, 
        blank=True
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ('-avg_salary',)
        verbose_name = 'Статистика по городам'
        verbose_name_plural = 'Статистика по городам'

    def __str__(self):
        return self.city
    
    def get_absolute_url(self):
        return reverse("main:city_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city)
        super().save(*args, **kwargs)

class Skill(models.Model):
    """Навыки по годам"""
    name = models.CharField('Название навыка', max_length=100, db_index=True)
    slug = models.SlugField('URL-адрес', max_length=100, unique=True, blank=True)
    year = models.IntegerField('Год')
    count = models.IntegerField('Количество упоминаний')
    is_android = models.BooleanField(
        'Для Android-разработчика', 
        default=False
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-year', '-count')
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        unique_together = ('name', 'year', 'is_android')

    def __str__(self):
        return f"{self.name} ({self.year})"
    
    def get_absolute_url(self):
        return reverse("main:skill_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Vacancy(models.Model):
    """Последние вакансии"""
    title = models.CharField('Название вакансии', max_length=255, db_index=True)
    slug = models.SlugField('URL-адрес', max_length=100, unique=True, blank=True)
    description = models.TextField('Описание вакансии')
    skills = models.TextField('Навыки')
    company = models.CharField('Компания', max_length=150)
    salary = models.CharField('Оклад', max_length=100)
    region = models.CharField('Регион', max_length=100)
    published_at = models.DateTimeField('Дата публикации')
    source_id = models.CharField(
        'ID вакансии на HH',
        max_length=20, 
        unique=True
    )
    is_android = models.BooleanField(
        'Для Android-разработчика', 
        default=True
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-published_at',)
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_android']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("main:vacancy_detail", args=[self.slug])
    
    def skills_list(self):
        """Преобразует строку навыков в список"""
        return [skill.strip() for skill in self.skills.split(',')]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Vacancy.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)