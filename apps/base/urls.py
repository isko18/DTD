from django.urls import path, include

from apps.base import views
from apps.base.views import (AndroidVersionControlAPIView, IOSVersionControlAPIView,
                             PrivacyPolicyAPIView, OfferAgreementAPIView)

urlpatterns = [
    path('banners/', views.BannerListView.as_view(), name='banners'),
    path('banners/<int:pk>/', views.BannerDetailView.as_view(), name='banner_detail'),
    path('support_and_faq/', views.SupportFAQView.as_view(), name='support_and_faq'),
    path('about_app/', views.AboutAppView.as_view(), name='about_app'),
    path('ad_page/', views.AdPageView.as_view(), name='ad_page'),
    path('privacy_policy/', PrivacyPolicyAPIView.as_view(), name='privacy_policy'),
    path('offer_agreement/', OfferAgreementAPIView.as_view(), name='offer_agreement'),
    path('android/', AndroidVersionControlAPIView.as_view()),
    path('ios/', IOSVersionControlAPIView.as_view()),

]
