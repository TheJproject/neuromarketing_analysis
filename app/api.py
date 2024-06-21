from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import analyze_image, analyze_heatmap, cognitiveload_image, summarize_results
from app.schemas import ProcessCResponse
import logging

router = APIRouter()

@router.post("/analyze", response_model=ProcessCResponse)
async def analyze(image: UploadFile = File(...), heatmap: UploadFile = File(...)):
    try:
        logging.info("Received request to /analyze")
        
        # Process A1
        logging.info("Starting Process A1")
        process_a1_result = await analyze_image(image)
        logging.info(f"Process A1 result: {process_a1_result}")
        
        # Process A2
        logging.info("Starting Process A2")
        process_a2_result = await analyze_heatmap(image, heatmap, process_a1_result)
        logging.info(f"Process A2 result: {process_a2_result}")
        
        # Process B
        logging.info("Starting Process B")
        process_b_results = await cognitiveload_image(image)
        logging.info(f"Process B result: {process_b_results}")

        # Process C
        logging.info("Starting Process C")
        process_c_results = await summarize_results(process_a2_result.model_dump_json(), process_b_results.model_dump_json())
        logging.info(f"Process C result: {process_c_results}")

        return process_c_results
    except Exception as e:
        logging.error(f"Error processing the request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
