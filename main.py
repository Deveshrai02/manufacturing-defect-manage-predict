from ingestion.reader import CSVReader
from ingestion.mapper import DefectMapper
from ml import dataset
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

from ml.features import FeatureBuilder
from ml.dataset import DatasetBuilder
from ml.model_factory import ModelFactory
from ml.trainer import Trainer
from ml.predictor import Predictor
from ml.metrics import Metrics

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

    # ML Pipeline

    feature_builder = FeatureBuilder()
    X, y = feature_builder.build(valid_defects)

    dataset = DatasetBuilder()
    X_train, X_test, y_train, y_test = dataset.split(X, y)

    model = ModelFactory.get("rf")

    trainer = Trainer()
    trained_model = trainer.train(model, X_train, y_train)

    predictor = Predictor()
    predictions = predictor.predict(trained_model, X_test)

    metrics = Metrics()
    accuracy = metrics.accuracy(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")




   
    

if __name__ == "__main__":
    main()