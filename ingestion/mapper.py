from domain.defect import Defect
from utils.exceptions import MappingError

class DefectMapper:
    def map(self, row):
        try:
            # safely parse repair cost; do NOT raise on bad numeric strings
            raw_cost = row[7] if len(row) > 7 else None
            # date is at column index 3 in the CSV (defect_date)
            raw_date = row[3] if len(row) > 3 else None
            try:
                repair_cost = float(raw_cost) if raw_cost is not None and raw_cost != "" else None
            except Exception:
                repair_cost = None

            return Defect(
                defect_id=row[0],
                defect_type=row[2],
                defect_location=row[4],
                severity=row[5],
                repair_cost=repair_cost,
                defect_date=raw_date,
            )
        except IndexError as e:
            # Missing required columns — still a mapping error
            raise MappingError(row, str(e))
            