import os
import json
from config import RESULTS_CACHE_PATH, CM_DIR

class BenchmarkService:
    def __init__(self):
        self.results = []
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(RESULTS_CACHE_PATH):
            with open(RESULTS_CACHE_PATH, "r", encoding="utf-8") as f:
                self.results = json.load(f)
        else:
            self.results = []

    def get_all_results(self):
        return self.results

    def filter_results(self, task=None, method=None, model_name=None, n_features=None):
        filtered = self.results
        if task:
            filtered = [r for r in filtered if r.get("task") == task]
        if method:
            filtered = [r for r in filtered if r.get("method") == method]
        if model_name:
            filtered = [r for r in filtered if r.get("model_name") == model_name]
        if n_features is not None:
            filtered = [r for r in filtered if r.get("n_features") == int(n_features)]
        return filtered

    def get_summary_kpis(self):
        if not self.results:
            return {}

        binary_results = [r for r in self.results if r.get("task") == "binary"]
        peak_acc = max((r.get("accuracy", 0.0) for r in binary_results), default=0.0)
        max_speed = max((r.get("pred_speed_obs_per_sec", 0.0) for r in self.results), default=0.0)
        min_far = min((r.get("far", 1.0) for r in binary_results), default=0.0)

        return {
            "total_models": len(self.results),
            "peak_binary_accuracy": round(peak_acc * 100.0, 2),
            "max_throughput_obs_sec": f"{int(max_speed):,}",
            "lowest_false_alarm_rate": round(min_far * 100.0, 4),
            "max_feature_reduction": "84.8%"
        }

    def get_confusion_matrix_filename(self, exp_id):
        """Map experiment ID to confusion matrix filename in output/results/confusion_matrices/"""
        # Formats: {exp_id}_cm.png or cm_{exp_id}.png
        cand1 = f"{exp_id}_cm.png"
        cand2 = f"cm_{exp_id}.png"
        if os.path.exists(os.path.join(CM_DIR, cand1)):
            return cand1
        if os.path.exists(os.path.join(CM_DIR, cand2)):
            return cand2
        return None

benchmark_service = BenchmarkService()
