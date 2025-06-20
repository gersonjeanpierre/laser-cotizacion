from fastapi import APIRouter
from . import store
from . import type_client
from . import product_type
from . import extra_option
from . import product
from . import customer

api_router = APIRouter()
api_router.include_router(store.router)
api_router.include_router(type_client.router)
api_router.include_router(product_type.router)
api_router.include_router(extra_option.router)
api_router.include_router(product.router)
api_router.include_router(customer.router)