from django.urls import path
from yousta.views import *




urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("add/",CategoryCreateView.as_view(),name="category-add"),
    path("categories/<int:pk>/remove/",remove_category,name="remove-category"),
    path("cloths/add",ClothCreateView.as_view(),name="cloth-add"),
    path("cloths/all",ClothListView.as_view(),name="cloth-list"),
    path("cloths/<int:pk>/change",ClothUpdateView.as_view(),name="cloth-change"),
    path("cloths/<int:pk>/remove",remove_clothView,name="cloth-remove"),
    path("cloths/<int:pk>/varients/add",ClothVarientCreateView.as_view(),name="add-varient"),
    path("cloths/<int:pk>/",ClothDetailView.as_view(),name="cloth-detail"),
    path("varient/<int:pk>/change/",ClothVarientUpdateView.as_view(),name="update-varient"),
    path("varients/<int:pk>/remove",remove_varient,name="remove-varient"),
    path("varients/<int:pk>/offer/add",OfferCreateView.as_view(),name="offer-add"),
    path("varients/<int:pk>/offers/remove",remove_offer,name="remove-offer"),
    path("logout",sign_out_view,name="signout"),
    path("index/",IndexView.as_view(),name="index"),
    path("userindex/",UserIndexView.as_view(),name="user-index"),
    path("profile/<int:pk>",ProfileView.as_view(),name="user-profile"),
    path("usercloths/<int:pk>/",ClothUserDetailView.as_view(),name="user-clothdetail"),
    path('usercart/add/<int:pk>/', CartAddView.as_view(), name='cart_add'),
    path('user/cart/<int:pk>/',CartView.as_view(),name="user-cart")



]