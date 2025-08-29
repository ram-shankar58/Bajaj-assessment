from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re
import json

app = FastAPI()

NAME = "john_doe"
DOB = "17091999"
EML = "john@xyz.com"
ROL = "ABCD123"

class Inp(BaseModel):
    data: List[str]

def fix(txt):
    txt = txt.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
    txt = re.sub(r'[\u201c\u201d]', '"', txt)
    txt = re.sub(r'[\u2018\u2019]', "'", txt)
    return txt

@app.post("/bfhl")
async def process_data(inp: Inp):
    try:
        dat = inp.data
        
        evn = []
        odd = []
        alp = []
        spc = []
        sm = 0
        cat = ""

        for itm in dat:
            itm = fix(itm)
            if itm.isdigit():
                num = int(itm)
                if num % 2 == 0:
                    evn.append(itm)
                else:
                    odd.append(itm)
                sm += num
            elif itm.isalpha():
                alp.append(itm.upper())
                cat += itm
            else:
                spc.append(itm)

        cat = cat[::-1]
        alt = ""
        for i, ch in enumerate(cat):
            alt += ch.upper() if i % 2 == 0 else ch.lower()

        res = {
            "is_success": True,
            "user_id": f"{NAME.lower()}_{DOB}",
            "email": EML,
            "roll_number": ROL,
            "odd_numbers": odd,
            "even_numbers": evn,
            "alphabets": alp,
            "special_characters": spc,
            "sum": str(sm),
            "concat_string": alt
        }

        return res
    except Exception as e:
        return {
            "is_success": False,
            "error": str(e)
        }

@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}