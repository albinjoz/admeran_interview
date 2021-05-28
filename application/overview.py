from application.models import *

from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overview_snippet(request):
    total_count = Snippet.objects.count()
    snippet_dict = {}  
    snippet_list = Snippet.objects.all()
    temp_list = []
    domain = request.META['HTTP_HOST']
    for snippet in snippet_list:
        temp_dict = {}
        temp_dict['link'] = "{}/snippet/{}".format(domain, snippet.id)
        temp_dict['snippets'] =model_to_dict(snippet)
        temp_list.append(temp_dict)
    snippet_dict['total_count'] = total_count
    snippet_dict['snippets'] = temp_list

    return Response(snippet_dict, status=status.HTTP_200_OK)