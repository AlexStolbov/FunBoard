from django.urls import path

from .views import PostList, PostDetail, CommentCreate, CommentApprove
from .views import comment_approve, comment_delete

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    # просмотр статьи
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    # заполнить или записать отклик
    path('<int:pk>/comment/', CommentCreate.as_view(), name='post_comment'),
    path('<int:pk>/approve/', CommentApprove.as_view()),
    path('<int:pk>/set_approve/', comment_approve),
    path('<int:pk>/set_delete/', comment_delete)
]
