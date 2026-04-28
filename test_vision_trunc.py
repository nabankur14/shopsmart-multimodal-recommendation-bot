import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from helpers.vision_helper import analyse_image_bytes
import base64

async def test_vision():
    # Attempting to use the first 32 characters of the provided key
    test_key = "4j75HVUGaHy5gOvdYU6tupPaVTltXwMI"
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.core.credentials import AzureKeyCredential
    from config import VISION_ENDPOINT
    
    client = ImageAnalysisClient(endpoint=VISION_ENDPOINT, credential=AzureKeyCredential(test_key))
    
    # Simple dummy image (1x1 pixel black dot)
    dummy_image = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    
    try:
        from azure.ai.vision.imageanalysis.models import VisualFeatures
        result = client.analyze(
            image_data=dummy_image,
            visual_features=[VisualFeatures.CAPTION]
        )
        print(f"Vision result: {result.caption.text}")
    except Exception as e:
        print(f"Vision failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_vision())
