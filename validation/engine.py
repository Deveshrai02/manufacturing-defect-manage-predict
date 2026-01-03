class ValidationEngine:
    def __init__(self, validators):
        self.validators = validators

    def validate(self, defect):
        failures = []

        for validator in self.validators:
            if not validator.validate(defect):
                failures.append(validator.__class__.__name__)

        return failures
