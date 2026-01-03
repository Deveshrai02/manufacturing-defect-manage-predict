class FeatureBuilder:
    def build(self, defects):
        """Build numeric feature matrix and labels from Defect objects.

        Encodes categorical fields (severity) to integers. Mapping is read
        from `config/rules.yaml` if available; otherwise a deterministic
        mapping based on observed categories is used.
        """
        # try to get ordered allowed values from config for stable mapping
        try:
            from utils.config import get_validations
            validations = get_validations()
            severity_allowed = validations.get("severity", {}).get("allowed_values")
            if severity_allowed:
                # preserve given order
                severity_map = {str(v).strip().lower(): i for i, v in enumerate(severity_allowed)}
            else:
                severity_map = None
        except Exception:
            severity_map = None

        # collect observed severities if we need to build mapping
        observed = []
        for d in defects:
            sev = getattr(d, "severity", None)
            if sev is not None:
                s = str(sev).strip().lower()
                if s not in observed:
                    observed.append(s)

        if severity_map is None:
            # deterministic mapping from observed (stable order)
            severity_map = {v: i for i, v in enumerate(observed)}

        features = []
        labels = []
        for defect in defects:
            # numeric feature: length of defect_type
            tlen = len(defect.defect_type) if getattr(defect, "defect_type", None) is not None else 0

            # severity -> numeric encoding (fallback 0)
            raw_sev = getattr(defect, "severity", None)
            sev_key = str(raw_sev).strip().lower() if raw_sev is not None else None
            sev_val = severity_map.get(sev_key, 0)

            # repair_cost should already be numeric or None
            cost = getattr(defect, "repair_cost", None)
            try:
                cost_val = float(cost) if cost is not None else 0.0
            except Exception:
                cost_val = 0.0

            features.append([tlen, sev_val, cost_val])
            labels.append(1 if defect.is_critical() else 0)

        return features, labels