# emails/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', SMTPListView.as_view(), name='smtp_list'),
    path('smtp/create/', SMTPCreateView.as_view(), name='smtp_create'),
    path('smtp/<int:pk>/', SMTPDetailView.as_view(), name='smtp_detail'),
    path('smtp/<int:pk>/edit/', SMTPUpdateView.as_view(), name='smtp_update'),
    path('smtp/<int:pk>/delete/', SMTPDeleteView.as_view(), name='smtp_delete'),
    path('send-emails/<int:smtp_id>/', SendBulkEmailView.as_view(), name='send_bulk_email'),
    path('upload-csv/', upload_csv, name='upload_csv'),
]
