# emails/forms.py
from django import forms
from .models import CSVUpload, SMTPSetting

class SMTPSettingForm(forms.ModelForm):
    class Meta:
        model = SMTPSetting
        fields = 'smtp_host', 'smtp_port', 'use_tls', 'email_address', 'email_password', 'is_active'
        widgets = {
            'email_password': forms.PasswordInput(render_value=True)
        }

class BulkEmailForm(forms.Form):
    smtp_setting = forms.ModelChoiceField(
        queryset=SMTPSetting.objects.all(),
        label="Select SMTP Account",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    csv_file = forms.FileField(label="Upload CSV (first_name, last_name, email)")
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        help_text='Use {{ first_name }} and {{ last_name }} as placeholders.'
    )

    
class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = CSVUpload
        fields = ['name', 'file']