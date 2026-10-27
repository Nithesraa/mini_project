// ==========================================================================
// IIoT Network Intrusion Detection Lab - Live Demo Client Logic
// Dynamic Execution & Real-Time Interpretability Engine (Light Theme)
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  let activePresetId = "mirai_udp";

  const presetBtns = document.querySelectorAll(".preset-btn");
  const taskSelect = document.getElementById("task-select");
  const methodSelect = document.getElementById("method-select");
  const nFeaturesGroup = document.getElementById("n-features-group");
  const nFeaturesSelect = document.getElementById("n-features-select");
  const modelSelect = document.getElementById("model-select");
  const executeBtn = document.getElementById("execute-btn");

  // Telemetry elements
  const threatBanner = document.getElementById("threat-banner");
  const threatLabel = document.getElementById("threat-label");
  const threatName = document.getElementById("threat-name");
  const presetContextDesc = document.getElementById("preset-context-desc");
  const confidenceVal = document.getElementById("confidence-val");
  const latencyVal = document.getElementById("latency-val");

  // Ground truth elements
  const gtLabel = document.getElementById("gt-label");
  const modelPredLabel = document.getElementById("model-pred-label");
  const matchTag = document.getElementById("match-tag");

  // Containers
  const probBarsContainer = document.getElementById("prob-bars-container");
  const dtExplanationCard = document.getElementById("dt-explanation-card");
  const mlpExplanationCard = document.getElementById("mlp-explanation-card");
  const pcaTelemetryCard = document.getElementById("pca-telemetry-card");
  const pathStepsContainer = document.getElementById("path-steps-container");
  const pathLengthBadge = document.getElementById("path-length-badge");
  const pcaComponentsBody = document.getElementById("pca-components-body");
  const featuresTableBody = document.getElementById("features-table-body");
  const featCountBadge = document.getElementById("feat-count-badge");
  const pcaTabBtn = document.getElementById("tab-btn-pca");

  // Tab Switching Functionality
  const tabButtons = document.querySelectorAll(".demo-tab-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".demo-tab-pane").forEach(pane => {
        pane.classList.remove("active");
        pane.style.display = "none";
      });

      const activePane = document.getElementById(targetId);
      if (activePane) {
        activePane.classList.add("active");
        activePane.style.display = "block";
      }
    });
  });

  // Preset Selection Handling
  presetBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      presetBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activePresetId = btn.getAttribute("data-preset");
      executeAnalysis();
    });
  });

  // Method Change Handling (Hide k for Baseline, adjust PCA tab)
  methodSelect.addEventListener("change", () => {
    const method = methodSelect.value;
    if (method === "baseline") {
      nFeaturesGroup.style.display = "none";
    } else {
      nFeaturesGroup.style.display = "block";
    }
    if (pcaTabBtn) {
      if (method === "pca") {
        pcaTabBtn.style.display = "inline-flex";
      } else {
        pcaTabBtn.style.display = "none";
        // If PCA tab was active, switch to decision path
        if (pcaTabBtn.classList.contains("active")) {
          const firstTab = document.querySelector(".demo-tab-btn[data-tab='pane-explanation']");
          if (firstTab) firstTab.click();
        }
      }
    }
  });

  // Execute Analysis Trigger
  executeBtn.addEventListener("click", executeAnalysis);

  async function executeAnalysis() {
    executeBtn.disabled = true;
    executeBtn.innerHTML = `<span>⏳</span><span>Analyzing Network Flow...</span>`;

    const payload = {
      preset_id: activePresetId,
      task: taskSelect.value,
      method: methodSelect.value,
      n_features: methodSelect.value === "baseline" ? 79 : parseInt(nFeaturesSelect.value),
      model_name: modelSelect.value
    };

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      if (data.status === "success") {
        renderResults(data);
      } else {
        alert("Error executing inference: " + (data.message || "Unknown error"));
      }
    } catch (err) {
      console.error("Inference request failed:", err);
      alert("Failed to connect to backend server.");
    } finally {
      executeBtn.disabled = false;
      executeBtn.innerHTML = `<span>⚡</span><span>Execute Intrusion Analysis</span>`;
    }
  }

  function renderResults(data) {
    const pred = data.prediction;
    const gt = data.ground_truth;
    const isAnomaly = pred.predicted_label.toLowerCase() !== "normal";

    // 1. Primary Threat Banner
    if (isAnomaly) {
      threatBanner.className = "threat-banner anomaly";
      threatLabel.textContent = "THREAT DETECTED";
      threatLabel.style.color = "var(--color-danger)";
      threatName.textContent = `ANOMALY (${pred.predicted_label.toUpperCase()})`;
      confidenceVal.style.color = "var(--color-danger)";
    } else {
      threatBanner.className = "threat-banner normal";
      threatLabel.textContent = "SECURE NETWORK FLOW";
      threatLabel.style.color = "var(--color-success)";
      threatName.textContent = "BENIGN (NORMAL)";
      confidenceVal.style.color = "var(--color-success)";
    }

    presetContextDesc.innerHTML = `<strong>${gt.preset_name}</strong> &bull; Ground Truth Sub-Category: <code>${gt.sub_category}</code>`;
    confidenceVal.textContent = `${(pred.confidence_score * 100).toFixed(2)}%`;
    latencyVal.textContent = `${data.telemetry.latency_ms.toFixed(2)} ms`;

    // 2. Ground Truth Integrity Bar
    gtLabel.textContent = gt.ground_truth_label;
    modelPredLabel.textContent = pred.predicted_label;
    if (gt.is_correct) {
      matchTag.className = "tag success";
      matchTag.textContent = "✓ Verified Match";
    } else {
      matchTag.className = "tag warning";
      matchTag.textContent = "⚠️ Misclassified";
    }

    // 3. Class Probability Breakdown
    probBarsContainer.innerHTML = "";
    const probs = pred.class_probabilities || {};
    for (const [cName, pVal] of Object.entries(probs)) {
      const pct = (pVal * 100).toFixed(2);
      const isTop = cName.toLowerCase() === pred.predicted_label.toLowerCase();
      const barColor = isTop ? (isAnomaly ? "var(--color-danger)" : "var(--color-success)") : "#cbd5e1";

      const barRow = document.createElement("div");
      barRow.style.display = "flex";
      barRow.style.flexDirection = "column";
      barRow.style.gap = "0.25rem";

      barRow.innerHTML = `
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem;">
          <span style="font-weight: ${isTop ? '700' : '500'}; color: ${isTop ? 'var(--text-primary)' : 'var(--text-secondary)'};">${cName}</span>
          <span style="font-family: var(--font-mono); font-weight: ${isTop ? '700' : '500'}; color: ${isTop ? 'var(--text-primary)' : 'var(--text-muted)'};">${pct}%</span>
        </div>
        <div style="background-color: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-full); height: 8px; overflow: hidden;">
          <div style="background-color: ${barColor}; width: ${pct}%; height: 100%; border-radius: var(--radius-full); transition: width 0.4s ease;"></div>
        </div>
      `;
      probBarsContainer.appendChild(barRow);
    }

    // 4. Decision Tree vs Neural Network Explanations
    if (data.decision_tree_explanation && data.decision_tree_explanation.is_applicable) {
      dtExplanationCard.style.display = "block";
      mlpExplanationCard.style.display = "none";
      renderDecisionTreePath(data.decision_tree_explanation);
    } else if (data.neural_network_explanation && data.neural_network_explanation.is_applicable) {
      dtExplanationCard.style.display = "none";
      mlpExplanationCard.style.display = "block";
    } else {
      dtExplanationCard.style.display = "none";
      mlpExplanationCard.style.display = "none";
    }

    // 5. PCA Telemetry Panel & Tab
    if (data.pca_telemetry && data.pca_telemetry.is_applicable) {
      if (pcaTabBtn) pcaTabBtn.style.display = "inline-flex";
      pcaTelemetryCard.style.display = "block";
      renderPcaTable(data.pca_telemetry.components);
    } else {
      if (pcaTabBtn) pcaTabBtn.style.display = "none";
      pcaTelemetryCard.style.display = "none";
    }

    // 6. Comprehensive Features Table
    featCountBadge.textContent = `${data.feature_table.length} Features`;
    renderFeaturesTable(data.feature_table);
  }

  function renderDecisionTreePath(dtData) {
    pathLengthBadge.textContent = `${dtData.traversed_node_count} Nodes Traversed`;
    pathStepsContainer.innerHTML = "";

    dtData.path_steps.forEach(step => {
      const stepEl = document.createElement("div");
      stepEl.className = "path-step";
      stepEl.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span class="path-step-badge">Step ${step.step_number}</span>
          <strong style="color: var(--text-primary);">${step.feature}</strong>
          <span style="color: var(--text-muted); font-size: 0.8rem;">(Raw: ${step.raw_value})</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span style="color: var(--text-secondary); font-size: 0.8rem;">Scaled: <code>${step.sample_value}</code></span>
          <span style="color: var(--accent-primary); font-weight: 600;">${step.condition}</span>
          <span class="tag ${step.condition_evaluated === 'True' ? 'success' : 'warning'}">
            ${step.condition_evaluated} &rarr; ${step.branch_taken} Branch
          </span>
        </div>
      `;
      pathStepsContainer.appendChild(stepEl);
    });

    // Terminal Leaf Card
    const leafEl = document.createElement("div");
    leafEl.className = "path-leaf-card";
    const countsStr = Object.entries(dtData.class_counts)
      .map(([k, v]) => `${k}: ${v.toLocaleString()}`)
      .join(" &bull; ");

    leafEl.innerHTML = `
      <div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
          <span class="tag success" style="font-weight: 800;">Terminal Leaf #${dtData.leaf_node_id}</span>
          <strong style="color: var(--text-heading); font-size: 1.05rem;">Predicted Class: ${dtData.predicted_class_name}</strong>
        </div>
        <div style="color: var(--text-secondary); font-size: 0.82rem;">
          Training Samples in Leaf: <strong>${dtData.leaf_samples.toLocaleString()}</strong> (${countsStr})
        </div>
      </div>
      <div style="text-align: right;">
        <span style="font-size: 0.72rem; color: var(--text-muted); display: block; text-transform: uppercase; font-weight: 600;">Leaf Node Purity</span>
        <span style="font-size: 1.35rem; font-weight: 800; color: var(--color-success-text); font-family: var(--font-mono);">${dtData.leaf_purity_pct}%</span>
      </div>
    `;
    pathStepsContainer.appendChild(leafEl);
  }

  function renderPcaTable(components) {
    pcaComponentsBody.innerHTML = "";
    components.forEach(comp => {
      const loadingsStr = comp.top_loadings
        .map(l => `<span style="display: inline-block; background: var(--bg-secondary); border: 1px solid var(--border-color); padding: 0.15rem 0.4rem; border-radius: 4px; margin: 0.1rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-primary);">${l.feature} (${l.loading > 0 ? '+' : ''}${l.loading})</span>`)
        .join(" ");

      const row = document.createElement("tr");
      row.innerHTML = `
        <td><strong style="color: var(--text-primary);">${comp.name}</strong></td>
        <td class="font-mono">${comp.coordinate_value}</td>
        <td class="font-mono">${comp.explained_variance_pct}%</td>
        <td class="font-mono">${comp.cumulative_variance_pct}%</td>
        <td>${loadingsStr}</td>
      `;
      pcaComponentsBody.appendChild(row);
    });
  }

  function renderFeaturesTable(features) {
    featuresTableBody.innerHTML = "";
    features.forEach(f => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td style="color: var(--text-muted); font-family: var(--font-mono);">${f.position}</td>
        <td><strong style="color: var(--text-primary);">${f.feature}</strong></td>
        <td class="font-mono" style="color: var(--text-primary); font-weight: 600;">${f.raw_value} <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 400;">${f.units}</span></td>
        <td class="font-mono" style="color: var(--accent-primary); font-weight: 600;">${f.normalized_value}</td>
        <td><span class="tag neutral">${f.importance_label}: ${f.importance_value}</span></td>
        <td style="font-size: 0.82rem; color: var(--text-secondary); max-width: 380px;">
          <strong style="color: var(--text-primary); display: block; margin-bottom: 0.15rem;">${f.meaning}</strong>
          <span>${f.relevance}</span>
        </td>
      `;
      featuresTableBody.appendChild(row);
    });
  }

  // Initial load execution
  executeAnalysis();
});
