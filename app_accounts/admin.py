from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from app_accounts.models import CustomUser
from app_exercises.models import Exercise


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_display_links = ('id', 'email', 'username')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login', 'display_image', 'exercises_done_links')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'display_image', 'image')}),
        ('Progress Info', {'fields': ('life', 'day_streak', 'exercises_done_links')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height:200px;" />', obj.image.url)
        return ""

    display_image.short_description = "Profile Image"

    def exercises_done_links(self, obj):
        header = '<tr><th>ID</th><th>Name</th><th>Lesson</th><th>Module</th><th>Subject</th><th>Actions</th></tr>'
        rows = []
        for exercise in obj.exercises_done.select_related('lesson', 'lesson__module', 'lesson__module__subject').all():
            lesson = exercise.lesson
            module = lesson.module
            subject = module.subject
            exercise_url = reverse('admin:app_exercises_exercise_change', args=[exercise.id])
            remove_url = reverse('admin:app_accounts_customuser_remove_exercise', args=[obj.id, exercise.id])
            row = f'<tr><td>{exercise.id}</td><td><a href="{exercise_url}">{exercise.name}</a></td><td>{lesson.name}</td><td>{module.name}</td><td>{subject.name}</td><td><a href="{remove_url}">Remove</a></td></tr>'
            rows.append(row)
        return format_html('<table>' + header + ''.join(rows) + '</table>')

    exercises_done_links.short_description = 'Exercises Done'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('exercises_done__lesson__module__subject')
        return queryset

    # Custom view to handle the removal of an exercise
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'remove-exercise/<int:user_id>/<int:exercise_id>/',
                self.admin_site.admin_view(self.remove_exercise),
                name='app_accounts_customuser_remove_exercise'
            ),
        ]
        return custom_urls + urls

    def remove_exercise(self, request, user_id, exercise_id):
        user = CustomUser.objects.get(pk=user_id)
        exercise = Exercise.objects.get(pk=exercise_id)
        user.exercises_done.remove(exercise)
        user.save()
        return redirect('..')
