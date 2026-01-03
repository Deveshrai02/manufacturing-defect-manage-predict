class Defect:
    def __init__(self, defect_id, defect_type, defect_location, severity, repair_cost, defect_date=None):
        self.defect_id = defect_id
        self.defect_type = defect_type
        self.defect_location = defect_location
        self.severity = severity
        self.repair_cost = repair_cost
        # store the raw date string from the CSV (may be None)
        self.defect_date = defect_date

    def is_critical(self):
        return self.severity.lower() == 'critical' or self.repair_cost > 700.0
    
