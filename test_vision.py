from azure.ai.vision.imageanalysis import ImageAnalysisClient
print("Methods in ImageAnalysisClient:")
print([m for m in dir(ImageAnalysisClient) if not m.startswith('_')])
