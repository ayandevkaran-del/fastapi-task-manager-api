from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import models, auth, database

app = FastAPI(title="Any.ai Backend Task")
models.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401)

@app.post("/register")
def register(email: str, password: str, role: str = "user", db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = models.User(email=email, hashed_password=auth.hash_pass(password), role=role)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_pass(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks")
def get_tasks(user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.Task).filter(models.Task.owner_id == user.id).all()

@app.post("/tasks")
def create_task(title: str, desc: str, user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    task = models.Task(title=title, description=desc, owner_id=user.id)
    db.add(task)
    db.commit()
    return {"message": "Task created"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}