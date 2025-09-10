#!/usr/bin/env python3
"""
Whisper Web UI - FastAPI Frontend for Faster-Whisper Service
ARM64 Optimized | Lightweight | Production Ready
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import aiofiles
import os
import json
import tempfile
import uuid
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Whisper Web UI",
    description="File upload interface for Faster-Whisper transcription",
    version="1.0.0"
)

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
FASTER_WHISPER_URL = "http://faster-whisper:8000"
UPLOAD_DIR = Path("/tmp/whisper-uploads")
RESULTS_DIR = Path("/tmp/whisper-results")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.mp4', '.avi', '.mov', '.flac', '.ogg'}

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main upload interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FASTER_WHISPER_URL}/health", timeout=5.0)
            backend_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        backend_status = "unreachable"
    
    return {
        "status": "healthy",
        "backend_status": backend_status,
        "timestamp": datetime.utcnow().isoformat()
    }

def validate_file(file: UploadFile) -> tuple[bool, str]:
    """Validate uploaded file"""
    # Check file extension
    if file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # File size will be checked during upload
    return True, "Valid"

def format_srt(segments: list, filename: str) -> str:
    """Convert segments to SRT format"""
    srt_content = []
    for i, segment in enumerate(segments, 1):
        start_time = format_timestamp(segment.get('start', 0))
        end_time = format_timestamp(segment.get('end', 0))
        text = segment.get('text', '').strip()
        
        srt_content.append(f"{i}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")  # Empty line
    
    return "\n".join(srt_content)

def format_timestamp(seconds: float) -> str:
    """Format timestamp for SRT (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')

@app.post("/transcribe")
async def transcribe_file(
    file: UploadFile = File(...),
    task: str = Form("transcribe"),
    language: Optional[str] = Form(None),
    output_format: str = Form("json")
):
    """Upload and transcribe audio file"""
    
    # Validate file
    is_valid, error_msg = validate_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Generate unique ID for this transcription
    transcription_id = str(uuid.uuid4())
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Create temporary file
        temp_file = UPLOAD_DIR / f"{transcription_id}_{file.filename}"
        
        async with aiofiles.open(temp_file, 'wb') as f:
            await f.write(file_content)
        
        logger.info(f"Processing file: {file.filename} ({len(file_content)} bytes)")
        
        # Send to faster-whisper service
        async with httpx.AsyncClient(timeout=300.0) as client:
            with open(temp_file, 'rb') as audio_file:
                files = {'file': (file.filename, audio_file, file.content_type)}
                data = {'task': task}
                if language:
                    data['language'] = language
                
                response = await client.post(
                    f"{FASTER_WHISPER_URL}/transcribe", 
                    files=files, 
                    data=data
                )
        
        # Clean up temp file
        temp_file.unlink(missing_ok=True)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Transcription failed: {response.text}"
            )
        
        result = response.json()
        
        # Add metadata
        result['transcription_id'] = transcription_id
        result['filename'] = file.filename
        result['file_size'] = len(file_content)
        result['timestamp'] = datetime.utcnow().isoformat()
        
        # Save result for downloads
        result_file = RESULTS_DIR / f"{transcription_id}.json"
        async with aiofiles.open(result_file, 'w') as f:
            await f.write(json.dumps(result, indent=2))
        
        # Return appropriate format
        if output_format == "srt":
            segments = result.get('segments', [])
            srt_content = format_srt(segments, file.filename)
            
            srt_file = RESULTS_DIR / f"{transcription_id}.srt"
            async with aiofiles.open(srt_file, 'w') as f:
                await f.write(srt_content)
            
            return {"transcription_id": transcription_id, "srt_content": srt_content}
        
        return result
        
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=503, detail="Transcription service unavailable")
    
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.get("/download/{transcription_id}")
async def download_result(transcription_id: str, format: str = "json"):
    """Download transcription result in specified format"""
    
    try:
        result_file = RESULTS_DIR / f"{transcription_id}.json"
        
        if not result_file.exists():
            raise HTTPException(status_code=404, detail="Transcription not found")
        
        # Read original result
        async with aiofiles.open(result_file, 'r') as f:
            result = json.loads(await f.read())
        
        filename_base = result.get('filename', transcription_id).split('.')[0]
        
        if format.lower() == "json":
            return FileResponse(
                result_file,
                media_type="application/json",
                filename=f"{filename_base}_transcription.json"
            )
        
        elif format.lower() == "srt":
            segments = result.get('segments', [])
            srt_content = format_srt(segments, filename_base)
            
            srt_file = RESULTS_DIR / f"{transcription_id}.srt"
            async with aiofiles.open(srt_file, 'w') as f:
                await f.write(srt_content)
            
            return FileResponse(
                srt_file,
                media_type="text/plain",
                filename=f"{filename_base}.srt"
            )
        
        elif format.lower() == "txt":
            segments = result.get('segments', [])
            text_content = "\n".join([seg.get('text', '').strip() for seg in segments])
            
            txt_file = RESULTS_DIR / f"{transcription_id}.txt"
            async with aiofiles.open(txt_file, 'w') as f:
                await f.write(text_content)
            
            return FileResponse(
                txt_file,
                media_type="text/plain",
                filename=f"{filename_base}.txt"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use: json, srt, txt")
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.get("/results")
async def list_results():
    """List available transcription results"""
    results = []
    
    for result_file in RESULTS_DIR.glob("*.json"):
        try:
            async with aiofiles.open(result_file, 'r') as f:
                result = json.loads(await f.read())
                
                results.append({
                    "transcription_id": result.get('transcription_id'),
                    "filename": result.get('filename'),
                    "timestamp": result.get('timestamp'),
                    "duration": result.get('duration'),
                    "language": result.get('language')
                })
        except Exception:
            continue
    
    # Sort by timestamp (newest first)
    results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return {"results": results[:20]}  # Return latest 20

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004, log_level="info")