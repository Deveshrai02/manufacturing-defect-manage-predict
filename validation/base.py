from abc import ABC, abstractmethod 


class Validator(ABC):

    @abstractmethod
    def validate(self, defect):
        pass

class GoodValidator(Validator):
    def validate(self, defect):
        return True
