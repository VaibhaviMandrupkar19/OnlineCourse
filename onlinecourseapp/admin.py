from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson")
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    inlines = [QuestionInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("question", "selected_choice", "is_correct")