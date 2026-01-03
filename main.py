from ingestion.reader import CSVReader
from ingestion.mapper import DefectMapper
from utils.exceptions import MappingError

from validation.validators import (
    PositionValidator,
    CostValidator,
    SeverityValidator,
    DateValidator,
)
from validation.engine import ValidationEngine

from analytics.aggregations import DefectAnalytics
from storage.writer import JSONWriter


def main():
    reader = CSVReader("data/defects_data.csv")
    mapper = DefectMapper()

    validators = [
        PositionValidator(),
        CostValidator(),
        SeverityValidator(),
        DateValidator()
    ]

    engine = ValidationEngine(validators)
    analytics = DefectAnalytics()
    writer = JSONWriter()

    valid_defects = []
    rejected_defects = []

    for row in reader:
        try:
            defect = mapper.map(row)
            failures = engine.validate(defect)

            if failures:
                rejected_defects.append({
                "defect_id": defect.defect_id,
                "reasons": failures
            })
            else:
                valid_defects.append(defect)
        except MappingError as me:
            rejected_defects.append({
                "row": me.row,
                "reasons": me.message
            })

    summary = {
        "defects_by_type": analytics.defects_by_type(valid_defects),
        "cost_by_position": analytics.cost_by_position(valid_defects),
        "total_valid_defects": len(valid_defects),
        "total_rejected_defects": len(rejected_defects)
    }

    writer.write(summary, "data/summary.json")
    writer.write(rejected_defects, "data/rejected.json")
    

if __name__ == "__main__":
    main()