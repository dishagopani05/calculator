from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from pydantic import BaseModel

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

class MathRequest(BaseModel):
    num1: float
    num2: float
    operation: str


@app.post("/calculate")    
async def calculate_math(request: MathRequest):
    try:
        # Construct the math query for Gemini
        prompt = f"What is {request.num1} {request.operation} {request.num2}?"

        # Generate response from Gemini
        response = model.generate_content(prompt)

        # Extract and clean response
        clean_response = response.text.strip()

        return {"question": prompt, "response": clean_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint (for testing)
@app.get("/")
async def root():
    return {"message": "Gemini FastAPI Math Solver is running!"}