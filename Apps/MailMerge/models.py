from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SMTPSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    smtp_host = models.CharField(max_length=255, null=False, blank=False)
    smtp_port = models.IntegerField(default=587)  # Default SMTP port is usually 587 for TLS
    use_tls = models.BooleanField(default=True, null=False, blank=False)
    email_address = models.EmailField(null=False, blank=False)
    email_password = models.CharField(max_length=255, null=False, blank=False)  # 🔒 You can later encrypt this
    is_active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_address} ({self.smtp_host}:{self.smtp_port})"


class CSVUpload(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name