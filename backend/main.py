from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import fitz

app = FastAPI(title="StudyForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "app": "StudyForge",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()

    doc = fitz.open(
        stream=contents,
        filetype="pdf"
    )

    pages = []

    for page in doc:
        pages.append(page.get_text())

    text = "\n".join(pages)

    doc.close()

    return {
        "filename": file.filename,
        "pages": len(pages),
        "text": text
    }