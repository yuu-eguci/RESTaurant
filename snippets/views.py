from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# NOTE: 【T2】で追加。
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# NOTE: 【T3】で追加。
from rest_framework.views import APIView
from django.http import Http404


# NOTE: @api_view(['GET', 'POST']) 付きの def で書いてしまうと
#       if request.method == 'GET':
#       elif request.method == 'POST':
#       でリクエスト分けをすることになってしまいます。 class のほうが洗練されています。
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # NOTE: JsonResponse(serializer.data, safe=False) よりこっちのほうがいい。
        #       Response で返すことによって web 画面に REST framework の view が出るようになる。
        return Response(serializer.data)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        # serializer = SnippetSerializer(data=data)
        # NOTE: 以上の処理を request.data で簡略可。
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # NOTE: status=400 -> status=status.HTTP_400_BAD_REQUEST こっちのほうがいい。
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NOTE: ↑と同じく @api_view(['GET', 'PUT', 'DELETE']) 付きの def では書かない。
class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # NOTE: status=404 -> status.HTTP_404_NOT_FOUND こっちのほうがいい。
            #       が、 Response(status=status.HTTP_404_NOT_FOUND) よりも
            #       raise Http404 のほうがさらによい。
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)