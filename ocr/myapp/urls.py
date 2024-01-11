from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import OCRView,OCRTaskCreateView,OCRTaskkCreateView

urlpatterns = [
    path('ocr/', OCRView.as_view(), name='ocr-view'),
    path('opencv/', OCRTaskCreateView.as_view(), name='ocr-task-create'),
    path('opencv_task/', OCRTaskkCreateView.as_view(), name='ocr-task-create-task'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)