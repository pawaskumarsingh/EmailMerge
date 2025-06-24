# emails/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', login_required(SMTPListView.as_view()), name='smtp_list'),
    path('smtp/create/', login_required(SMTPCreateView.as_view()), name='smtp_create'),
    path('smtp/<int:pk>/', login_required(SMTPDetailView.as_view()), name='smtp_detail'),
    path('smtp/<int:pk>/edit/', login_required(SMTPUpdateView.as_view()), name='smtp_update'),
    path('smtp/<int:pk>/delete/', login_required(SMTPDeleteView.as_view()), name='smtp_delete'),
    path('send-emails/<int:smtp_id>/', login_required(SendBulkEmailView.as_view()), name='send_bulk_email'),
    path('upload-csv/', login_required(upload_csv), name='upload_csv'),
]
