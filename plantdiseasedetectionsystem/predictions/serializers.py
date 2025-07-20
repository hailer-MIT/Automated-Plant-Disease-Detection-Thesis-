# predictions/serializers.py

from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()  # Assuming you're uploading an image
