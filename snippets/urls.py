from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    # NOTE: view を def で書くなら
    #       path('snippets/', views.snippet_list)
    #       こんな感じだけど、 class で定義した場合こうなる。
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)