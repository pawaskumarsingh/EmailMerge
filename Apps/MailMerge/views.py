# emails/views.py
import csv
import smtplib
import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import SMTPSetting
from .forms import CSVUploadForm, SMTPSettingForm
from django.template import Template, Context
from .forms import BulkEmailForm
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from smtplib import SMTPRecipientsRefused
from django.template.loader import render_to_string
from concurrent.futures import ThreadPoolExecutor, as_completed

def setting_obj(request):
    if request.user.is_authenticated:
        settings = SMTPSetting.objects.filter(is_active=True, user=request.user)
    else:
        settings = SMTPSetting.objects.none()  # Return an empty queryset
    return settings


class SMTPListView(View):
    def get(self, request):
        settings = setting_obj(request)
        return render(request, 'emails/smtp_list.html', {'settings': settings, 'smtp_settings':settings})


class SMTPDetailView(View):
    def get(self, request, pk):
        settings = setting_obj(request)
        setting = get_object_or_404(SMTPSetting, pk=pk)
        return render(request, 'emails/smtp_detail.html', {'setting': setting,  'smtp_settings': settings})

class SMTPCreateView(View):
    def get(self, request):
        settings = setting_obj(request)
        form = SMTPSettingForm()
        return render(request, 'emails/smtp_form.html', {'form': form, 'title': 'Add SMTP Setting',  'smtp_settings': settings})

    def post(self, request):
        settings = setting_obj(request)
        form = SMTPSettingForm(request.POST)
        if form.is_valid(commit=False):
            form.instance.user = request.user
            form.instance.is_active = True  # Default to active
            form.save()
            return redirect('smtp_list')
        return render(request, 'emails/smtp_form.html', {'form': form, 'title': 'Add SMTP Setting', 'smtp_settings': settings})

class SMTPUpdateView(View):
    def get(self, request, pk):
        settings = setting_obj(request)
        setting = get_object_or_404(SMTPSetting, pk=pk)
        form = SMTPSettingForm(instance=setting)
        return render(request, 'emails/smtp_form.html', {'form': form, 'title': 'Edit SMTP Setting', 'smtp_settings': settings})

    def post(self, request, pk):
        setting = get_object_or_404(SMTPSetting, pk=pk)
        settings = setting_obj(request)
        form = SMTPSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('smtp_list')
        return render(request, 'emails/smtp_form.html', {'form': form, 'title': 'Edit SMTP Setting', 'smtp_settings': settings})

class SMTPDeleteView(View):
    def get(self, request, pk):
        settings = setting_obj(request)
        setting = get_object_or_404(SMTPSetting, pk=pk)
        return render(request, 'emails/smtp_confirm_delete.html', {'setting': setting, 'smtp_settings': settings})

    def post(self, request, pk):
        setting = get_object_or_404(SMTPSetting, pk=pk)
        setting.delete()
        return redirect('smtp_list')


# class SendBulkEmailView(View):
#     template_name = 'emails/send_bulk_email.html'

#     def get(self, request):
#         form = BulkEmailForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = BulkEmailForm(request.POST, request.FILES)
#         if not form.is_valid():
#             return render(request, self.template_name, {'form': form})

#         smtp = form.cleaned_data['smtp_setting']
#         subject_template = form.cleaned_data['subject']
#         message_template = form.cleaned_data['message']
#         csv_file = request.FILES['csv_file']

#         # Parse CSV rows
#         decoded_file = csv_file.read().decode('utf-8').splitlines()
#         reader = list(csv.DictReader(decoded_file))

#         sent_count = 0
#         failed_emails = []
#         lock = threading.Lock()

#         def send_email(row):
#             email_to = row.get('email', '').strip()

#             if not email_to:
#                 return "Missing email"

#             try:
#                 # Prepare subject and message
#                 context = Context(row)
#                 subject = Template(subject_template).render(context).strip()
#                 message_body = Template(message_template).render(context)

#                 # Prepare context for rendering HTML email template
#                 context_data = {
#                     **row,
#                     'message': message_body
#                 }

#                 html_content = render_to_string("emails/email_template.html", context_data)
#                 text_content = strip_tags(html_content)

#                 # Create email message
#                 email = EmailMultiAlternatives(
#                     subject=subject,
#                     body=text_content,
#                     from_email=smtp.email_address,
#                     to=[email_to],
#                     reply_to=[smtp.email_address],
#                     headers={"List-Unsubscribe": "<mailto:unsubscribe@yourdomain.com>"}
#                 )
#                 email.attach_alternative(html_content, "text/html")

#                 # SMTP sending logic with TLS/SSL handling
#                 if smtp.use_tls and smtp.smtp_port == 587:
#                     with smtplib.SMTP(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
#                         server.starttls()
#                         server.login(smtp.email_address, smtp.email_password)
#                         server.sendmail(smtp.email_address, email_to, email.message().as_bytes())
#                 elif smtp.smtp_port == 465:
#                     with smtplib.SMTP_SSL(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
#                         server.login(smtp.email_address, smtp.email_password)
#                         server.sendmail(smtp.email_address, email_to, email.message().as_bytes())
#                 else:
#                     with smtplib.SMTP(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
#                         server.login(smtp.email_address, smtp.email_password)
#                         server.sendmail(smtp.email_address, email_to, email.message().as_bytes())

#                 return None  # success

#             except Exception as e:
#                 return f"{email_to or 'Unknown'} - {str(e)}"

#         # Use threads to send emails
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             futures = [executor.submit(send_email, row) for row in reader]

#             for future in as_completed(futures):
#                 result = future.result()
#                 with lock:
#                     if result is None:
#                         sent_count += 1
#                     else:
#                         failed_emails.append(result)

#         return render(request, 'emails/email_success.html', {
#             'count': sent_count,
#             'failed': failed_emails
#         })

class SendBulkEmailView(View):
    template_name = 'emails/send_bulk_email.html'

    def get(self, request, smtp_id=None):
        settings = setting_obj(request)
        if smtp_id:
            try:
                smtp_instance = SMTPSetting.objects.get(pk=smtp_id)
                form = BulkEmailForm(initial={'smtp_setting': smtp_instance})
            except SMTPSetting.DoesNotExist:
                form = BulkEmailForm()
        else:
            form = BulkEmailForm()

        return render(request, self.template_name, {
            'form': form,
            'smtp_instance':smtp_instance,
            'smtp_settings': settings  # for sidebar if needed
        })

    def post(self, request, smtp_id=None):
        form = BulkEmailForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        smtp = form.cleaned_data['smtp_setting']
        subject_template = form.cleaned_data['subject']
        message_template = form.cleaned_data['message']
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
        except UnicodeDecodeError:
            return render(request, self.template_name, {
                'form': form,
                'error': 'Uploaded file is not UTF-8 encoded. Please upload a valid CSV file.'
            })

        reader = list(csv.DictReader(decoded_file))

        sent_count = 0
        failed_emails = []
        lock = threading.Lock()

        
        def send_email(row):
            email_to = row.get('email', '').strip()
            if not email_to:
                return "Missing email"

            try:
                context = Context(row)
                subject = Template(subject_template).render(context).strip()
                message_body = Template(message_template).render(context)

                html_content = render_to_string("emails/email_template.html", {
                    **row,
                    'message': message_body,
                })
                text_content = strip_tags(html_content)

                # Native Gmail Unsubscribe Support (DO NOT render in body)
                unsubscribe_url = f"https://financialsolution24x7.com/unsubscribe?email={email_to}"

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=smtp.email_address,
                    to=[email_to],
                    reply_to=[smtp.email_address],
                    headers={
                        "List-Unsubscribe": f"<mailto:collectiondepartment@financialsolution24x7.com>, <{unsubscribe_url}>",
                        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
                    }
                )
                email.attach_alternative(html_content, "text/html")

                if smtp.use_tls and smtp.smtp_port == 587:
                    with smtplib.SMTP(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
                        server.starttls()
                        server.login(smtp.email_address, smtp.email_password)
                        server.sendmail(smtp.email_address, email_to, email.message().as_bytes())
                elif smtp.smtp_port == 465:
                    with smtplib.SMTP_SSL(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
                        server.login(smtp.email_address, smtp.email_password)
                        server.sendmail(smtp.email_address, email_to, email.message().as_bytes())
                else:
                    with smtplib.SMTP(smtp.smtp_host, smtp.smtp_port, timeout=30) as server:
                        server.login(smtp.email_address, smtp.email_password)
                        server.sendmail(smtp.email_address, email_to, email.message().as_bytes())

                return None

            except Exception as e:
                return f"{email_to or 'Unknown'} - {str(e)}"

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_email, row) for row in reader]

            for future in as_completed(futures):
                result = future.result()
                with lock:
                    if result is None:
                        sent_count += 1
                    else:
                        failed_emails.append(result)

        return render(request, 'emails/email_success.html', {
            'count': sent_count,
            'failed': failed_emails,
            'smtp_id':smtp_id
        })


def upload_csv(request):
    settings = setting_obj(request)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('csv_list')  # Or wherever you want to redirect
    else:
        form = CSVUploadForm()
    return render(request, 'csv/upload_csv.html', {'form': form, 'smtp_settings': settings})
