from model import DataModel

class LogicService:
    def process(self, raw_input):
        model = DataModel(raw_input)
        return model.get_payload()