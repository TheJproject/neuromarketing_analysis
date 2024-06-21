import instructor
from openai import OpenAI
from fastapi import UploadFile
from app.schemas import ProcessA1Response, ProcessA2Response, ProcessBResponse, ProcessCResponse
import base64
import os
import logging

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY), mode=instructor.function_calls.Mode.MD_JSON)

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

async def read_and_encode_image(file: UploadFile) -> str:
    image_bytes = await file.read()
    encoded_image = encode_image(image_bytes)
    return encoded_image

async def analyze_image(base64_image: str) -> ProcessA1Response:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=ProcessA1Response,
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "You are a Senior Insights Manager with decades of experience, and a background in marketing."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": """You are provided with an image of a digital advertisement.
                                                You have two tasks:
                                                    1) Provide a detailed description of the advert. In other words, identify and
                                                    describe the key elements such as the product being advertised, the brand name,
                                                    and the call-to-action (CTA), where available.
                                                    2) Additionally, assess and determine the primary purpose of the advertisement."""},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
    )
    return response

async def analyze_heatmap(base64_image: str, base64_heatmap: str, chain_response: ProcessA1Response) -> ProcessA2Response:
    # Log only the first 50 characters for readability
    logging.info(f"Base64 Image: {base64_image[:50]}...")  # Log the start of the base64 string
    logging.info(f"Base64 Heatmap: {base64_heatmap[:50]}...")  # Log the start of the base64 string

    messages = [
        {
            "role": "system",
            "content": "You are a Senior Insights Manager with decades of experience, and a background in marketing."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """You are provided with an image of a digital advertisement.
                                            You have two tasks:
                                                1) Provide a detailed description of the advert. In other words, identify and
                                                describe the key elements such as the product being advertised, the brand name,
                                                and the call-to-action (CTA), where available.
                                                2) Additionally, assess and determine the primary purpose of the advertisement."""},
                {"type": "image_url", "image_url":  {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        },
        {
            "role": "system",
            "content": chain_response.model_dump_json()
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """You are now provided with the attention heatmap of the same image. The
                                            attention heatmap illustrates the distribution of attention as predicted by an
                                            AI model that was trained on eye-tracking data. Red colour indicates high
                                            attention, green implies moderate level and transparent colours mean low
                                            attention. Please do not confuse the heatmap colours, i.e. the red, yellow,
                                            green blobs etc. with the actual colours of the video frames.
                                            You have a single task:
                                            Based on the provided heatmap, identify the most visually salient elements,
                                            i.e. the elements that catch the most attention. Please pay special attention
                                            to the product being advertised, the brand or logo, and call-to-action (CTA),
                                            where available."""},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_heatmap}"}},
            ],
        },
    ]

    #logging.info(f"Messages payload: {messages}")

    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=ProcessA2Response,
        max_tokens=4000,
        messages=messages
    )
    return response

async def cognitiveload_image(base64_image: str) -> ProcessBResponse:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=ProcessBResponse,
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in applied neuroscience and behavioural psychology."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": """Assess the perceptual or cognitive load of the image. This is a measure of the
                                                effort required for mental processing based on the visual complexity, such as
                                                diversity of colours, presence of patterns and the inclusion of text. In other
                                                words, assess how accessible the image will be to a viewer in terms of the
                                                brain processing capacity required to interpret and understand the
                                                advertisement."""},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
    )
    return response

async def summarize_results(first_output: str, second_output: str) -> ProcessCResponse:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=ProcessCResponse,
        max_tokens=1800,
        messages=[
            {
                "role": "system",
                "content": "You are a professional writer."
            },
            {
                "role": "user",
                "content": f"""You are provided with text descriptions that are outputs from two different
                                                multi-modal LLMs.Summarise the text provided from the following two different outputs:
                                                1st output: {first_output}
                                                2nd output: {second_output}"""
            }
        ]
    )
    return response
