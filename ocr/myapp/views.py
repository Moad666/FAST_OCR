from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import OCRResult,OCRTask,OCRTaskk
from .serializers import OCRResultSerializer,OCRTaskSerializer,OCRTaskkSerializer
import pytesseract
from PIL import Image
import cv2
import easyocr
from PIL import Image
import numpy as np
from rest_framework import status


class OCRView(generics.CreateAPIView):
    queryset = OCRResult.objects.all()
    serializer_class = OCRResultSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        image = self.request.data['image']
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        serializer.save(image=image, text=text)

class OCRTaskCreateView(generics.CreateAPIView):
    queryset = OCRTask.objects.all()
    serializer_class = OCRTaskSerializer

    def perform_create(self, serializer):
        # Retrieve the file-like object from the request
        image = self.request.FILES.get('image')

        # Convert the image to a NumPy array
        image_array = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

        # Use OpenCV for text zone detection
        text_zones = self.detect_text_zones(image_array)

        result_text = ""
        for zone in text_zones:
            # Extract the region from the original image based on the bounding box
            x, y, w, h = zone
            text_zone = image_array[y:y+h, x:x+w]

            # Convert the text zone to RGB (PIL format) for pytesseract
            text_zone_rgb = cv2.cvtColor(text_zone, cv2.COLOR_BGR2RGB)

            # Use pytesseract for OCR on the text zone
            text = pytesseract.image_to_string(text_zone_rgb)
            result_text += text + '\n'

        serializer.save(result_text=result_text)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def detect_text_zones(self, image_array):
        # Convert the image to grayscale for text detection
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # Apply an appropriate preprocessing (e.g., thresholding, edge detection)
        # This might vary based on the type of images you are processing
        _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Extract the bounding boxes of the contours as text zones
        text_zones = [cv2.boundingRect(contour) for contour in contours]

        # Return the bounding boxes as text zones
        return text_zones


    def perform_create(self, serializer):
        image = self.request.data['image']
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        serializer.save(image=image, text=text)

class OCRTaskkCreateView(generics.CreateAPIView):
    queryset = OCRTaskk.objects.all()
    serializer_class = OCRTaskkSerializer

    def perform_create(self, serializer):
            # Retrieve the file-like object from the request
            image = self.request.FILES.get('image')

            # Convert the image to a NumPy array
            image_array = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

            # Use OpenCV for text zone detection
            text_zones = self.detect_text_zones(image_array)

            result_text = []
            array_date = []
            array_cin = []
            array_capital_word = []

            for zone in text_zones:
                # Extract the region from the original image based on the bounding box
                x, y, w, h = zone
                text_zone = image_array[y:y + h, x:x + w]

                # Convert the text zone to RGB (PIL format) for pytesseract
                text_zone_rgb = cv2.cvtColor(text_zone, cv2.COLOR_BGR2RGB)

                # Use pytesseract for OCR on the text zone
                text = pytesseract.image_to_string(text_zone_rgb)

                # Split the text into words
                words = text.split()

                for word in words:
                    # Save words containing numbers and having a length of 5 or more characters
                    if any(char.isdigit() for char in word) and len(word) >= 5:
                        result_text.append(word)

                        # Check if the word matches a date pattern
                        if re.match(r'\d{2}[./,]\d{2}[./,]\d{4}', word):
                            array_date.append(word)
                            # Extract 5 words before the first word in array_date
                            keyword_index = words.index(word)
                            start_index = max(keyword_index - 5, 0)
                            five_words_before = words[start_index:keyword_index]
                            
                            # Filter and get only capital words without numbers
                            capital_words_before = [word for word in five_words_before if not any(char.isdigit() for char in word) and word.isupper()]
                            
                            array_capital_word.extend(capital_words_before)

                        # Check if the word matches a CIN pattern
                        elif re.match(r'[A-Z]+\d+', word):
                            array_cin.append(word)

                        # Check if the word is in all capital letters
                        elif word.isupper():
                            array_capital_word.append(word)

            # Join the words into a formatted result text
            formatted_result_text = ' '.join(result_text)

            serializer.save(
                result_text=text,
                array_date=array_date,
                array_cin=array_cin,
                array_capital_word=array_capital_word
            )
            print(text)
            print(array_date)
            print(array_cin)
            print(array_capital_word)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def detect_text_zones(self, image_array):
        # Convert the image to grayscale for text detection
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # Apply an appropriate preprocessing (e.g., thresholding, edge detection)
        # This might vary based on the type of images you are processing
        _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Extract the bounding boxes of the contours as text zones
        text_zones = [cv2.boundingRect(contour) for contour in contours]

        # Return the bounding boxes as text zones
      
        return text_zones