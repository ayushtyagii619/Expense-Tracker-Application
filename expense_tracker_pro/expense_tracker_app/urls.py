from django.urls import path
from .views import RegisterApiView, LoginApiView,ExpenseCreateListApiView,ExpenseAnalyticsApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('expenses/',ExpenseCreateListApiView.as_view()),
    path('expenses/analytics/', ExpenseAnalyticsApiView.as_view()),
]
