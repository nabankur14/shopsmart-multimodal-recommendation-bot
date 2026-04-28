from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from config import VISION_ENDPOINT, VISION_KEY

client = ImageAnalysisClient(endpoint=VISION_ENDPOINT,
                              credential=AzureKeyCredential(VISION_KEY))

async def analyse_image(image_url: str) -> str:
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS]
    )
    tags = ", ".join([t.name for t in result.tags.list[:10]])
    return f"Image tags: {tags}"

async def analyse_image_bytes(image_data: bytes) -> str:
    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS]
    )
    tags = ", ".join([t.name for t in result.tags.list[:10]])
    return f"Image tags: {tags}"
