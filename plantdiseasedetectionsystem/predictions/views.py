from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from predictions.models import PlantDisease  # Import your model
import tensorflow as tf
import numpy as np
import random
from PIL import Image
from django.conf import settings
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import matplotlib.pyplot as plt
import logging
import tempfile
import json
from django.shortcuts import get_object_or_404
logger = logging.getLogger(__name__)
model = None
IMAGE_SIZE = 256
BATCH_SIZE = 32
CHANNELS = 3
EPOCHS = 50
plantType=None
class_names=[]
dataset=None
results=[]
def load_model(plantType):
    global model
    if plantType == 'potato':
        print("potato")
        model_path = 'predictions/Aimodel/potato.keras'
    elif plantType == 'tomato':
        model_path = 'predictions/Aimodel/tomato.keras'
    elif plantType == 'apple':

        print("plant is ",plantType)
        model_path = 'predictions/Aimodel/model_apple.keras'
        print("model path",model_path)


    elif plantType == 'corn':
        
        model_path = 'predictions/Aimodel/model_Corn.keras'



    elif plantType == 'cactus':
        print("choosen is cactus please so model is not none ")
        model_path = 'predictions/Aimodel/model_cactus.keras'
        print("model path for cactus is",model_path)


    else:
        model_path = None
    try:
        if model_path is not None:
          
            model = tf.keras.models.load_model(model_path)
            print("model",model)

    except Exception as e:
        model = None

@csrf_exempt  # Disable CSRF protection for this view
def predict_uploaded_image(request):
    print("File comes from the flutter")
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        else:
            print("Image is provided")
        image_file = request.FILES['image']
        plant=request.POST.get('plant')
        if not plant:
            return JsonResponse({'error': 'No plant type provided.'}, status=400)
        else:
            print("Plant type is provided",plant)
        allowed_plants = ["potato", "tomato", "apple", "corn", "cactus"]
       
        if plant not in allowed_plants:
            return JsonResponse({'error': 'Invalid plant type use only potato,tomato,apple,corn,cactus.'}, status=400)
        
        plant_paths = {
                'potato': 'predictions/potato/Potato___Early_blight',
                'tomato': 'predictions/tomato/Tomato___Early_blight',
                'apple': 'predictions/apple/Apple___Apple_scab',
                'corn': 'predictions/corn/Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                'cactus': 'predictions/cactus/EarlyStage'
            }
        
        upload_folder = os.path.join(settings.MEDIA_ROOT, plant_paths[plant])
        print("upload_folder",upload_folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # Create 'uploads' folder inside 'media'

        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove the file
            except Exception as e:
                return JsonResponse({'error': f'Error deleting file: {e}'}, status=500)

        # Define the full image path
        image_path = os.path.join(upload_folder, image_file.name)

        # Save the image in the 'uploads' folder
        with default_storage.open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

       

        print("i reach here ",plant)

        data_directory = os.path.join(settings.MEDIA_ROOT, 'predictions', plant)
        print("data_directory",data_directory)
        global dataset
        dataset= tf.keras.preprocessing.image_dataset_from_directory(
            data_directory,
            shuffle = True,
            image_size = (IMAGE_SIZE, IMAGE_SIZE),
            batch_size = BATCH_SIZE
        )


        print("dataset==",dataset)

        global class_names
        class_names = dataset.class_names
        print("class_names==",class_names)
        # Ensure the folder exists, create it if it doesn't
        global model
        model=None
        load_model(plant)
        # Loop through the dataset
        results=[]
        for images, labels in dataset.take(1):
            for i in range(1):
                image_array = images[i].numpy()
                print("image_array", image_array)

                # Predict the class and confidence
                predicted_class, confidence = predict(model, image_array)
                print("predicted class and confidence are:", predicted_class, confidence)

                # Get recommendation and cause directly from the function
                recommendation_and_cause = get_recommendation_from_db(plant, predicted_class)

                # Build the result dictionary
                result = {
                    'plant': plant,
                    'predicted_class': predicted_class,
                    'confidence': float(confidence)  # Ensure confidence is a float for JSON serialization
                }
                # Check if recommendation and cause were found
                if "error" not in recommendation_and_cause:
                    result['recommendation'] = recommendation_and_cause["recommendation"]
                    result['cause'] = recommendation_and_cause["cause"]
                else:
                    result['error'] = recommendation_and_cause["error"]

                # Append the result to the results list
                results.append(result)
                print("successfully responded to the cause and disease and recomendation.")
        # Return JSON response
        return JsonResponse({'results': results}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def evaluate(request):
    if request.method == 'GET':
        if model is None:
            load_model("apple")
            data_directory = os.path.join(settings.MEDIA_ROOT, 'predictions', 'apple')
            print("data_directory",data_directory)
            global dataset
            dataset= tf.keras.preprocessing.image_dataset_from_directory(
                data_directory,
                shuffle = True,
                image_size = (IMAGE_SIZE, IMAGE_SIZE),
                batch_size = BATCH_SIZE
            )
            global class_names
            class_names = dataset.class_names
            for images, labels in dataset.take(1):
               for i in range(1):  # Limiting to 9 images
                # Prepare image for prediction
                    image_array = images[i].numpy()
                    predicted_class, confidence = predict(model, image_array)
                    actual_class = class_names[labels[i].numpy()]
                    # Collect results
                    results.append({
                        'actual_class': actual_class,
                        'predicted_class': predicted_class,
                        'confidence': float(confidence)  # Ensure confidence is a float for JSON serialization
                    })

        return JsonResponse({'results': results}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
                            
def predict(model, img):
    if not isinstance(img, np.ndarray):
        img_array = tf.keras.img_to_array(img)
    else:
        img_array = img
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    print("Predict",predictions)
    
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)

    return predicted_class, confidence

def get_all_plant_diseases(request):
    try:
        # Fetch all records from the PlantDisease model
        diseases = PlantDisease.objects.all()

        # Prepare a list to hold the results
        disease_list = []

        # Loop through the queryset and create a dictionary for each entry
        for disease in diseases:
            disease_list.append({
                'id':disease.id,
                'cause':disease.cause,
                'plant_type': disease.plant_type,
                'disease_type': disease.disease_type,
                'recommendation': disease.recommendation,
            })

        # Return the list of plant diseases as a JSON response
        return JsonResponse({'diseases': disease_list}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def get_recommendation_from_db(plant_type, disease_type):
    try:
        # Convert plant_type and disease_type to lowercase for the query
        plant_type_lower = plant_type.lower()
        disease_type_lower = disease_type.lower()

        # Query the database for the recommendation with lowercased values
        disease_record = PlantDisease.objects.get(
            plant_type__iexact=plant_type_lower,
            disease_type__iexact=disease_type_lower,
        )
        return {
            "recommendation": disease_record.recommendation,
            "cause": disease_record.cause
        }
    except PlantDisease.DoesNotExist:
        return f"No recommendation found for {disease_type} in {plant_type}."
    except Exception as e:
        return f"An error occurred: {str(e)}"


@csrf_exempt
def edit_disease(request, disease_id):
    # Check if the request method is POST
    if request.method == 'POST':
        try:
            # Get the disease instance based on the provided ID
            disease = get_object_or_404(PlantDisease, id=disease_id)

            # Load the JSON data from the request body
            data = json.loads(request.body)

            # Update the disease_type field
            disease.cause = data.get('cause', disease.cause)

            # Save the changes to the database
            disease.save()

            # Return a success response
            return JsonResponse({'message': 'Disease updated successfully!', 'disease': {'id': disease.id, 'plant_type': disease.plant_type, 'disease_type': disease.disease_type, 'recommendation': disease.recommendation}}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method. Please use POST.'}, status=405)
