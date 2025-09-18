from django.urls import path
from . import views

app_name = 'updates'

urlpatterns = [
    path('add/<int:activity_pk>/', views.UpdateCreateView.as_view(), name='update_add'),
]
