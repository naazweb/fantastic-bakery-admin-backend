from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.routes import product, category
from app.database import Base, engine
from fastapi.exceptions import RequestValidationError, HTTPException
from app.utils import response_wrapper
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate

# Create a FastAPI instance
app = FastAPI()
add_pagination(app)

# Creates all tables in database
Base.metadata.create_all(bind=engine)

# Allow requests from your React application's domain
origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace with your React app's domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Handle Validation Error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_response = []
    for error in exc.errors():
        field_name = ".".join(str(loc)
                              for loc in error["loc"] if loc != "body")
        error_message = f"{error['msg']}"
        error_response.append({"field": field_name, "error": error_message})
    return JSONResponse(status_code=400, content=response_wrapper("error", "Validation Error", None, error_response))


# Handle HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(status_code=404, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


# Handle Unpredicted Error
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    print(exc)
    return JSONResponse(status_code=500, content=exc.detail)


# Include your API routers here
app.include_router(product.router, prefix="")
app.include_router(category.router, prefix="")


if __name__ == "__main__":
    # Run the FastAPI application using Uvicorn server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
