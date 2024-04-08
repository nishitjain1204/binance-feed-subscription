from django.urls import path
from api.views.subscription_views import SubscriptionView , DeleteSubscriptionView
from api.views.user_views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('subscribe/', SubscriptionView.as_view(), name="subscribe"),
    path('unsubscribe/', DeleteSubscriptionView.as_view(), name="unsubscribe"),
]