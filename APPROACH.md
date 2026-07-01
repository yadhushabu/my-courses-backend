
---

# APPROACH.md

```md
# Approach

## Understanding the task

The goal was to build a small Learning Management System where a student can securely log in, view only their enrolled courses, access course details, and mark study materials as completed. The application also needed authentication, authorization, progress tracking, and a live deployment.

---

## Data Modelling

The application models the following entities:

- Student
- Faculty
- Course
- Classroom
- Enrollment
- Study Material
- Live Class
- Assignment
- Student Material Completion

A student can enroll in multiple courses, and each course can contain multiple study materials, assignments, and live classes. Progress is calculated dynamically from completed study materials instead of storing a separate progress value.

---

## Key Decisions

- Used Django REST Framework with JWT Authentication.
- Used PostgreSQL as the production database.
- Used React Query for server-state management.
- Used Axios interceptors to automatically attach JWT tokens.
- Added protected routes so unauthenticated users cannot access course pages.
- Calculated progress dynamically from completed materials.
- Added a search feature to improve usability.

---

## Trade-offs

To keep the project focused, I chose not to implement:

- File uploads
- Pagination
- Admin analytics
- Course thumbnail uploads
- Notifications
- User profile management

The interface is intentionally simple and prioritizes functionality over advanced UI.

---

## Future Improvements

With more time I would add:

- Search and filtering from the backend
- Pagination
- Course thumbnails
- Profile page
- Assignment submission
- Email notifications
- Better dashboard analytics
- Responsive improvements for mobile devices