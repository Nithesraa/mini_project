import time
import numpy as np
from services.model_service import model_service
from services.explain_service import explain_service

class InferenceService:
    def run_inference(self, vector_79, task, method, n_features, model_name, raw_dict=None, norm_dict=None):
        """
        Execute live model inference and generate accompanying interpretability telemetry.
        vector_79: numpy array of shape (1, 79) containing normalized [0, 1] values.
        """
        if raw_dict is None:
            raw_dict = {}
        if norm_dict is None:
            norm_dict = {}

        # 1. Format experiment ID and load model
        exp_id = f"{task}_{method}_{n_features}_{model_name.replace(' ', '_')}"
        model = model_service.get_model(exp_id)

        feature_cols = model_service.get_feature_cols()
        classes = model_service.get_binary_classes() if task == "binary" else model_service.get_multiclass_classes()

        # 2. Slice or project feature vector to exact model representation
        if method == "baseline":
            X_sub = vector_79.copy()
        elif method == "mrmr":
            rankings = model_service.get_mrmr_rankings(task)
            selected_features = rankings[:n_features]
            col_indices = [feature_cols.index(f) for f in selected_features]
            X_sub = vector_79[:, col_indices]
        elif method == "pca":
            pca_artifact = model_service.get_pca_artifact()
            if not pca_artifact or "full_pca" not in pca_artifact:
                raise RuntimeError("PCA checkpoint artifact not available.")
            full_pca = pca_artifact["full_pca"]
            X_sub = full_pca.transform(vector_79)[:, :n_features]
        else:
            raise ValueError(f"Unknown reduction method: {method}")

        # 3. Execute prediction and measure latency
        t0 = time.perf_counter()
        pred_raw = model.predict(X_sub)[0]
        latency_ms = (time.perf_counter() - t0) * 1000.0

        pred_idx = int(pred_raw)
        pred_label = classes[pred_idx] if pred_idx < len(classes) else str(pred_idx)

        # 4. Extract class probabilities if supported
        class_probabilities = {}
        confidence_score = 0.0
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_sub)[0]
            confidence_score = float(probs[pred_idx]) if pred_idx < len(probs) else 0.0
            for idx, c_name in enumerate(classes):
                class_probabilities[c_name] = round(float(probs[idx]), 4) if idx < len(probs) else 0.0
        else:
            class_probabilities[pred_label] = 1.0
            confidence_score = 1.0

        # 5. Generate configuration-specific explanations
        explanation_data = explain_service.explain_prediction(
            model=model,
            X_sub=X_sub,
            vector_79=vector_79,
            task=task,
            method=method,
            n_features=n_features,
            model_name=model_name,
            raw_dict=raw_dict,
            norm_dict=norm_dict
        )

        compression_pct = round((1.0 - (n_features / 79.0)) * 100.0, 2)

        return {
            "status": "success",
            "telemetry": {
                "latency_ms": round(latency_ms, 3),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            },
            "configuration": {
                "task": task,
                "method": method,
                "n_features": n_features,
                "model_name": model_name,
                "experiment_id": exp_id
            },
            "prediction": {
                "predicted_class_index": pred_idx,
                "predicted_label": pred_label,
                "confidence_score": round(confidence_score, 4),
                "class_probabilities": class_probabilities
            },
            "reduction_summary": {
                "method": method,
                "original_features": 79,
                "active_features": n_features,
                "compression_pct": compression_pct
            },
            "decision_tree_explanation": explanation_data["decision_tree"],
            "neural_network_explanation": explanation_data["neural_network"],
            "pca_telemetry": explanation_data["pca_telemetry"],
            "feature_table": explanation_data["feature_table"]
        }

inference_service = InferenceService()
