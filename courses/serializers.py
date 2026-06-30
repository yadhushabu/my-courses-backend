from rest_framework import serializers
from .models import (
    Course, Classroom, Enrollment, LiveClass,
    StudyMaterial, Assignment, Faculty, StudentMaterialCompletion
)


class FacultySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'designation']


class LiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = ['id', 'title', 'scheduled_at', 'meeting_link']


class StudyMaterialSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = StudyMaterial
        fields = ['id', 'folder', 'title', 'file_url', 'completed']

    def get_completed(self, obj):
        # obj.my_completions is set by Prefetch in the view (no extra query here)
        return len(obj.my_completions) > 0


class AssignmentSerializer(serializers.ModelSerializer):
    display_status = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'due_date', 'status', 'display_status']

    def get_display_status(self, obj):
        labels = {
            'published': 'Pending submission',
            'submitted': 'Awaiting evaluation',
            'evaluated': 'Graded',
            'overdue': 'Overdue',
        }
        return labels.get(obj.status, obj.status)


class CourseListSerializer(serializers.ModelSerializer):
    """Used for GET /api/courses/ - lightweight, just enough for a course card."""
    classroom = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'classroom', 'progress']

    def get_classroom(self, obj):
        enrollment = obj.my_enrollment  # set in the view via Prefetch
        if enrollment.classroom:
            return enrollment.classroom.name
        return None  # not yet assigned to a classroom

    def get_progress(self, obj):
        materials = list(obj.study_materials.all())
        if not materials:
            return None  # no materials at all - distinguish from 0% progress
        completed_count = sum(1 for m in materials if len(m.my_completions) > 0)
        return round((completed_count / len(materials)) * 100)


class CourseDetailSerializer(serializers.ModelSerializer):
    """Used for GET /api/courses/:id/ - full nested data."""
    classroom = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    faculty = FacultySerializer(many=True, read_only=True)
    live_classes = LiveClassSerializer(many=True, read_only=True)
    study_materials = StudyMaterialSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'classroom', 'progress',
            'faculty', 'live_classes', 'study_materials', 'assignments'
        ]

    def get_classroom(self, obj):
        enrollment = obj.my_enrollment
        if enrollment.classroom:
            return enrollment.classroom.name
        return None

    def get_progress(self, obj):
        materials = list(obj.study_materials.all())
        if not materials:
            return None
        completed_count = sum(1 for m in materials if len(m.my_completions) > 0)
        return round((completed_count / len(materials)) * 100)