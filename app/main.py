
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# ----------import packages
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routes.v1.life_span import combined_lifespan
from app.routes.v1.roles import roles_router
from app.routes.v1.users import user_router
from app.routes.v1.brands import brands_router
from app.routes.v1.categories import categories_router
from app.routes.v1.regions import regions_router
from app.routes.v1.districts import districts_router
from app.routes.v1.colors import colors_router
from app.routes.v1.loan_months import loan_months_router
from app.routes.v1.products import products_router
from app.routes.v1.productDetails   import product_details_router
from app.routes.v1.files import files_router

from app.utils.utils import get_current_user_for_docs



# from app.utils.websocket_connections import manager

app = FastAPI(lifespan=combined_lifespan,swagger_ui_parameters = {"docExpansion":"none"},docs_url=None, redoc_url=None, openapi_url=None,)



app.title = settings.app_name
app.version = settings.version




app.include_router(roles_router, prefix="/api/v1", tags=["User Roles"])
app.include_router(user_router, prefix="/api/v1", tags=["Users"])
app.include_router(brands_router, prefix="/api/v1", tags=["Brands"])
app.include_router(categories_router, prefix="/api/v1", tags=["Categories"])
app.include_router(regions_router, prefix="/api/v1", tags=["Regions"])
app.include_router(districts_router, prefix="/api/v1", tags=["Districts"])
app.include_router(colors_router, prefix="/api/v1", tags=["Colors"])
app.include_router(loan_months_router, prefix="/api/v1", tags=["Loan Months"])
app.include_router(products_router, prefix="/api/v1", tags=["Products"])
app.include_router(product_details_router, prefix="/api/v1", tags=["Product Details"])
app.include_router(files_router, prefix="/api/v1", tags=["Files"] )



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(current_user: str = Depends(get_current_user_for_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI",swagger_ui_parameters={"docExpansion": "none"},)


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(current_user: str = Depends(get_current_user_for_docs)):
    return get_openapi(title="Custom OpenAPI", version="1.0.0", routes=app.routes)



Base.metadata.create_all(bind=engine)

app.mount("/files", StaticFiles(directory="files"), name="files")



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




@app.get("/", tags=["Home"])
async def message( request: Request,):
    try:
        data = await request.json()  # Parse JSON data


        if not data:  # If data is empty
            raise HTTPException(status_code=400, detail="Empty JSON body received")

        print(str(data))  # Print as string
        return {"success": True, "message": "Data received", "data": data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")


add_pagination(app)
