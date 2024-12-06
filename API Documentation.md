# User Management API Documentation

## Authentication Workflow

### 1. User Registration
- **Endpoint**: `/api/register/`
- **Method**: POST
- **Request Body**:
```json
{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "strongpassword123"
}
```
- **Response**:
  - 201: User created successfully
  - 400: Validation error

### 2. Login OTP Workflow
#### Send OTP
- **Endpoint**: `/api/login/`
- **Method**: POST
- **Request Body**:
```json
{
    "email": "johndoe@example.com"
}
```

#### Verify OTP
- **Endpoint**: `/api/verify-otp/`
- **Method**: POST
- **Request Body**:
```json
{
    "email": "johndoe@example.com",
    "otp": "123456"
}
```
- **Response**:
  - JWT Tokens
  - User RBAC Permissions
  - User Role

### 3. Token Management
#### Refresh Token
- **Endpoint**: `/api/refresh-token/`
- **Method**: POST
- **Request Body**:
```json
{
    "refresh": "<refresh_token>"
}
```

## RBAC Permission Levels

### User Roles
1. **Admin**
   - Full system access
   - Can create, read, update, delete all resources

2. **Manager**
   - Partial system access
   - Limited create and edit permissions
   - Can view most resources

3. **Regular User**
   - Minimal permissions
   - Can only view/edit own resources

## Task Management

### 1. List Tasks
- **Endpoint**: `/api/tasks/`
- **Method**: GET
- **Permission**: 
  - Admin: See all tasks
  - Manager: Limited task view
  - User: Only own tasks

### 2. Create Task
- **Endpoint**: `/api/tasks/`
- **Method**: POST
- **Request Body**:
```json
{
    "summary": "Project meeting",
    "remind_at": "2024-01-15T10:00:00Z",
    "is_complete": false
}
```
- **Permission**:
  - Admin: Create any task
  - Manager: Create tasks
  - User: Create own tasks

### 3. Update Task
- **Endpoint**: `/api/tasks/{task_id}/`
- **Method**: PATCH
- **Request Body**:
```json
{
    "summary": "Updated meeting details",
    "is_complete": true
}
```
- **Permission**:
  - Admin: Update any task
  - Manager: Limited update
  - User: Update only own tasks

### 4. Delete Task
- **Endpoint**: `/api/tasks/{task_id}/`
- **Method**: DELETE
- **Permission**:
  - Admin: Delete any task
  - Manager: Limited delete
  - User: Delete only own tasks

## Profile Management

### 1. Get Profile
- **Endpoint**: `/api/profiles/`
- **Method**: GET
- **Permission**:
  - View own profile details

### 2. Update Profile
- **Endpoint**: `/api/profiles/{profile_id}/`
- **Method**: PATCH
- **Request Body**:
```json
{
    "bio": "Software Developer",
    "phone_number": "+1234567890"
}
```
- **Permission**:
  - Update own profile details

## Error Handling

### Common HTTP Status Codes
- 200: Successful request
- 201: Resource created
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden (RBAC restriction)
- 404: Resource not found
- 500: Server error

## Authentication Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```


## Rate Limiting
- Login attempts: 3 per minute
- API requests: 5 per minute for anonymous user and 20 per minute for authenticated user

## Postman Collection
- Download Postman collection for easy API testing
- Import collection with pre-configured requests
