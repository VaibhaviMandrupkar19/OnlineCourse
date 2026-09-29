from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Lesson, Enrollment, Submission, Choice


def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.question_set.all()

    return render(
        request,
        "exam.html",
        {
            "course": course,
            "questions": questions,
        }
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    enrollment = Enrollment.objects.get(
        user=user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_choices = []

    for key in request.POST:
        if key.startswith("choice"):
            choice_id = request.POST[key]
            selected_choices.append(int(choice_id))

    choices = Choice.objects.filter(
        id__in=selected_choices
    )

    submission.choices.set(choices)

    return HttpResponseRedirect(
        reverse(
            "show_exam_result",
            args=(course_id, submission.id)
        )
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        id=course_id
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    choices = submission.choices.all()

    total_score = 0

    for choice in choices:
        if choice.is_correct:
            total_score += choice.question.grade

    return render(
        request,
        "exam_result.html",
        {
            "course": course,
            "grade": total_score,
            "choices": choices,
        }
    )