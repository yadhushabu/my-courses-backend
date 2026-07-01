# My Courses

A simple Learning Management System (LMS) built using React, Django REST Framework, PostgreSQL and JWT Authentication.

## Live Demo

Frontend:
https://my-courses-frontend-seven.vercel.app/

Backend API:
https://my-courses-api-i6uz.onrender.com

## GitHub Repositories

Frontend:
https://github.com/yadhushabu/my-courses-frontend

Backend:
https://github.com/yadhushabu/my-courses-backend

---

## Tech Stack

Frontend

- React
- Vite
- React Router
- React Query
- Axios
- Tailwind CSS

Backend

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Render

Deployment

- Frontend: Vercel
- Backend: Render

---

## Features

- JWT Login
- Protected Routes
- My Courses Dashboard
- Course Details
- Study Materials
- Toggle Material Completion
- Live Classes
- Assignments
- Progress Tracking
- Search Courses
- Logout

---

## Test Credentials

### Student 1

Username:
arya_r

Password:
student123

- Enrolled in 3 courses
- Partial Progress
- Full Progress
- No Progress

### Student 2

Username:
govind_g

Password:
student123

- Enrolled in 2 courses
- Partial Progress
- No Progress

---

## Running Locally

### Backend

```bash
git clone https://github.com/yadhushabu/my-courses-backend

cd my-courses-backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

### Frontend

```bash
git clone https://github.com/yadhushabu/my-courses-frontend

cd my-courses-frontend

npm install

npm run dev
```
## Environment Variables

### Frontend

VITE_API_BASE=http://127.0.0.1:8000

### Backend

Configure PostgreSQL database settings in .env.

## API Endpoints

POST /api/token/

GET /api/courses/

GET /api/courses/:id/

POST /api/materials/:id/toggle-complete/



