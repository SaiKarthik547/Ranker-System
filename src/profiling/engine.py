import uuid
from src.contracts import DatasetRecord, SchemaGraph, ProfileReport, ProfileMetric, ArtifactMetadata, Confidence, Evidence
from src.contracts.enums import ArtifactType, MetricType, ConfidenceLevel

class ProfilingEngine:
    def process(self, records: list[DatasetRecord], schema: SchemaGraph, run_id: uuid.UUID) -> ProfileReport:
        metrics = []
        total = len(records)
        
        for field in schema.fields:
            null_count = 0
            for r in records:
                if not r.raw_payload.get(field.field_name):
                    null_count += 1
                    
            null_rate = null_count / total if total > 0 else 0.0
            
            metric = ProfileMetric(
                field_path=field.field_name,
                metric_type=MetricType.NULLABILITY,
                metric_value=float(null_rate),
                calculation_method="count"
            )
            metrics.append(metric)

        meta = ArtifactMetadata(
            artifact_type=ArtifactType.PROFILE_REPORT,
            producer_module="profiling_engine",
            pipeline_run_id=run_id,
        )
        conf = Confidence(
            confidence_score=1.0, 
            confidence_level=ConfidenceLevel.HIGH, 
            confidence_method="aggregate", 
            confidence_explanation="aggregated from metrics"
        )
        return ProfileReport(
            metadata=meta,
            confidence=conf,
            field_metrics=tuple(metrics),
            summary=f"Profiled {total} records."
        )
