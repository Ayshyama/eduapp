from django.contrib import admin
from .models import Subject, Module, Lesson, Exercise, Keywords, TestAnswer


# Inline classes
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


class TestAnswerInline(admin.TabularInline):
    model = TestAnswer
    extra = 1


# Admin classes
class SubjectAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ('name', 'description')
    search_fields = ['name']


class ModuleAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'description', 'subject')
    search_fields = ['name']
    list_filter = ('subject',)


class LessonAdmin(admin.ModelAdmin):
    inlines = [ExerciseInline]
    list_display = ('name', 'description', 'module')
    search_fields = ['name']
    list_filter = ('module',)


class ExerciseAdmin(admin.ModelAdmin):
    inlines = [TestAnswerInline]
    list_display = ('name', 'lesson', 'is_test')
    search_fields = ['name']
    list_filter = ('lesson', 'is_test')


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('keyword',)
    search_fields = ['keyword']


class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ('name', 'exercise', 'is_correct')
    search_fields = ['name']
    list_filter = ('exercise', 'is_correct')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(TestAnswer, TestAnswerAdmin)
