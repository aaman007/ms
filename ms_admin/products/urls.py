from django.urls import path

from products.views import ProductViewSet, UserAPIView

urlpatterns = [
    path('', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user/', UserAPIView.as_view())
]
