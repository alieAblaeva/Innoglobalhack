from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import sqlite3
from typing import List, Optional
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the frontend URL for production (e.g., ["https://yourfrontend.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "/home/alie/Innoglobalhack/db/VKdatabase"

print(os.path.exists(DB_NAME))

@app.get("/api/employees")
async def get_employees(
    category: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    skill: Optional[str] = Query(None)
) -> List[dict]:
    # Try to connect to the database and print a message if successful
    try:
        conn = sqlite3.connect(DB_NAME)
        print("Connected to database successfully")
    except sqlite3.Error as e:
        print(f"Failed to connect to database: {e}")
        return JSONResponse(content={"error": "Database connection failed"}, status_code=500)

    cursor = conn.cursor()

    query = "SELECT id, name, fields, comment, languages FROM employees WHERE 1=1"
    params = []

    if category:
        query += " AND fields LIKE ?"
        params.append(f'%{category}%')

    if location:
        query += " AND city = ?"
        params.append(location)

    if skill:
        query += " AND languages LIKE ?"
        params.append(f'%{skill}%')  

    # Print the query and parameters for debugging
    print("Executing query:", query)
    print("With parameters:", params)

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Query execution failed: {e}")
        return JSONResponse(content={"error": "Query execution failed"}, status_code=500)

    employees = []
    for row in rows:
        print(row)
        employee = {
            "id": row[0],
            "name": row[1],
            "skills": row[4].split(", "), 
            "comment": row[3]
        }
        employees.append(employee)
    print(employees)
    conn.close()
    print("Connection to database closed")
    # print(JSONResponse(content=employees))
    return JSONResponse(content=employees)
