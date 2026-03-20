from fastapi import FastAPI, Header, HTTPException, Response, Depends
from pydantic import BaseModel, field_validator
from typing import Optional
import re
from datetime import datetime

app = FastAPI()


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v):
        pattern = r"^[a-zA-Z]{2}-[a-zA-Z]{2}(,[a-zA-Z]{2};q=0\.\d+)*$"
        if not re.match(pattern, v):
            raise ValueError("Invalid Accept-Language format")
        return v


def get_headers(
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing required headers")

    return CommonHeaders(
        user_agent=user_agent,
        accept_language=accept_language
    )


@app.get("/headers")
def read_headers(headers: CommonHeaders = Depends(get_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info")
def read_info(response: Response, headers: CommonHeaders = Depends(get_headers)):
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()

    return {
        "message": "Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }