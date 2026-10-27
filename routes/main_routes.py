import os
from flask import Blueprint, render_template, send_from_directory, abort
from config import CM_DIR, RESULTS_DIR, EDA_DIR, FE_DIR
from services.benchmark_service import benchmark_service
from services.model_service import model_service
from services.feature_catalog import FEATURE_CATEGORIES, FEATURE_DEFINITIONS

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    kpis = benchmark_service.get_summary_kpis()
    return render_template("index.html", kpis=kpis, active_page="dashboard")

@main_bp.route("/demo")
def demo():
    return render_template("demo.html", active_page="demo")

@main_bp.route("/benchmarks")
def benchmarks():
    results = benchmark_service.get_all_results()
    kpis = benchmark_service.get_summary_kpis()
    return render_template("benchmarks.html", results=results, kpis=kpis, active_page="benchmarks")

@main_bp.route("/features")
def features():
    binary_rankings = model_service.get_mrmr_rankings("binary")
    multi_rankings = model_service.get_mrmr_rankings("multiclass")
    pca_artifact = model_service.get_pca_artifact()

    pca_components = []
    if pca_artifact and "full_pca" in pca_artifact:
        full_pca = pca_artifact["full_pca"]
        exp_var = full_pca.explained_variance_ratio_
        cum_var = pca_artifact.get("cumulative_variance", [])
        for i in range(len(exp_var)):
            c_val = cum_var[i] if i < len(cum_var) else sum(exp_var[:i+1])
            pca_components.append({
                "component": i + 1,
                "explained_variance": round(float(exp_var[i] * 100.0), 3),
                "cumulative_variance": round(float(c_val * 100.0), 3)
            })

    return render_template(
        "features.html",
        active_page="features",
        binary_rankings=binary_rankings,
        multi_rankings=multi_rankings,
        pca_components=pca_components,
        categories=FEATURE_CATEGORIES,
        definitions=FEATURE_DEFINITIONS
    )

@main_bp.route("/methodology")
def methodology():
    return render_template("methodology.html", active_page="methodology")

# Static asset routes for pre-rendered output images
@main_bp.route("/assets/cm/<path:filename>")
def serve_cm(filename):
    return send_from_directory(CM_DIR, filename)

@main_bp.route("/assets/results/<path:filename>")
def serve_result_img(filename):
    return send_from_directory(RESULTS_DIR, filename)

@main_bp.route("/assets/eda/<path:filename>")
def serve_eda_img(filename):
    return send_from_directory(EDA_DIR, filename)

@main_bp.route("/assets/fe/<path:filename>")
def serve_fe_img(filename):
    return send_from_directory(FE_DIR, filename)
