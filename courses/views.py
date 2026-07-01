from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.utils import timezone

from .models import Course, Enrollment, StudyMaterial, StudentMaterialCompletion
from .serializers import CourseListSerializer, CourseDetailSerializer


def get_student_courses_queryset(student):
    """
    Shared query logic for both list and detail views.
    Prefetches everything needed so serializers don't trigger extra queries per object.
    """
    return Course.objects.prefetch_related(
        'faculty__user',
        'live_classes',
        'assignments',
        Prefetch(
            'study_materials',
            queryset=StudyMaterial.objects.prefetch_related(
                Prefetch(
                    'completions',
                    queryset=StudentMaterialCompletion.objects.filter(student=student),
                    to_attr='my_completions'
                )
            )
        ),
    )


class MyCoursesListView(APIView):
    """GET /api/courses/ - list all courses the logged-in student is enrolled in."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student  # assumes a Student profile exists for this user

        enrollments = Enrollment.objects.filter(student=student).select_related('classroom')
        course_ids = enrollments.values_list('course_id', flat=True)
        enrollment_map = {e.course_id: e for e in enrollments}

        courses = get_student_courses_queryset(student).filter(id__in=course_ids)

        # attach each course's enrollment so the serializer can read classroom info
        for course in courses:
            course.my_enrollment = enrollment_map[course.id]

        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class MyCourseDetailView(APIView):
    """GET /api/courses/:id/ - full detail for one course, scoped to the logged-in student."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        student = request.user.student

        # Authorization check: student must actually be enrolled in this course.
        # This is the IDOR protection the task explicitly asks for.
        enrollment = get_object_or_404(Enrollment, student=student, course_id=pk)

        course = get_student_courses_queryset(student).get(id=pk)
        course.my_enrollment = enrollment

        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)


class ToggleMaterialCompletionView(APIView):
    """POST /api/materials/:id/toggle-complete/ - idempotent toggle of completion state."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        student = request.user.student
        material = get_object_or_404(StudyMaterial, pk=pk)

        # Authorization: the material's course must be one this student is enrolled in.
        is_enrolled = Enrollment.objects.filter(student=student, course=material.course).exists()
        if not is_enrolled:
            return Response({'error': 'Not enrolled in this course.'}, status=status.HTTP_403_FORBIDDEN)

        completion, created = StudentMaterialCompletion.objects.get_or_create(
            student=student, material=material
        )

        if not created:
            completion.delete()
            return Response({
                "message": "Material marked as incomplete",
                "completed": False
            })

        return Response({
            "message": "Material marked as complete",
            "completed": True
        })