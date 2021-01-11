from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.views.decorators.csrf import requires_csrf_token
from django.http import (
    HttpResponseServerError,
)

# NOTE: 【T2】で追加。
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# NOTE: 【T3】で追加。
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics

# NOTE: 【T4】で追加。
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

# NOTE: 【T5】で追加。
from rest_framework import renderers
from rest_framework.reverse import reverse

# NOTE: 【T6】で追加。
from rest_framework import viewsets
from rest_framework.decorators import action


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# NOTE: @api_view(['GET', 'POST']) 付きの def で書いてしまうと
#       if request.method == 'GET':
#       elif request.method == 'POST':
#       でリクエスト分けをすることになってしまいます。 class のほうが洗練されています。
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    List all snippets, or create a new snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # NOTE: mixins や queryset serializer_class を使うことで、
    #       この↓メソッドがめちゃカンタン↑になります。【T3】
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     # NOTE: JsonResponse(serializer.data, safe=False) よりこっちのほうがいい。
    #     #       Response で返すことによって web 画面に REST framework の view が出るようになる。
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # NOTE: get に同じ。
    # def post(self, request, format=None):
    #     # data = JSONParser().parse(request)
    #     # serializer = SnippetSerializer(data=data)
    #     # NOTE: 以上の処理を request.data で簡略可。
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     # NOTE: status=400 -> status=status.HTTP_400_BAD_REQUEST こっちのほうがいい。
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NOTE: ↑と同じく @api_view(['GET', 'PUT', 'DELETE']) 付きの def では書かない。
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # NOTE: mixin を利用してこの↑ように書くことで、
    #       こんな↓処理を全部すっ飛ばして書ける。【T3】
    #       ここ変わりすぎてわけわかめやわ。

    # def get_object(self, pk):
    #     try:
    #         return Snippet.objects.get(pk=pk)
    #     except Snippet.DoesNotExist:
    #         # NOTE: status=404 -> status.HTTP_404_NOT_FOUND こっちのほうがいい。
    #         #       が、 Response(status=status.HTTP_404_NOT_FOUND) よりも
    #         #       raise Http404 のほうがさらによい。
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# NOTE: てかさらにここ↓まで簡略化が可能。これが T3 の奥義。
#       generic がツヨすぎる。
#       【T3】終幕。
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):

    # NOTE: print が App Service で機能するかどうか確かめるために print しています。
    import traceback
    print(traceback.format_exc())
    print('500 Error happened!(Japanese letters garble.)')
    # return HttpResponseServerError('<h1>Server Error (500)</h1>')

    # DEBUG = True と同様の画面を出します。
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
