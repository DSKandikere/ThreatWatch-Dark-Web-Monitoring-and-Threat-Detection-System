from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def extract_features(self, item):
        parsed = item.get("parsed_data", {})

        return [
            len(parsed.get("emails", [])),
            len(parsed.get("passwords", [])),
            len(parsed.get("credit_cards", [])),
            len(item.get("content", "")),
        ]

    def fit(self, data):
        X = [self.extract_features(item) for item in data]
        self.model.fit(X)

    def predict(self, data):
        X = [self.extract_features(item) for item in data]
        scores = self.model.decision_function(X)
        labels = self.model.predict(X)

        results = []
        for i, item in enumerate(data):
            item["anomaly_score"] = float(scores[i])
            item["is_anomaly"] = True if labels[i] == -1 else False
            results.append(item)

        return results
