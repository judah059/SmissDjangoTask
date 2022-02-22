import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import EmployeesRequest
from django.db.models import F


class CollectRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/taskapp/employees/':
            request.session['start'] = datetime.datetime.now().isoformat()
            obj, create = EmployeesRequest.objects.get_or_create(name='employee_req_counter')
            obj.count = F('count') + 1
            obj.save()

    def process_response(self, request, response):
        if request.path == '/api/taskapp/employees/':
            start_time = request.session.get('start')
            res = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
            delta = (datetime.datetime.now() - res).microseconds
            print(delta)
            obj = EmployeesRequest.objects.filter(name='employee_req_counter')
            obj.update(sum_time=F('sum_time')+delta)
            obj.update(average_time=F('sum_time')/F('count'))
        return response


