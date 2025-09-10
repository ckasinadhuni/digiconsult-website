#!/usr/bin/env python3
"""
Tesseract OCR Service - ARM64 Optimized
FastAPI server for text extraction from images and PDFs
"""

import os
import time
import tempfile
import logging
from pathlib import Path
from typing import Dict, Any, List

import pytesseract
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import PyPDF2
import magic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tesseract OCR Service",
    description="ARM64-optimized OCR service for DigiConsult infrastructure",
    version="1.0.0"
)

# Configuration
UPLOAD_DIR = "/tmp/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS = {"image/jpeg", "image/png", "image/tiff", "image/bmp"}
SUPPORTED_PDF_FORMAT = "application/pdf"

# Ensure upload directory exists
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancer"""
    try:
        # Test Tesseract availability
        version = pytesseract.get_tesseract_version()
        return JSONResponse({
            "status": "healthy",
            "service": "tesseract-ocr",
            "tesseract_version": str(version),
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported OCR languages"""
    try:
        languages = pytesseract.get_languages()
        return JSONResponse({
            "languages": languages,
            "default": "eng"
        })
    except Exception as e:
        logger.error(f"Failed to get languages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve languages")

@app.post("/ocr/image")
async def ocr_image(file: UploadFile = File(...), lang: str = "eng"):
    """Extract text from image file using Tesseract OCR"""
    start_time = time.time()
    
    try:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Read file content
        content = await file.read()
        
        # Detect file type
        file_type = magic.from_buffer(content, mime=True)
        
        if file_type not in SUPPORTED_IMAGE_FORMATS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported format: {file_type}. Supported: {SUPPORTED_IMAGE_FORMATS}"
            )
        
        # Save temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
        temp_file.write(content)
        temp_file.flush()
        
        try:
            # Open and process image
            image = Image.open(temp_file.name)
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(image, lang=lang)
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            processing_time = time.time() - start_time
            
            return JSONResponse({
                "text": extracted_text.strip(),
                "confidence": round(avg_confidence / 100, 3),  # Normalize to 0-1
                "processing_time": round(processing_time, 3),
                "language": lang,
                "file_type": file_type,
                "characters_detected": len(extracted_text.strip())
            })
            
        finally:
            # Clean up temp file
            os.unlink(temp_file.name)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.post("/ocr/pdf")
async def ocr_pdf(file: UploadFile = File(...), lang: str = "eng"):
    """Extract text from PDF file"""
    start_time = time.time()
    
    try:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Read file content
        content = await file.read()
        
        # Detect file type
        file_type = magic.from_buffer(content, mime=True)
        
        if file_type != SUPPORTED_PDF_FORMAT:
            raise HTTPException(status_code=400, detail=f"Expected PDF, got: {file_type}")
        
        # Save temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(content)
        temp_file.flush()
        
        try:
            # Extract text from PDF
            extracted_text = ""
            page_count = 0
            
            with open(temp_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page_count = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
            
            processing_time = time.time() - start_time
            
            return JSONResponse({
                "text": extracted_text.strip(),
                "processing_time": round(processing_time, 3),
                "pages_processed": page_count,
                "file_type": file_type,
                "characters_extracted": len(extracted_text.strip())
            })
            
        finally:
            # Clean up temp file
            os.unlink(temp_file.name)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return JSONResponse({
        "service": "Tesseract OCR API",
        "version": "1.0.0",
        "endpoints": [
            "GET /health - Health check",
            "GET /languages - Supported languages",
            "POST /ocr/image - Extract text from images",
            "POST /ocr/pdf - Extract text from PDFs"
        ],
        "supported_formats": {
            "images": list(SUPPORTED_IMAGE_FORMATS),
            "documents": [SUPPORTED_PDF_FORMAT]
        }
    })

if __name__ == "__main__":
    logger.info("Starting Tesseract OCR Service on ARM64")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003,
        log_level="info",
        access_log=True
    )