from validation.base import Validator
from datetime import datetime


class PositionValidator(Validator):
    # Normalize to lowercase when comparing
    ALLOWED_POSITIONS = {"component", "internal", "surface"}

    def validate(self, defect):
        loc = getattr(defect, "defect_location", None)
        if loc is None:
            return False
        return str(loc).strip().lower() in self.ALLOWED_POSITIONS


class CostValidator(Validator):
    def validate(self, defect):
        cost = getattr(defect, "repair_cost", None)
        try:
            return float(cost) >= 0
        except Exception:
            return False


class SeverityValidator(Validator):
    ALLOWED_SEVERITIES = {"critical", "moderate", "minor"}

    def validate(self, defect):
        sev = getattr(defect, "severity", None)
        if sev is None:
            return False
        return str(sev).strip().lower() in self.ALLOWED_SEVERITIES


class DateValidator(Validator):
    """Validate that `defect.defect_date` is present and parseable.

    Accepts a few common date formats (month/day/year and ISO). If the date
    is missing or unparseable, validation fails and the defect will be
    reported as rejected.
    """
    FORMATS = ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%d/%m/%Y"]

    def validate(self, defect):
        date_str = getattr(defect, "defect_date", None)
        if not date_str:
            return False
        s = str(date_str).strip()
        for fmt in self.FORMATS:
            try:
                datetime.strptime(s, fmt)
                return True
            except Exception:
                continue
        return False
