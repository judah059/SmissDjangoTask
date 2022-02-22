from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from employees.models import EmployeesRequest
from django.conf import settings


@shared_task
def send_requests_count():
    admins = get_user_model().objects.filter(is_superuser=True)
    for admin in admins:
        print(admin.email, 'im here')
        print(f'Count: {EmployeesRequest.objects.last().count}, Average time of request in microseconds: '
                f'{EmployeesRequest.objects.last().average_time}')
        send_mail(
            'Report',
            f'Count: {EmployeesRequest.objects.last().count}, Average time of request: '
            f'{EmployeesRequest.objects.last().average_time}',
            settings.EMAIL_HOST_USER,
            [admin.email, ],
            fail_silently=False
        )
