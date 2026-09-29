from django.shortcuts import get_object_or_404, render

from .models import Course, Lesson, Submission


def exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    return render(
        request,
        "exam.html",
        {
            "lesson": lesson,
            "questions": questions,
        }
    )


def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        Submission.objects.filter(
            question__lesson=lesson
        ).delete()

        submissions = []

        for question in lesson.questions.all():
            selected_choice_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_choice_id:
                submission = Submission.objects.create(
                    question=question,
                    selected_choice_id=selected_choice_id,
                    is_correct=False
                )

                submission.is_correct = (
                    submission.selected_choice.is_correct
                )
                submission.save()

                submissions.append(submission)

        correct_answers = sum(
            submission.is_correct
            for submission in submissions
        )

        total_questions = lesson.questions.count()

        score = (
            (correct_answers / total_questions) * 100
            if total_questions else 0
        )

        return render(
            request,
            "exam_result.html",
            {
                "lesson": lesson,
                "submissions": submissions,
                "score": score,
                "correct_answers": correct_answers,
                "total_questions": total_questions,
            }
        )

    return render(
        request,
        "exam.html",
        {
            "lesson": lesson,
            "questions": lesson.questions.all(),
        }
    )


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    submissions = Submission.objects.filter(
        question__lesson__course=course
    )

    total_questions = submissions.count()
    correct_answers = submissions.filter(
        is_correct=True
    ).count()

    score = (
        (correct_answers / total_questions) * 100
        if total_questions else 0
    )

    return render(
        request,
        "exam_result.html",
        {
            "course": course,
            "submissions": submissions,
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
        }
    )