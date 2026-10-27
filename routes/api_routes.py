import os
import json
import numpy as np
from flask import Blueprint, request, jsonify
from config import PRESETS_FILE_PATH
from services.inference_service import inference_service
from services.benchmark_service import benchmark_service

api_bp = Blueprint("api", __name__, url_prefix="/api")

def _load_presets():
    if os.path.exists(PRESETS_FILE_PATH):
        with open(PRESETS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@api_bp.route("/presets", methods=["GET"])
def get_presets():
    presets = _load_presets()
    # Return metadata without heavy raw dumps for swift navbar/dropdown consumption
    summary = []
    for p in presets:
        summary.append({
            "id": p["id"],
            "name": p["name"],
            "expected_binary": p["expected_binary"],
            "expected_multiclass": p["expected_multiclass"],
            "badge_color": p["badge_color"],
            "description": p["description"],
            "raw_features": p["raw_features"],
            "normalized_features": p["normalized_features"]
        })
    return jsonify({"status": "success", "presets": summary})

@api_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}

    preset_id = data.get("preset_id", "mirai_udp")
    task = data.get("task", "binary").lower()
    method = data.get("method", "mrmr").lower()
    n_features = int(data.get("n_features", 12 if method != "baseline" else 79))
    model_name = data.get("model_name", "Decision Tree")

    # Validate inputs
    if task not in ["binary", "multiclass"]:
        return jsonify({"status": "error", "message": f"Invalid task: {task}"}), 400
    if method not in ["baseline", "mrmr", "pca"]:
        return jsonify({"status": "error", "message": f"Invalid method: {method}"}), 400
    if method == "baseline" and n_features != 79:
        n_features = 79
    if method in ["mrmr", "pca"] and n_features not in [4, 12, 23, 50]:
        n_features = 12

    # Load authentic preset vector
    presets = _load_presets()
    selected_preset = next((p for p in presets if p["id"] == preset_id), None)
    if not selected_preset:
        selected_preset = presets[0] if presets else None

    if not selected_preset:
        return jsonify({"status": "error", "message": "Preset data not available."}), 500

    vector_79 = np.array(selected_preset["normalized_vector"], dtype=float).reshape(1, -1)
    raw_dict = selected_preset.get("raw_features", {})
    norm_dict = selected_preset.get("normalized_features", {})

    try:
        response = inference_service.run_inference(
            vector_79=vector_79,
            task=task,
            method=method,
            n_features=n_features,
            model_name=model_name,
            raw_dict=raw_dict,
            norm_dict=norm_dict
        )

        # Ground truth tracking for evaluation transparency
        gt_label = selected_preset["expected_binary"] if task == "binary" else selected_preset["expected_multiclass"]
        pred_label = response["prediction"]["predicted_label"]
        is_correct = (gt_label.lower() == pred_label.lower())

        response["ground_truth"] = {
            "preset_id": selected_preset["id"],
            "preset_name": selected_preset["name"],
            "sub_category": selected_preset["sub_category"],
            "ground_truth_label": gt_label,
            "is_correct": is_correct
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/metrics", methods=["GET"])
def get_metrics():
    task = request.args.get("task")
    method = request.args.get("method")
    model_name = request.args.get("model_name")
    n_features = request.args.get("n_features")

    filtered = benchmark_service.filter_results(
        task=task,
        method=method,
        model_name=model_name,
        n_features=n_features
    )
    return jsonify({"status": "success", "count": len(filtered), "results": filtered})
