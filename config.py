import os

# Base directory paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHECKPOINTS_DIR = os.path.join(OUTPUT_DIR, "checkpoints")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")
CM_DIR = os.path.join(RESULTS_DIR, "confusion_matrices")
ROC_DIR = os.path.join(RESULTS_DIR, "roc_curves")
FE_DIR = os.path.join(OUTPUT_DIR, "feature_engineering")
EDA_DIR = os.path.join(OUTPUT_DIR, "eda")

# Core artifact file paths
PREPROCESSED_DATA_PATH = os.path.join(CHECKPOINTS_DIR, "preprocessed_data.npz")
PREPROCESSED_META_PATH = os.path.join(CHECKPOINTS_DIR, "preprocessed_meta.pkl")
PCA_RESULT_PATH = os.path.join(CHECKPOINTS_DIR, "pca_result.pkl")
MRMR_BINARY_RANKINGS_PATH = os.path.join(FE_DIR, "mrmr_binary_rankings.csv")
MRMR_MULTI_RANKINGS_PATH = os.path.join(FE_DIR, "mrmr_multiclass_rankings.csv")
RESULTS_CACHE_PATH = os.path.join(CHECKPOINTS_DIR, "results_cache.json")

# Data presets path
PRESETS_FILE_PATH = os.path.join(BASE_DIR, "data_presets", "attack_presets.json")

# Server configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "iiot-nids-secret-key-2024")
DEBUG = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
