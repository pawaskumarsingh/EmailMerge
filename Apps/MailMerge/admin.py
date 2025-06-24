from django.contrib import admin
from .models import SMTPSetting, CSVUpload

# Register your models here.

@admin.register(SMTPSetting)

class SMTPSettingAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'smtp_host', 'smtp_port', 'use_tls', 'is_active', 'created_at')
    search_fields = ('email_address', 'smtp_host')
    list_filter = ('use_tls', 'is_active')
    ordering = ('-created_at',) 
    
@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'uploaded_at')
    search_fields = ('name',)
    ordering = ('-uploaded_at',)
# This file is used to register models with the Django admin interface.

# By registering the models here, they will be available in the admin panel
# for management, allowing you to add, edit, and delete instances of these models.      
