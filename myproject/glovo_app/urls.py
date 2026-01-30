from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileListAPIView,UserProfileDetailAPIView,ContactViewSet,CourierViewSet,CategoryListAPIView,CategoryDetailAPIView,
                    StoreListAPIView,StoreDetailAPIView,ProductListAPIView,ProductDetailAPIView,AddressViewSet,
                    ReviewEditView,ReviewListAPIView,OrderViewSet,ProductCreateAPIView,UserLoginView , UserRegisterView , LogoutView)

router = routers.DefaultRouter()
router.register(r'courier',CourierViewSet)
router.register(r'contact',ContactViewSet)
router.register(r'address',AddressViewSet)
router.register(r'order',OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('product_create', ProductCreateAPIView.as_view(), name='product_generate'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('review/', ReviewListAPIView.as_view(), name='review'),
    path('review/<int:pk>/', ReviewEditView.as_view(), name='edit_review'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
    ]