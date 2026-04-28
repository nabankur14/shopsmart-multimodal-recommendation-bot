import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import base64
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from config import VISION_ENDPOINT, VISION_KEY

async def test_vision():
    test_key = VISION_KEY
    print(f"Testing Vision with key: {test_key[:5]}...{test_key[-5:]}")
    print(f"Endpoint: {VISION_ENDPOINT}")
    
    client = ImageAnalysisClient(endpoint=VISION_ENDPOINT, credential=AzureKeyCredential(test_key))
    
    # Simple dummy image (1x1 pixel black dot)
    dummy_image = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    
    try:
        from azure.ai.vision.imageanalysis.models import VisualFeatures
        result = client.analyze(
            image_data=dummy_image,
            visual_features=[VisualFeatures.TAGS]
        )
        print(f"Vision Success! Result: {', '.join([t.name for t in result.tags.list])}")
    except Exception as e:
        print(f"Vision failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_vision())
