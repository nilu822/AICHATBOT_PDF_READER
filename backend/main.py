from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
from backend.rag.rag_pipeline import load_pdf_and_store, answer_query



from rag.rag_pipeline import load_pdf_and_store, answer_query

load_dotenv()

app = FastAPI()

# ----------------------------
# Correct Paths Based on Your Folder Structure
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # aichatbot/
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = BASE_DIR / "static"

# ----------------------------
# Static File Mount (IMPORTANT)
# ----------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ----------------------------
# Serve index.html
# ----------------------------
@app.get("/")
def read_index():
    return FileResponse(FRONTEND_DIR / "index.html")


# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Upload PDF
# ----------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    load_pdf_and_store(pdf_bytes)
    return {"message": "Uploaded and indexed successfully!"}


# ----------------------------
# Chat Endpoint
# ----------------------------
@app.get("/chat")
async def chat(q: str):
    response = answer_query(q)
    return {"answer": response}
