from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body, Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import shutil
import os

from models import User, UserInDB, UserCreate, Token, TokenData, Item, ItemCreate, ItemUpdate
from database import fake_users_db, fake_items_db

# App configuration
app = FastAPI(
    title="FastAPI Learning Project",
    description="Comprehensive FastAPI project for testing and learning with Swagger UI",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
    },
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use proper secret management
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    return """
    <html>
        <head>
            <title>FastAPI Learning Project</title>
        </head>
        <body>
            <h1>Welcome to FastAPI Learning Project</h1>
            <p>Visit <a href="/docs">/docs</a> for Swagger UI documentation</p>
            <p>Visit <a href="/redoc">/redoc</a> for ReDoc documentation</p>
        </body>
    </html>
    """

# Authentication routes
@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/users/", response_model=User, tags=["Users"])
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    fake_users_db[user.username] = user_dict
    return user_dict

# Item routes
@app.get("/items/", response_model=List[Item], tags=["Items"])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    current_user: User = Depends(get_current_active_user)
):
    """Get a list of items with optional pagination and search"""
    items = list(fake_items_db.values())[skip : skip + limit]
    if q:
        items = [item for item in items if q.lower() in item["name"].lower()]
    return items

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", gt=0),
    current_user: User = Depends(get_current_active_user)
):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    new_id = max(fake_items_db.keys()) + 1 if fake_items_db else 1
    fake_items_db[new_id] = {
        "id": new_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "owner": current_user.username
    }
    return fake_items_db[new_id]

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(
    item_id: int,
    item: ItemUpdate,
    current_user: User = Depends(get_current_active_user)
):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if fake_items_db[item_id]["owner"] != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    
    stored_item = fake_items_db[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = {**stored_item, **update_data}
    fake_items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user)
):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if fake_items_db[item_id]["owner"] != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    del fake_items_db[item_id]
    return None

# File upload example
@app.post("/uploadfile/", tags=["Files"])
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    try:
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    return {"filename": file.filename, "location": file_location}

@app.get("/download/{filename}", tags=["Files"])
async def download_file(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

# Form data example
@app.post("/login-form/", tags=["Forms"])
async def login_form(
    username: str = Form(...),
    password: str = Form(...)
):
    return {"username": username}

# Advanced query parameters example
@app.get("/advanced-query/", tags=["Advanced"])
async def advanced_query(
    q: Optional[str] = Query(None, title="Query string", alias="query"),
    ids: List[int] = Query([], title="List of IDs"),
    importance: int = Query(1, gt=0, le=3, description="Importance level (1-3)")
):
    return {"q": q, "ids": ids, "importance": importance}

# Custom response example
@app.get("/custom-response/", tags=["Advanced"])
async def custom_response():
    content = {"message": "This is a custom response"}
    headers = {"X-Custom-Header": "custom-value"}
    return JSONResponse(content=content, headers=headers)

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy"}