from django.urls import path
from .views import MyCoursesListView, MyCourseDetailView, ToggleMaterialCompletionView

urlpatterns = [
    path('courses/', MyCoursesListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', MyCourseDetailView.as_view(), name='course-detail'),
    path('materials/<int:pk>/toggle-complete/', ToggleMaterialCompletionView.as_view(), name='toggle-material'),
]