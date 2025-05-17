# FastAPI Learning Project

A comprehensive FastAPI project designed for testing and learning API development with Swagger documentation.

## Features

- JWT Authentication (OAuth2 with password flow)
- CRUD operations with items
- User management
- File upload/download
- Form data handling
- Comprehensive Swagger UI documentation
- Example endpoints demonstrating various FastAPI features

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sameeralam3127/FastAPI_Project.git
   cd FastAPI_Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The application will be available at:
- http://127.0.0.1:8000

## API Documentation

Interactive documentation is available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Test Users

The database comes with these test users:

| Username | Password | Status  |
|----------|----------|---------|
| johndoe  | secret   | Active  |
| alice    | secret   | Disabled|

## API Endpoints

### Authentication
- `POST /token` - Get JWT access token
- `GET /users/me` - Get current user info

### Users
- `POST /users/` - Create new user

### Items
- `GET /items/` - List all items (with pagination)
- `GET /items/{item_id}` - Get specific item
- `POST /items/` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Files
- `POST /uploadfile/` - Upload a file
- `GET /download/{filename}` - Download a file

### Advanced
- `GET /advanced-query/` - Example of complex query parameters
- `GET /custom-response/` - Example of custom response

## Project Structure

```
fastapi-learning-project/
├── main.py                # Main FastAPI application
├── models.py              # Pydantic models/schemas
├── database.py            # Simulated database
├── requirements.txt       # Dependencies
└── README.md              # This documentation
```

## Testing with Swagger UI

1. Start by getting an access token at `/token` endpoint using:
   - username: `johndoe`
   - password: `secret`

2. Click "Authorize" button and paste the token

3. Test protected endpoints like `/users/me` and `/items/`

## Dependencies

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- python-jose (JWT tokens)
- passlib (password hashing)
- python-multipart (form parsing)

## License

MIT
```

