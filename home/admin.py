from django.contrib import admin
from . import models

# Register your models here.
from django.contrib import admin
from .models import User, Student, Mentor, Lesson, Parent, Relationship


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('username',
                     'email',
                     'relationships__child__user__username',
                     'relationships__child__user__email',
                     'relationships__mentor__user__username',
                     'relationships__mentor__user__email')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number')
    search_fields = ('user__username', 'user__email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'parent')
    list_filter = ('parent',)
    search_fields = ('user__username',
                     'user__email',
                     'parent__user__username',
                     'parent__user__email')


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'area_of_expertise')
    search_fields = ('user__username', 'user__email')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'student', 'start_time', 'end_time')
    list_filter = ('mentor', 'student')
    search_fields = ('mentor__user__username',
                     'child__user__username')


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('mentor_id', 'student_id')
    search_fields = ('mentor_id', 'student_id')