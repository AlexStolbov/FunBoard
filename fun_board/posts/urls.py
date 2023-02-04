from django.urls import path

from .views import PostList, PostCreate, PostDetail, CommentCreate, CommentApprove
from .views import comment_approve, comment_delete, subscribe_on, subscribe_off

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    # создание объявления
    path('create/', PostCreate.as_view(), name='post_create'),
    # просмотр объявления
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    # заполнить или записать отклик
    path('<int:pk>/comment/', CommentCreate.as_view(), name='post_comment'),
    path('<int:pk>/approve/', CommentApprove.as_view()),
    path('<int:pk>/set_approve/', comment_approve),
    path('<int:pk>/set_delete/', comment_delete),
    path('subscribe_on/', subscribe_on),
    path('subscribe_off/', subscribe_off),
]
