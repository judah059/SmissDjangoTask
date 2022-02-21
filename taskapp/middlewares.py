import datetime

from django.utils.deprecation import MiddlewareMixin
from .models import EmployeesRequest


class CollectRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/employees/':
            request.session['start'] = datetime.datetime.now().isoformat()
            erc = EmployeesRequest.objects.get(name='employee_req_counter')
            erc.count += 1
            erc.save()
            print(request.session['start'])

    def process_response(self, request, response):
        if request.path == '/api/employees/':
            start_time = request.session.get('start')
            res = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
            delta = (datetime.datetime.now() - res).microseconds
            erc = EmployeesRequest.objects.get(name='employee_req_counter')
            erc.sum_time += delta
            erc.average_time = erc.sum_time / erc.count
            erc.save()
        return response


