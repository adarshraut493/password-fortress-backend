from fastapi import FastAPI
app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://inquisitive-kleicha-27d717.netlify.app"
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
    score = 0
    suggestions = []

    if len(pwd) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if re.search(r"[A-Z]", pwd):
        score += 1
    else:
        suggestions.append("Add an uppercase letter")

    if re.search(r"[a-z]", pwd):
        score += 1
    else:
        suggestions.append("Add a lowercase letter")

    if re.search(r"[0-9]", pwd):
        score += 1
    else:
        suggestions.append("Add a number")

    if re.search(r"[^A-Za-z0-9]", pwd):
        score += 1
    else:
        suggestions.append("Add a special character")

    strength = ["Weak", "Medium", "Strong"][min(score // 2, 2)]
    return {"strength": strength, "suggestions": suggestions}
