from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Union
import re

app = FastAPI()

# Replace with your details
FULL_NAME = "john_doe"
DOB = "17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

class InputData(BaseModel):
    data: List[str]

@app.post("/bfhl")
async def process_data(input_data: InputData):
    try:
        data = input_data.data
        
        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_chars = []
        sum_numbers = 0
        concat_string = ""

        # Separate data
        for item in data:
            if item.isdigit():  # Check if item is a number (handles single digits and multi-digit numbers)
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                sum_numbers += num
            elif item.isalpha():  # Check if item contains only alphabetic characters
                alphabets.append(item.upper())
                concat_string += item
            else:  # Special characters
                special_chars.append(item)

        # Alternating caps reverse concatenation
        concat_string = concat_string[::-1]
        alt_caps = ""
        for i, ch in enumerate(concat_string):
            alt_caps += ch.upper() if i % 2 == 0 else ch.lower()

        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME.lower()}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_chars,
            "sum": str(sum_numbers),
            "concat_string": alt_caps
        }

        return response
    except Exception as e:
        return {
            "is_success": False,
            "error": str(e)
        }

@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}