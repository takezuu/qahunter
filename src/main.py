from typing import Union
from typing import Annotated
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from sqlmodel import Session, select
from fastapi import FastAPI, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.database import get_session
from src.routes import projects

app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]
app.include_router(projects.router)

@app.get("/")
async def root():
    return {"Hello it's home page"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_details = []
    for error in errors:
        error_type = error["type"]
        if len(error["loc"]) == 1:
            error_location = error["loc"]
        else:
            error_location = error["loc"][1]
        error_message = error["msg"]

        if error_message == "JSON decode error":
            ctx = error["ctx"]["error"]
            error_details.append(f"Type: {error_type}, Position: {error_location} - {error_message} - {ctx}")
        else:
            error_details.append(f"Type: {error_type}, Field: {error_location} - {error_message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation failed",
            "details": error_details
        }
    )