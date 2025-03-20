from google.genai import types
from models import DogAnalysis
from google.genai.client import Client

def analyzeImage(client: Client, image_data: bytes) -> DogAnalysis:
    """
    Analyze an image using Gemini AI to detect dogs and their state.

    Args:
        client: The Gemini AI client
        image_data: The binary image data to analyze

    Returns:
        DogAnalysis: An object containing the analysis results
    """
    contents = types.Content(
        role='user',
        parts=[
            types.Part.from_text(text="Analyze this image:"),
            types.Part.from_bytes(data=image_data, mime_type='image/jpeg'),
            types.Part.from_text(text="""
                Now, answer these questions:

                1. Is there a dog in the crate?
                2. If yes, is the dog sitting, standing or lying down?
                3. What is the probability (0.0 to 1.0) that the dog is panting? If it's not clear, respond with 0.0.

                Respond using JSON following the provided schema.
                Format your response as a valid JSON object that matches the DogAnalysis schema.
                """),
        ]
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=DogAnalysis,
        ),
    )

    # Handle the case where response.text might be None
    if response.text is None:
        raise ValueError("No response text received from the model")

    return DogAnalysis.model_validate_json(response.text)
