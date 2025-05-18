from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

# FastAPI app metadata
app = FastAPI(
    title="User Management API",
    description="User management system with MySQL integration.",
    version="5.6.0"
)

# DB Connection Dependency
def get_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fresh$321",
            database="FastAPI"
        )
        cursor = db.cursor(dictionary=True)
        yield cursor
    finally:
        db.commit()
        cursor.close()
        db.close()

# Pydantic Model
class User(BaseModel):
    name: str
    email: str
    age: int

# ---------------- API Endpoints ----------------

# GET: Fetch All Users
@app.get('/viewuser', status_code=200, tags=["users"], summary="Get all users")
def get_all_users(cursor=Depends(get_db)):
    try:
        cursor.execute("SELECT * FROM USER")
        result = cursor.fetchall()
        return {"users": result}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")


# GET: Fetch User by ID
@app.get('/viewuser/{user_id}', status_code=200, tags=["users"], summary="Get user by ID")
def get_single_user(user_id: int, cursor=Depends(get_db)):
    try:
        cursor.execute("SELECT * FROM USER WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": result}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")


# POST: Create New User
@app.post('/create_user', status_code=status.HTTP_201_CREATED, tags=["users"], summary="Create new user")
def create_user(user: User, cursor=Depends(get_db)):
    try:
        cursor.execute(
            "INSERT INTO USER (name, email, age) VALUES (%s, %s, %s)",
            (user.name, user.email, user.age)
        )
        user_id = cursor.lastrowid
        return {
            "message": "User created successfully",
            "user_id": user_id
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")


# PUT: Update Existing User
@app.put('/update_user/{user_id}', status_code=status.HTTP_200_OK, tags=["users"], summary="Update user")
def update_user(user_id: int, user: User, cursor=Depends(get_db)):
    try:
        cursor.execute("SELECT * FROM USER WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute(
            "UPDATE USER SET name = %s, email = %s, age = %s WHERE id = %s",
            (user.name, user.email, user.age, user_id)
        )
        return {"message": "User updated successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")


# DELETE: Remove User by ID
@app.delete('/delete_user/{user_id}', status_code=status.HTTP_200_OK, tags=["users"], summary="Delete user")
def delete_user(user_id: int, cursor=Depends(get_db)):
    try:
        cursor.execute("SELECT * FROM USER WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("DELETE FROM USER WHERE id = %s", (user_id,))
        return {"message": "User deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
