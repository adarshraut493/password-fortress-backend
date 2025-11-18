from fastapi import FastAPI
app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://inquisitive-kleicha-27d717.netlify.app"
        # "http://localhost:3001"
    ],  # 👈 your Netlify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to Password Fortress!"}

from pydantic import BaseModel
import re

class PasswordInput(BaseModel):
    password: str

@app.post("/check_strength")
def check_strength(data: PasswordInput):
    pwd = data.password
    suggestions = []

    has_length = len(pwd) >= 8
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_lower = bool(re.search(r"[a-z]", pwd))
    has_number = bool(re.search(r"[0-9]", pwd))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", pwd))

    # Collect suggestions
    if not has_length:
        suggestions.append("Use at least 8 characters")
    if not has_upper:
        suggestions.append("Add an uppercase letter")
    if not has_lower:
        suggestions.append("Add a lowercase letter")
    if not has_number:
        suggestions.append("Add a number")
    if not has_symbol:
        suggestions.append("Add a special character")

    # Strict strength logic
    if has_length and has_upper and has_lower and has_number and has_symbol:
        strength = "Strong 🤩"
        suggestions = []  # No suggestions for strong
    elif has_length and (has_upper or has_lower) and (has_number or has_symbol):
        strength = "Medium 😀"
    else:
        strength = "Weak 😩"

    return {"strength": strength, "suggestions": suggestions}
