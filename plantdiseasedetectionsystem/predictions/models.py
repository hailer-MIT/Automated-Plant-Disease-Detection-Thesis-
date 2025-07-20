from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

plant_disease_recommendations = {
    "apple": {
        "apple scab": "Remove infected leaves and apply fungicides.",
        "fire blight": "Prune infected branches and avoid excessive nitrogen fertilization.",
        "powdery mildew": "Use sulfur-based fungicides and prune to improve air circulation.",
        "black root": "Improve soil drainage and avoid overwatering.",
        "cedar apple rust": "Apply fungicides early in the season and remove nearby cedar trees if possible."
    },
    "cherry": {
        "brown rot": "Remove infected fruit and apply fungicides before and after bloom.",
        "cherry leaf spot": "Apply fungicides in spring and remove fallen leaves."
    },
    "corn": {
        "northern corn leaf blight": "Use resistant varieties and apply fungicides.",
        "gray leaf spot": "Rotate crops and use fungicides.",
        "common rust": "Use resistant hybrids and apply fungicides if necessary.",
        "ceracospora leaf spot": "Plant resistant varieties and apply fungicides."
    },
    "grape": {
        "downy mildew": "Use fungicides and improve vineyard air circulation.",
        "powdery mildew": "Apply sulfur or fungicide sprays and prune regularly."
    },
    "orange": {
        "citrus canker": "Prune infected branches and apply copper sprays.",
        "greening disease (haunglongbing)": "Remove infected trees and control insect vectors.",
        "black root": "Improve soil drainage and avoid waterlogging.",
        "black measles": "Remove infected vines and apply fungicides.",
        "leaf blight (isariposis leaf spot)": "Apply fungicides and maintain proper tree hygiene."
    },
    "peach": {
        "peach leaf curl": "Apply fungicides before bud break in early spring.",
        "brown rot": "Remove infected fruit and apply pre-harvest fungicides.",
        "bacterial spot": "Use copper-based sprays and plant resistant varieties."
    },
    "pepper": {
        "bacterial spot": "Use copper sprays and resistant varieties.",
        "anthracnose": "Remove infected plants and apply fungicides."
    },
    "potato": {
        "potato___late_blight": "Apply fungicides and avoid overhead watering.",
        "potato___healthy": "Use resistant varieties and avoid alkaline soil.",
        "potato___early_blight": "Use resistant varieties and apply fungicides regularly."
    },
    "raspberry": {
        "cane blight": "Prune infected canes and apply fungicides.",
        "gray mold": "Remove infected fruit and improve air circulation."
    },
    "soybean": {
        "soybean rust": "Apply fungicides and rotate crops.",
        "sudden death syndrome": "Use resistant varieties and rotate crops."
    },
    "squash": {
        "powdery mildew": "Use fungicides and plant resistant varieties.",
        "downy mildew": "Apply fungicides and improve air circulation."
    },
    "strawberry": {
        "gray mold": "Use fungicides and remove infected fruit.",
        "powdery mildew": "Apply sulfur-based fungicides and improve air circulation.",
        "leaf scorch": "Remove affected leaves and apply fungicides."
    },
    "tomato": {
        "late blight": "Apply fungicides and remove infected plants.",
        "early blight": "Use resistant varieties and prune lower leaves.",
        "bacterial spot": "Apply copper-based bactericides and remove infected plants.",
        "leaf mold": "Ensure proper ventilation and use fungicides.",
        "septoria leaf spot": "Use fungicides and remove infected leaves.",
        "spider mites": "Use miticides or insecticidal soap to control mites.",
        "two-spotted spider mite": "Apply insecticidal soap or miticides.",
        "target spot": "Apply fungicides and remove affected leaves.",
        "tomato mosaic virus": "Remove infected plants and control insect vectors."
    },
    "onion": {
        "downy mildew": "Apply fungicides and ensure good drainage.",
        "neck rot": "Store onions in dry conditions and treat with fungicides."
    },
    "cactus": {
        "EarlyStage": "Use insecticidal soap or neem oil.",
        "LateStage": "Repeat insecticidal treatments more frequently and remove heavily infested parts if possible.",
        "Old_Dead": "Remove dead plant material to prevent fungal growth and improve hygiene."
    }
}

class PlantDisease(models.Model):
    plant_type = models.CharField(max_length=100)
    disease_type = models.CharField(max_length=100)
    recommendation = models.TextField()
    cause = models.TextField(default="Unknown cause")

    def __str__(self):
        return f"{self.plant_type} - {self.disease_type}"

    class Meta:
        verbose_name = "Plant Disease"
        verbose_name_plural = "Plant Diseases"


# Signal to insert data after migration
@receiver(post_migrate)
def insert_plant_disease_data(sender, **kwargs):
    PlantDisease = apps.get_model('predictions', 'PlantDisease')
    for plant, diseases in plant_disease_recommendations.items():
        for disease, recommendation in diseases.items():
            # Check if it already exists to avoid duplicates
            if not PlantDisease.objects.filter(plant_type=plant, disease_type=disease).exists():
                PlantDisease.objects.create(
                    plant_type=plant,
                    # Use default value if 'cause' is not provided
                    disease_type=disease,
                    recommendation=recommendation
                )
