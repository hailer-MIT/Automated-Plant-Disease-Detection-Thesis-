from django.urls import path

from .views import predict_uploaded_image,get_all_plant_diseases,evaluate,edit_disease
urlpatterns = [
    path('predict', predict_uploaded_image, name='predict'),
    path('disease/edit/<int:disease_id>/', edit_disease, name='edit_disease'),
    path('diseases', get_all_plant_diseases, name='diseases'),
    path('evaluate', evaluate, name='evaluate'),
]