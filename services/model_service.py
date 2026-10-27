import os
import joblib
import pandas as pd
from collections import OrderedDict
from config import (
    MODELS_DIR, PREPROCESSED_META_PATH, PCA_RESULT_PATH,
    MRMR_BINARY_RANKINGS_PATH, MRMR_MULTI_RANKINGS_PATH
)

class ModelService:
    def __init__(self, max_cached_models=5):
        self.max_cached = max_cached_models
        self.cache = OrderedDict()
        self.meta = None
        self.pca_artifact = None
        self.mrmr_binary_rankings = None
        self.mrmr_multi_rankings = None
        self._load_metadata()

    def _load_metadata(self):
        """Load static feature lists and ranking metadata once at initialization."""
        if os.path.exists(PREPROCESSED_META_PATH):
            self.meta = joblib.load(PREPROCESSED_META_PATH)
        else:
            self.meta = {}

        if os.path.exists(MRMR_BINARY_RANKINGS_PATH):
            df_b = pd.read_csv(MRMR_BINARY_RANKINGS_PATH)
            self.mrmr_binary_rankings = df_b["feature"].tolist()
        else:
            self.mrmr_binary_rankings = []

        if os.path.exists(MRMR_MULTI_RANKINGS_PATH):
            df_m = pd.read_csv(MRMR_MULTI_RANKINGS_PATH)
            self.mrmr_multi_rankings = df_m["feature"].tolist()
        else:
            self.mrmr_multi_rankings = []

    def get_feature_cols(self):
        """Return the authoritative list of 79 feature names in original order."""
        return self.meta.get("feature_cols", [])

    def get_binary_classes(self):
        """Return binary class names ['Anomaly', 'Normal']."""
        if "le_binary" in self.meta:
            return list(self.meta["le_binary"].classes_)
        return ["Anomaly", "Normal"]

    def get_multiclass_classes(self):
        """Return 5-class multiclass names ['DoS', 'MITM ARP Spoofing', 'Mirai', 'Normal', 'Scan']."""
        if "le_multi" in self.meta:
            return list(self.meta["le_multi"].classes_)
        return ["DoS", "MITM ARP Spoofing", "Mirai", "Normal", "Scan"]

    def get_mrmr_rankings(self, task):
        """Return ranked feature list for the given task."""
        if task == "binary":
            return self.mrmr_binary_rankings
        return self.mrmr_multi_rankings

    def get_pca_artifact(self):
        """Load and return PCA checkpoint."""
        if self.pca_artifact is None and os.path.exists(PCA_RESULT_PATH):
            self.pca_artifact = joblib.load(PCA_RESULT_PATH)
        return self.pca_artifact

    def get_model(self, experiment_id):
        """
        Load a trained model by experiment_id with LRU caching.
        Example exp_id: 'binary_mrmr_12_Decision_Tree'
        """
        if experiment_id in self.cache:
            self.cache.move_to_end(experiment_id)
            return self.cache[experiment_id]

        model_filename = f"model_{experiment_id}.joblib"
        model_path = os.path.join(MODELS_DIR, model_filename)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model checkpoint not found: {model_path}")

        model = joblib.load(model_path)

        if len(self.cache) >= self.max_cached:
            self.cache.popitem(last=False)

        self.cache[experiment_id] = model
        return model

# Global singleton instance
model_service = ModelService()
