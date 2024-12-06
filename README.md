# Advanced Django RBAC Authentication System

## Project Overview

This project implements a robust, feature-rich authentication and authorization system leveraging Django Rest Framework, SimpleJWT, Celery, Redis, and a custom Role-Based Access Control (RBAC) implementation.

### Key Unique Features
- Two-Factor Authentication (2FA) with OTP
- Granular Role-Based Access Control (RBAC)
- Dynamic RBAC Permission Mapping
- Frontend-Friendly RBAC Data Transmission
- Asynchronous Task Processing with Celery
- Secure Token-Based Authentication
- Secure Password Hashing using Argon2 for protection against modern GPU based attacks

## System Architecture

### Authentication Flow
1. User Registration
2. OTP-Based Login
3. JWT Token Generation
4. RBAC Permissions Mapping

### RBAC Implementation
Our RBAC system goes beyond traditional Django permissions by:
- Providing dynamic, granular access control
- Transmitting complete permission structure to frontend
- Supporting complex permission scenarios

## Installation Guide

### Prerequisites
- Python 3.9+
- Redis
- Virtual Environment

### Setup Steps

1. Clone the Repository
```bash
git clone https://github.com/ranjeetsinh/rbac_vrv.git
cd rbac_project
```

2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Configure Environment Variables
Create a `.env` file with:
```
configure the env file as per requiremnents
```

5. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create Permissions and Groups
   Use shell to run the create_groups_and_permissions() function from add_permissions.py 
```bash
python manage.py shell
```

7. Run Celery Worker
```bash
celery -A your_project_name worker -l info
```

8. Run Redis
```bash
redis-server
```

9. Start Django Development Server
```bash
python manage.py runserver
```

## RBAC Permission Structure

### Frontend RBAC Response Example
```json
{
  "rbac": {
    "tasks": {
      "task_list": {
        "view": true,
        "add": false,
        "change": false,
        "delete": false
      }
    },
    "profile": {
      "profile_details": {
        "view": true,
        "edit": false
      }
    }
  }
}
```

### Backend Permission Mapping
```python
PAGE_SECTION_ACCESS_MAP = {
    'tasks': {
        'task_list': {
            'view': 'task.can_view_tasks',
            'add': 'task.can_create_tasks',
            'change': 'task.can_edit_tasks',
            'delete': 'task.can_delete_tasks'
        }
    },
    'profile': {
        'profile_details': {
            'view': 'user.can_view_profile_details',
            'edit': 'user.can_edit_profile_details'
        }
    }
}
```

## Security Practices

1. Two-Factor Authentication
2. JWT Token-Based Authentication
3. Permission-Level Access Control
4. OTP-Based Login
5. Secure Password Hashing using Argon2 for protection against modern GPU based attacks
6. Rate Limiting
7. Custom Throttling for login
8. Authentication logging
9. CORS Protection

## Advanced RBAC Unique Aspects

### Dynamic Permission Mapping
- Supports complex, nested permission structures
- Easily extensible for new features
- Frontend-Friendly permission representation

### Flexible Group-Based Permissions
- Admin, Manager, User role hierarchies
- Granular control over actions
- Easy to modify and expand


## Monitoring and Logging

- Integrated Logging Mechanisms
- Celery Task Monitoring
- Authentication Event Tracking


## Contact
ranjeetsinhjagdale10@gmail.com
https://www.linkedin.com/in/ranjeetsinh-jagdale-6159b3237/
