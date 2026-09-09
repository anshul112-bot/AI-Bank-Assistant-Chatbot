from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from auth import create_token, current_user, hash_password, verify_password
from chatbot import answer
from database import Base, SessionLocal, engine, get_db
from models import ChatMessage, Transaction, User

app = FastAPI(title="National Digital Bank API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)

class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
class Signup(Credentials): name: str = Field(min_length=2, max_length=100)
class MessageIn(BaseModel): content: str = Field(min_length=1, max_length=2000)

def public_user(user):
    return {"id": user.id, "name": user.name, "email": user.email, "account_number": user.account_number, "balance": user.balance}

@app.on_event("startup")
def seed():
    db = SessionLocal()
    try:
        if not db.query(User).filter_by(email="demo@ndb.com").first():
            demo = User(name="Anshul Sharma", email="demo@ndb.com", password_hash=hash_password("Demo@123"), account_number="NDB-4820-1192", balance=125000)
            db.add(demo); db.commit(); db.refresh(demo)
            db.add_all([
                Transaction(user_id=demo.id, title="Salary credit", amount=85000, direction="credit", category="Income"),
                Transaction(user_id=demo.id, title="FreshMart Groceries", amount=1840, direction="debit", category="Shopping"),
                Transaction(user_id=demo.id, title="Electricity bill", amount=2460, direction="debit", category="Bills"),
                Transaction(user_id=demo.id, title="UPI from Riya", amount=2200, direction="credit", category="Transfer"),
            ]); db.commit()
    finally: db.close()

@app.get("/health")
def health(): return {"status": "healthy"}

@app.post("/auth/signup")
def signup(data: Signup, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first(): raise HTTPException(400, "An account already exists with this email")
    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password), account_number=f"NDB-{datetime.now().strftime('%M%S%f')[-10:]}")
    db.add(user); db.commit(); db.refresh(user)
    return {"token": create_token(user.id), "user": public_user(user)}

@app.post("/auth/login")
def login(data: Credentials, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.password_hash): raise HTTPException(401, "Incorrect email or password")
    return {"token": create_token(user.id), "user": public_user(user)}

@app.get("/users/me")
def me(user: User = Depends(current_user)): return public_user(user)

@app.get("/dashboard")
def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.created_at.desc()).limit(8).all()
    return {"balance": user.balance, "account_number": user.account_number, "transactions": [{"id":t.id,"title":t.title,"amount":t.amount,"direction":t.direction,"category":t.category,"date":t.created_at.strftime('%d %b')} for t in txs]}

@app.get("/chat/history")
def history(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(ChatMessage).filter_by(user_id=user.id).order_by(ChatMessage.created_at.asc()).limit(100).all()
    return [{"id":x.id,"role":x.role,"content":x.content,"created_at":x.created_at.isoformat()} for x in rows]

@app.post("/chat")
def chat(data: MessageIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    reply = answer(data.content)
    db.add_all([ChatMessage(user_id=user.id, role="user", content=data.content), ChatMessage(user_id=user.id, role="assistant", content=reply)])
    db.commit()
    return {"reply": reply}
