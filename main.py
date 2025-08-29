from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re
import json
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FULL_NAME = "r_ram_shankar"
DOB = "23032005"
EMAIL = "ramshankar.r2022@vitstudent.ac.in"
ROLL_NUMBER = "22BCE1576"

class Inp(BaseModel):
    data: List[str]

def fix(txt):
    if not isinstance(txt, str):
        return str(txt)
    try:
        txt = txt.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
        txt = re.sub(r'[\u201c\u201d]', '"', txt)
        txt = re.sub(r'[\u2018\u2019]', "'", txt)
        txt = re.sub(r'[\u2013\u2014]', '-', txt)
        return txt
    except Exception:
        return str(txt)

@app.post("/bfhl")
async def process_data(req: Request):
    try:
        try:
            body = await req.body()
            if not body:
                return {
                    "is_success": False,
                    "error": "Request body is empty"
                }
            
            txt = body.decode('utf-8')
            txt = fix(txt)
            
        except UnicodeDecodeError:
            logger.error("Unicode decode error in request body")
            return {
                "is_success": False,
                "error": "Invalid character encoding in request body"
            }
        except Exception as e:
            logger.error(f"Error reading request body: {str(e)}")
            return {
                "is_success": False,
                "error": "Failed to read request body"
            }
        
        try:
            dat_json = json.loads(txt)
            if not isinstance(dat_json, dict):
                return {
                    "is_success": False,
                    "error": "Request body must be a JSON object"
                }
                
            dat = dat_json.get("data")
            if dat is None:
                return {
                    "is_success": False,
                    "error": "Missing 'data' field in request"
                }
                
            if not isinstance(dat, list):
                return {
                    "is_success": False,
                    "error": "'data' field must be an array"
                }
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return {
                "is_success": False,
                "error": "Invalid JSON format in request body"
            }
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            return {
                "is_success": False,
                "error": "Failed to parse JSON"
            }
        
        evn = []
        odd = []
        alp = []
        spc = []
        sm = 0
        cat = ""

        try:
            for idx, itm in enumerate(dat):
                try:
                    if itm is None:
                        continue
                        
                    itm = fix(itm)
                    
                    if itm.isdigit():
                        try:
                            num = int(itm)
                            if num % 2 == 0:
                                evn.append(itm)
                            else:
                                odd.append(itm)
                            sm += num
                        except (ValueError, OverflowError) as e:
                            logger.warning(f"Invalid number at index {idx}: {itm}")
                            continue
                            
                    elif itm.isalpha():
                        alp.append(itm.upper())
                        cat += itm
                    else:
                        spc.append(itm)
                        
                except Exception as e:
                    logger.warning(f"Error processing item at index {idx}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error processing data array: {str(e)}")
            return {
                "is_success": False,
                "error": "Failed to process data array"
            }

        try:
            cat = cat[::-1]
            alt = ""
            for i, ch in enumerate(cat):
                alt += ch.upper() if i % 2 == 0 else ch.lower()
        except Exception as e:
            logger.error(f"Error creating concat string: {str(e)}")
            alt = ""

        try:
            res = {
                "is_success": True,
                "user_id": f"{FULL_NAME.lower()}_{DOB}",
                "email": EMAIL,
                "roll_number": ROLL_NUMBER,
                "odd_numbers": odd,
                "even_numbers": evn,
                "alphabets": alp,
                "special_characters": spc,
                "sum": str(sm),
                "concat_string": alt
            }
            
            logger.info(f"Successfully processed request with {len(dat)} items")
            return res
            
        except Exception as e:
            logger.error(f"Error building response: {str(e)}")
            return {
                "is_success": False,
                "error": "Failed to build response"
            }

    except Exception as e:
        logger.error(f"Unexpected error in process_data: {str(e)}")
        return {
            "is_success": False,
            "error": "Internal server error occurred"
        }

@app.get("/bfhl")
async def get_operation_code():
    try:
        return {"operation_code": 1}
    except Exception as e:
        logger.error(f"Error in get_operation_code: {str(e)}")
        return {
            "is_success": False,
            "error": "Internal server error occurred"
        }