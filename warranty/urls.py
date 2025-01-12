from django.urls import path
from .views import Level2SubmissionView,Level1ListCreateView, Level1DetailView, Level2DetailView,Level2ListCreateView

urlpatterns = [
    path('level2/submit/', Level2SubmissionView.as_view(), name='level2-submit'),
    path('level1/', Level1ListCreateView.as_view(), name='level1-list-create'),
    path('level1/<int:pk>/', Level1DetailView.as_view(), name='level1-detail'),
    path('level2/', Level2ListCreateView.as_view(), name='level2-list-create'),
    path('level2/<int:pk>/', Level2DetailView.as_view(), name='level2-detail'),
]
