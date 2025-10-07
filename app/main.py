from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes.routes import all_api_routes
from app.routes.agents import router as agents_router
from app.config import settings
from app.kernel.kernel import get_kernel

import logging


# Create the kernel with the aidbox_client
kernel = get_kernel()


# This will run on application startup (before the API is ready to accept requests)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting {Place_holder_for_service} Queue Listener Thread...")
    # please the service code here
    logging.info("Started {Place_holder_for_service} Queue Listener Thread")
    yield


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"tryItOutEnabled": True})


app.include_router(all_api_routes)
app.include_router(agents_router, prefix="/api", tags=["Agent Operations"])
