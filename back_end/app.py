import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from back_end.create_db import create_tables  
from back_end.route.login_route import router as login_route
from back_end.route.adminNaf_route import router as adminNaf_route
from back_end.route.usuario_route import router as usuario_route
from back_end.route.agenda_route import router as agenda_route
from back_end.utils.error_handlers import http_exception_handler, validation_exception_handler  # Importando os handlers

# Instanciação do aplicativo FastAPI
app = FastAPI()


logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    create_tables()  

# Registro dos handlers de exceção
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Inclusão das rotas
app.include_router(usuario_route)
app.include_router(adminNaf_route)
app.include_router(agenda_route)
app.include_router(login_route)
