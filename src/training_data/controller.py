from service import LogicService

class APIController:
    def handle_request(self, request):
        service = LogicService()
        return service.process(request)