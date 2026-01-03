from validation.base import Validator
from datetime import datetime

try:
    from utils.config import get_validations
    _VALIDATIONS = get_validations()
except Exception:
    _VALIDATIONS = {}


class PositionValidator(Validator):
    def __init__(self):
        allowed = _VALIDATIONS.get("defect_location", {}).get("allowed_values")
        if allowed:
            self.allowed = {str(x).strip().lower() for x in allowed}
        else:
            # fallback default
            self.allowed = {"component", "internal", "surface"}

    def validate(self, defect):
        loc = getattr(defect, "defect_location", None)
        if loc is None:
            return False
        return str(loc).strip().lower() in self.allowed


class CostValidator(Validator):
    def __init__(self):
        cfg = _VALIDATIONS.get("repair_cost", {})
        self.min = cfg.get("min")
        self.max = cfg.get("max")

    def validate(self, defect):
        cost = getattr(defect, "repair_cost", None)
        try:
            val = float(cost)
        except Exception:
            return False

        if self.min is not None and val < float(self.min):
            return False
        if self.max is not None and val > float(self.max):
            return False
        return True


class SeverityValidator(Validator):
    def __init__(self):
        allowed = _VALIDATIONS.get("severity", {}).get("allowed_values")
        if allowed:
            self.allowed = {str(x).strip().lower() for x in allowed}
        else:
            self.allowed = {"critical", "moderate", "minor"}

    def validate(self, defect):
        sev = getattr(defect, "severity", None)
        if sev is None:
            return False
        return str(sev).strip().lower() in self.allowed


class DateValidator(Validator):
    """Validate that `defect.defect_date` is present and parseable.

    Date formats are read from configuration under `defect_date.date_formats`.
    """
    def __init__(self):
        self.formats = _VALIDATIONS.get("defect_date", {}).get("date_formats") or [
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%m-%d-%Y",
            "%d/%m/%Y",
        ]

    def validate(self, defect):
        date_str = getattr(defect, "defect_date", None)
        if not date_str:
            return False
        s = str(date_str).strip()
        for fmt in self.formats:
            try:
                datetime.strptime(s, fmt)
                return True
            except Exception:
                continue
        return False
