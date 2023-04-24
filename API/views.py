from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getData(request):
    person = {
        'nombre':'miti',
        'edad':23
    }
    return Response(person)