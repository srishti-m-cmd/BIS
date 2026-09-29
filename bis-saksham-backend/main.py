"""
BIS SAKSHAM - FastAPI Application Entry Point
==============================================
Bureau of Indian Standards Compliance Management System
Demo Backend - All data is labeled [DEMO DATA]

Run with:
    uvicorn main:app --reload

API Documentation:
    http://localhost:8000/docs     (Swagger UI)
    http://localhost:8000/redoc    (ReDoc)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import HealthResponse
from app.routers import products, bom, labs, documents, chat, standards, services, updates

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="BIS SAKSHAM API",
    description=(
        "## BIS SAKSHAM - Bureau of Indian Standards Compliance Assistant\n\n"
        "A FastAPI backend for managing BIS compliance workflows including:\n"
        "- Product compliance analysis\n"
        "- IS standard & QCO mapping\n"
        "- Bill of Materials (BOM) compliance assessment\n"
        "- NABL lab matching\n"
        "- Document analysis\n"
        "- Compliance gap identification\n\n"
        "> **⚠️ DEMO DATA**: All products, standards references, laboratory details, "
        "and compliance assessments in this system are **demo/synthetic data** "
        "for illustration purposes only. They do NOT represent real BIS records, "
        "real NABL accreditations, or authoritative compliance decisions.\n\n"
        "For real BIS compliance, visit [bis.gov.in](https://www.bis.gov.in/)"
    ),
    version="1.0.0-demo",
    contact={
        "name": "BIS SAKSHAM Demo",
        "url": "https://www.bis.gov.in/",
    },
    license_info={
        "name": "Demo - Not for production use",
    },
    openapi_tags=[
        {"name": "Health", "description": "System health check"},
        {"name": "Products", "description": "Product analysis and compliance management"},
        {"name": "BOM Analysis", "description": "Bill of Materials compliance assessment"},
        {"name": "Laboratory Matching", "description": "NABL lab matching for required tests"},
        {"name": "Document Analysis", "description": "Compliance document upload and analysis"},
        {"name": "Chat Assistant", "description": "Contextual BIS compliance chat assistant"},
        {"name": "Standards", "description": "IS standards catalog search"},
        {"name": "BIS Services", "description": "BIS certification and registration services"},
        {"name": "Regulatory Updates", "description": "Regulatory change notifications"},
    ],
)

# ---------------------------------------------------------------------------
# CORS - Open for development
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Open for demo; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ---------------------------------------------------------------------------
# Mount routers
# ---------------------------------------------------------------------------

app.include_router(products.router)
app.include_router(bom.router)
app.include_router(labs.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(standards.router)
app.include_router(services.router)
app.include_router(updates.router)

# ---------------------------------------------------------------------------
# Root & Health endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"], summary="API root")
async def root():
    """Returns a welcome message and links to API docs."""
    return JSONResponse(content={
        "message": "Welcome to BIS SAKSHAM API",
        "version": "1.0.0-demo",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "data_label": "DEMO DATA",
        "disclaimer": (
            "All data in this system is DEMO/SYNTHETIC DATA for illustration only. "
            "Not authoritative BIS records. Visit https://www.bis.gov.in/ for official information."
        ),
    })


@app.get("/health", response_model=HealthResponse, tags=["Health"], summary="Health check")
async def health_check():
    """Returns the health status of the API."""
    return HealthResponse(
        status="healthy",
        version="1.0.0-demo",
        environment="development",
        data_label="DEMO DATA",
    )


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "data_label": "DEMO DATA",
        },
    )
