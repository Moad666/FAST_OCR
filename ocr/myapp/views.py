from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import OCRResult
from .serializers import OCRResultSerializer
import pytesseract
from PIL import Image

class OCRView(generics.CreateAPIView):
    queryset = OCRResult.objects.all()
    serializer_class = OCRResultSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        image = self.request.data['image']
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        serializer.save(image=image, text=text)

