class DataModel:
    def __init__(self, data):
        self.data = data
    def get_payload(self):
        return {'status': 'success', 'content': self.data}