import numpy as np
from services.feature_catalog import get_feature_info
from services.model_service import model_service

class ExplainService:
    def explain_prediction(self, model, X_sub, vector_79, task, method, n_features, model_name, raw_dict, norm_dict):
        """
        Generate a comprehensive, configuration-specific explanation payload.
        Adheres to scikit-learn 1.6.1 runtime introspection without hardcoded values.
        """
        classes = model_service.get_binary_classes() if task == "binary" else model_service.get_multiclass_classes()
        feature_cols = model_service.get_feature_cols()

        # 1. Determine active feature identifiers passed to estimator
        if method == "baseline":
            active_labels = feature_cols
            is_pca = False
        elif method == "mrmr":
            rankings = model_service.get_mrmr_rankings(task)
            active_labels = rankings[:n_features]
            is_pca = False
        elif method == "pca":
            active_labels = [f"PC{i+1}" for i in range(n_features)]
            is_pca = True
        else:
            raise ValueError(f"Unknown reduction method: {method}")

        # 2. Decision Tree Explanation (Dynamic Runtime Introspection)
        dt_explanation = {
            "is_applicable": False,
            "disclaimer": None
        }

        if hasattr(model, "tree_"):
            tree = model.tree_
            reached_leaf = int(model.apply(X_sub)[0])
            dec_path_nodes = model.decision_path(X_sub).indices

            path_steps = []
            for step_idx, node in enumerate(dec_path_nodes):
                feat_idx = tree.feature[node]
                if feat_idx != -2:  # Decision Split Node
                    feat_label = active_labels[feat_idx]
                    thresh = float(tree.threshold[node])
                    sample_val = float(X_sub[0, feat_idx])
                    is_left = sample_val <= thresh
                    branch = "Left" if is_left else "Right"
                    cond_bool = "True" if is_left else "False"

                    # Raw measurement value if original feature
                    raw_val_str = raw_dict.get(feat_label, "N/A") if not is_pca else f"Proj Coord: {sample_val:.4f}"

                    path_steps.append({
                        "step_number": step_idx + 1,
                        "node_id": int(node),
                        "feature": feat_label,
                        "feature_position": int(feat_idx),
                        "threshold": round(thresh, 6),
                        "sample_value": round(sample_val, 6),
                        "raw_value": raw_val_str,
                        "condition": f"{feat_label} <= {thresh:.6f}",
                        "condition_evaluated": cond_bool,
                        "branch_taken": branch,
                        "n_node_samples": int(tree.n_node_samples[node])
                    })

            # Leaf Node Properties
            leaf_samples = int(tree.n_node_samples[reached_leaf])
            weighted_samples = float(tree.weighted_n_node_samples[reached_leaf])
            val_dist = tree.value[reached_leaf][0]
            val_sum = float(np.sum(val_dist))
            prob_dist = val_dist / val_sum
            leaf_pred_class = int(np.argmax(prob_dist))
            purity_pct = float(np.max(prob_dist) * 100.0)

            # Reconstructed class counts
            class_counts = {}
            for c_idx, c_name in enumerate(classes):
                p = float(prob_dist[c_idx]) if c_idx < len(prob_dist) else 0.0
                class_counts[c_name] = int(round(weighted_samples * p))

            dt_explanation = {
                "is_applicable": True,
                "traversed_node_count": len(dec_path_nodes),
                "leaf_node_id": reached_leaf,
                "leaf_samples": leaf_samples,
                "leaf_purity_pct": round(purity_pct, 2),
                "predicted_class_name": classes[leaf_pred_class] if leaf_pred_class < len(classes) else str(leaf_pred_class),
                "class_counts": class_counts,
                "path_steps": path_steps,
                "is_pca_tree": is_pca
            }

        # 3. Neural Network Explanation (Global Context & Explicit Disclaimer)
        mlp_explanation = {
            "is_applicable": False,
            "disclaimer": None
        }
        if "Neural Network" in model_name or "Neural_Network" in model_name or "MLP" in model_name:
            mlp_explanation = {
                "is_applicable": True,
                "disclaimer": (
                    "The 25-neuron Multi-Layer Perceptron (MLP) evaluates the continuous non-linear "
                    "interaction across all input dimensions simultaneously. Local sample split conditions "
                    "are not mathematically defined for this estimator. Displayed feature rankings represent "
                    "global relevance from the feature reduction track, not individual prediction attribution."
                )
            }

        # 4. PCA Telemetry & Component Loadings
        pca_telemetry = {
            "is_applicable": is_pca,
            "components": []
        }
        if is_pca:
            pca_artifact = model_service.get_pca_artifact()
            if pca_artifact and "full_pca" in pca_artifact:
                full_pca = pca_artifact["full_pca"]
                exp_var = full_pca.explained_variance_ratio_
                cum_var = pca_artifact.get("cumulative_variance", np.cumsum(exp_var))
                comps = full_pca.components_

                for comp_idx in range(n_features):
                    coord_val = float(X_sub[0, comp_idx])
                    var_pct = float(exp_var[comp_idx] * 100.0)
                    cum_pct = float(cum_var[comp_idx] * 100.0)

                    # Extract top 3 constituent features with highest absolute loadings
                    row = comps[comp_idx, :]
                    top_indices = np.argsort(np.abs(row))[::-1][:3]
                    top_loadings = [
                        {
                            "feature": feature_cols[idx],
                            "loading": round(float(row[idx]), 4),
                            "direction": "Positive" if row[idx] >= 0 else "Negative"
                        }
                        for idx in top_indices
                    ]

                    pca_telemetry["components"].append({
                        "name": f"PC{comp_idx+1}",
                        "coordinate_value": round(coord_val, 6),
                        "explained_variance_pct": round(var_pct, 2),
                        "cumulative_variance_pct": round(cum_pct, 2),
                        "top_loadings": top_loadings
                    })

        # 5. Build Comprehensive Feature Table
        feature_table = []
        gini_importances = getattr(model, "feature_importances_", None)

        if not is_pca:
            for pos_idx, f_name in enumerate(active_labels):
                info = get_feature_info(f_name)
                norm_val = float(X_sub[0, pos_idx])
                raw_val = raw_dict.get(f_name, "N/A")

                # Importance Metric
                imp_label = "Full Feature Vector"
                imp_val = "Baseline"
                if method == "mrmr":
                    imp_label = f"MRMR {task.capitalize()} Rank"
                    imp_val = f"#{pos_idx + 1}"

                gini_val = None
                if gini_importances is not None and pos_idx < len(gini_importances):
                    gini_val = round(float(gini_importances[pos_idx]), 4)

                feature_table.append({
                    "position": pos_idx + 1,
                    "feature": f_name,
                    "is_principal_component": False,
                    "raw_value": str(raw_val),
                    "normalized_value": round(norm_val, 6),
                    "units": info.get("units", "Numerical"),
                    "meaning": info.get("meaning", "Network flow metric."),
                    "relevance": info.get("relevance", "Contributes to flow profiling."),
                    "importance_label": imp_label,
                    "importance_value": imp_val,
                    "gini_importance": gini_val
                })
        else:
            # For PCA models, table shows Principal Components
            for pos_idx in range(n_features):
                comp_data = pca_telemetry["components"][pos_idx] if pos_idx < len(pca_telemetry["components"]) else {}
                gini_val = None
                if gini_importances is not None and pos_idx < len(gini_importances):
                    gini_val = round(float(gini_importances[pos_idx]), 4)

                feature_table.append({
                    "position": pos_idx + 1,
                    "feature": f"PC{pos_idx+1}",
                    "is_principal_component": True,
                    "raw_value": "Orthogonal Projection",
                    "normalized_value": comp_data.get("coordinate_value", round(float(X_sub[0, pos_idx]), 6)),
                    "units": f"{comp_data.get('explained_variance_pct', 0.0)}% Variance",
                    "meaning": f"Principal Component {pos_idx+1} capturing {comp_data.get('explained_variance_pct', 0.0)}% of dataset variance.",
                    "relevance": f"Heavily loaded by: {', '.join([l['feature'] + ' (' + str(l['loading']) + ')' for l in comp_data.get('top_loadings', [])])}",
                    "importance_label": "Explained Variance",
                    "importance_value": f"{comp_data.get('explained_variance_pct', 0.0)}%",
                    "gini_importance": gini_val
                })

        return {
            "decision_tree": dt_explanation,
            "neural_network": mlp_explanation,
            "pca_telemetry": pca_telemetry,
            "feature_table": feature_table
        }

explain_service = ExplainService()
