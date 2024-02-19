from django.db import models

class Incident(models.Model):
    """
    Model to represent an incident.
    
    Attributes:
        mac (models.CharField): MAC address involved in the incident.
        date (models.DateTimeField): Date and time when the incident occurred.
        class_field (models.CharField): Classification of the incident. 'class' is a reserved word in Python,
                                        hence 'class_field' is used and mapped to 'class' column in the database.
        evidence (models.TextField): Detailed evidence or description of the incident.
    """
    
    mac = models.CharField(max_length=17)  # Example format: "00:1B:44:11:3A:B7"
    date = models.DateTimeField()
    class_field = models.CharField(max_length=100, db_column='class')  # Mapping 'class_field' to 'class' DB column
    evidence = models.TextField()

    def __str__(self):
        """
        String representation of the Incident model.
        
        Returns:
            str: A string indicating the MAC address and the date of the incident.
        """
        return f"Incident {self.mac} on {self.date}"

