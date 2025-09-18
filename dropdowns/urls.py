from django.urls import path
from . import views

app_name = 'dropdowns'

urlpatterns = [
    path('', views.DropdownListView.as_view(), name='dropdown_list'),
    path('nodename/add/', views.NodeNameCreateView.as_view(), name='nodename_add'),
    path('nodename/<int:pk>/edit/', views.NodeNameUpdateView.as_view(), name='nodename_edit'),
    path('nodename/<int:pk>/delete/', views.NodeNameDeleteView.as_view(), name='nodename_delete'),
    path('activitytype/add/', views.ActivityTypeCreateView.as_view(), name='activitytype_add'),
    path('activitytype/<int:pk>/edit/', views.ActivityTypeUpdateView.as_view(), name='activitytype_edit'),
    path('activitytype/<int:pk>/delete/', views.ActivityTypeDeleteView.as_view(), name='activitytype_delete'),
    path('status/add/', views.StatusCreateView.as_view(), name='status_add'),
    path('status/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_edit'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]
