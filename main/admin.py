from django.contrib import admin
from .models import Profession, ProfessionImage, YearStatistic, CityStatistic, Skill, Vacancy

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProfessionImage)
class ProfessionImageAdmin(admin.ModelAdmin):
    list_display = ['profession', 'image', 'created']

@admin.register(YearStatistic)
class YearStatisticAdmin(admin.ModelAdmin):
    list_display = ['year', 'avg_salary', 'vacancy_count', 'updated']
    list_editable = ['avg_salary', 'vacancy_count']

@admin.register(CityStatistic)
class CityStatisticAdmin(admin.ModelAdmin):
    list_display = ['city', 'slug', 'avg_salary', 'vacancy_share', 'updated']
    prepopulated_fields = {'slug': ('city',)}
    list_editable = ['avg_salary', 'vacancy_share']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'year', 'count', 'is_android']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['count', 'is_android']
    list_filter = ['year', 'is_android']

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'salary', 'is_android', 'published_at']
    list_filter = ['is_android', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_android']