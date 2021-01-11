"""RESTaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from snippets import views
from shuumulator import views as shuumulator_views
# from snippets.views import SnippetViewSet, UserViewSet, api_root, my_customized_server_error
from rest_framework import renderers

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Create a router and register our viewsets with it.
# NOTE: view クラスではなく ViewSet を使うことでこういうやり方ができる。
router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)
router.register(r'stock', shuumulator_views.StockViewSet)
router.register(r'tradingrecord', shuumulator_views.TradingRecordViewSet)
router.register(r'trader', shuumulator_views.TraderViewSet)

# NOTE: ViewSet を使って↑のように書くことで、これが全部省略できる。
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # NOTE: ViewSet を使って↑のように書くことで、これが全部省略できる。
    # path('', api_root),
    # path('snippets/', snippet_list, name='snippet-list'),
    # path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    # path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    # path('users/', user_list, name='user-list'),
    # path('users/<int:pk>/', user_detail, name='user-detail'),
    # NOTE: これがないと画面に login のリンクすら出ない。
    path('api-auth/',
         include('rest_framework.urls',
                 namespace='rest_framework'),
         ),
    path('commands/samplecommand/', views.call_samplecommand),
    path('commands/executetrade/', shuumulator_views.call_executetrade),
]

handler500 = views.my_customized_server_error
