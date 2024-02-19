from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Incident
from .serializers import IncidentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class IncidentViewSet(viewsets.ViewSet):
    """
    A view set for creating incidents and retrieving them for dashboard purposes.
    """
    # Requires users to be authenticated to use any endpoint within this viewset
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Creates a new incident based on the provided data.
        """
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Msg_success': 'Incident reported successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def dashboard(self, request, day=None, month=None, year=None):
        """
        Custom action to retrieve incidents for a dashboard view, with optional
        filtering by day, month, and year through query parameters.
        """
        # Extracting query parameters for filtering
        day = request.query_params.get('day', 0)
        month = request.query_params.get('month', 0)
        year = request.query_params.get('year', 0)

        # Converting parameters to integers
        day = int(day)
        month = int(month)
        year = int(year)
        
        # Initializing the query
        query = Incident.objects.all()
        
        # Applying filters based on the provided parameters
        if year > 0:
            query = query.filter(date__year=year)
        if month > 0:
            query = query.filter(date__month=month)
        if day > 0:
            query = query.filter(date__day=day)
        
        # Serializing the data
        serializer = IncidentSerializer(query, many=True)
        
        # Returning the response
        return Response(serializer.data)
