from fastapi import Query
from fastapi import FastAPI
app = FastAPI()

AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD = "supersecretpassword123!"
@app.get("/")
def health_check():
    return {"status": "healthy", "service": "target-api"}

@app.get("/user/{user_id}")
def get_user_data(user_id: str):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    return {
        "query_executed": query, 
        "message": "This endpoint simulates a dangerous DB query."
    }