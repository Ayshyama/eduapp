from django import forms
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
    list_display = ('name',)
    search_fields = ['name']


class ModuleAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'subject')
    search_fields = ['name']
    list_filter = ('subject',)


class LessonAdmin(admin.ModelAdmin):
    inlines = [ExerciseInline]
    list_display = ('name', 'module')
    search_fields = ['name']
    list_filter = ('module',)


# Custom form for Exercise
class ExerciseForm(forms.ModelForm):
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keywords.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Keywords', is_stacked=False)
    )

    class Meta:
        model = Exercise
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['keywords'].initial = self.instance.keywords.all()

    def save(self, commit=True):
        exercise = super(ExerciseForm, self).save(commit=False)
        if commit:
            exercise.save()
        if exercise.pk:
            exercise.keywords.set(self.cleaned_data['keywords'])
            self.save_m2m()
        return exercise


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseForm
    inlines = [TestAnswerInline]

    def short_name(self, obj):
        return obj.name[:80]

    short_name.short_description = 'Name'

    list_display = ('id', 'short_name', 'lesson', 'is_test')
    list_display_links = ('id', 'short_name')
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
