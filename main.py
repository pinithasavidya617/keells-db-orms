from fastapi import FastAPI

from user_routes import router as user_router
from invoice_routes import router as invoice_router
app = FastAPI(title="C-Clarke ORM Implementation with DB Agent")

app.include_router(router=user_router)
app.include_router(router=invoice_router)