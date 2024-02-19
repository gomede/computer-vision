from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Incident model.

    The serializer converts instances of the Incident model to and from JSON format,
    allowing for easy serialization of querysets and model instances to JSON and
    deserialization of JSON back to model instances.

    Attributes:
        Meta: A class that defines the serializer behavior and specifies the model
              to serialize and the fields to include in the serialized data.
    """
    
    class Meta:
        model = Incident  # Specifies the model associated with this serializer.
        fields = ['mac', 'date', 'class_field', 'evidence']  # Fields to be included in the serialization.
