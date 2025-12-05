import React, { useState } from "react";

const API_BASE = "http://localhost:8000";

const severityOrder = ["critical", "high", "medium", "low", "info", "unknown"];

function severityBadgeClass(sev) {
  const s = (sev || "unknown").toLowerCase();
  return (
    "badge " +
    (s === "critical"
      ? "badge-critical"
      : s === "high"
      ? "badge-high"
      : s === "medium"
      ? "badge-medium"
      : s === "low"
      ? "badge-low"
      : s === "info"
      ? "badge-info"
      : "badge-unknown")
  );
}

function App() {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [scanError, setScanError] = useState("");
  const [scanData, setScanData] = useState(null);

  const [selectedSeverityFilter, setSelectedSeverityFilter] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFinding, setSelectedFinding] = useState(null);

  const handleScan = async () => {
    if (!target.trim()) return;
    setLoading(true);
    setScanError("");
    setSelectedFile(null);
    setSelectedFinding(null);

    try {
      const res = await fetch(`${API_BASE}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }

      const data = await res.json();
      setScanData(data);

      // Auto-select first file with findings
      const filePaths = Object.keys(data.results || {});
      if (filePaths.length > 0) {
        setSelectedFile(filePaths[0]);
      }
    } catch (err) {
      console.error(err);
      setScanError(String(err));
    } finally {
      setLoading(false);
    }
  };

  const findingsByFile = scanData?.results || {};
  const severityCounts = scanData?.severity_counts || {};

  // Filter files by severity filter
  const fileList = Object.entries(findingsByFile).filter(([file, findings]) => {
    if (!selectedSeverityFilter) return true;
    return findings.some((f) => f.severity === selectedSeverityFilter);
  });

  const currentFindings = selectedFile ? findingsByFile[selectedFile] || [] : [];

  return (
    <div className="app">
      <header className="header">
        <div>
          <div className="header-title">CyberWarriorV2 Dashboard</div>
          <div className="header-sub">
            AI bug bounty scanner · code vulnerabilities · auto patch suggestions
          </div>
        </div>
        <div style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
          API: <code>{API_BASE}</code>
        </div>
      </header>

      <div className="main-layout">
        {/* LEFT: Target + File list */}
        <div className="panel">
          <div className="panel-header">
            <h2>Target & Files</h2>
          </div>
          <div className="input-row">
            <input
              placeholder="Git URL or local path (e.g. E:\Project)"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            />
            <button onClick={handleScan} disabled={loading}>
              {loading ? "Scanning..." : "Scan"}
            </button>
          </div>
          {scanError && (
            <div style={{ color: "#fca5a5", fontSize: "0.75rem", marginBottom: "0.5rem" }}>
              {scanError}
            </div>
          )}

          <div className="severity-badges">
            {severityOrder.map((sev) => {
              const count = severityCounts[sev] || 0;
              if (!count && !selectedSeverityFilter && !scanData) return null;

              return (
                <div
                  key={sev}
                  className={
                    severityBadgeClass(sev) +
                    (selectedSeverityFilter === sev ? " selected" : "")
                  }
                  onClick={() =>
                    setSelectedSeverityFilter(
                      selectedSeverityFilter === sev ? null : sev
                    )
                  }
                >
                  {sev.toUpperCase()} {count ? `(${count})` : ""}
                </div>
              );
            })}
          </div>

          <div className="file-list">
            {fileList.length === 0 && scanData && (
              <div style={{ fontSize: "0.8rem", color: "#9ca3af" }}>
                No files with findings for this filter.
              </div>
            )}
            {fileList.map(([filePath, findings]) => (
              <div
                key={filePath}
                className={
                  "file-item" + (selectedFile === filePath ? " selected" : "")
                }
                onClick={() => {
                  setSelectedFile(filePath);
                  setSelectedFinding(null);
                }}
              >
                <span
                  style={{
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                  title={filePath}
                >
                  {filePath}
                </span>
                <span className="file-count">{findings.length}</span>
              </div>
            ))}
          </div>
        </div>

        {/* MIDDLE: Findings list */}
        <div className="panel">
          <div className="panel-header">
            <h2>Findings</h2>
            <div style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
              {selectedFile
                ? `${currentFindings.length} findings`
                : "Select a file"}
            </div>
          </div>

          <div className="findings-list">
            {selectedFile && currentFindings.length === 0 && (
              <div style={{ fontSize: "0.8rem", color: "#9ca3af" }}>
                No findings in this file.
              </div>
            )}

            {currentFindings.map((f, idx) => (
              <div
                key={idx}
                className={
                  "finding-item" +
                  (selectedFinding === f ? " selected" : "")
                }
                onClick={() => setSelectedFinding(f)}
              >
                <div className="finding-header">
                  <span className="finding-severity">
                    {(f.severity || "unknown").toUpperCase()}
                  </span>
                  <span className="finding-score">
                    score: {f.ensemble_score?.toFixed(2) ?? "?"}
                  </span>
                </div>
                <div className="finding-snippet">
                  {f.snippet?.slice(0, 220) || "<no snippet>"}
                  {f.snippet && f.snippet.length > 220 ? "…" : ""}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT: Details & Patch */}
        <div className="panel">
          <div className="panel-header">
            <h2>Details & Patch</h2>
          </div>

          {selectedFinding ? (
            <div className="details-body">
              <div className="details-section">
                <strong>Severity:</strong> {selectedFinding.severity}
                {" · "}
                <strong>Ensemble Score:</strong>{" "}
                {selectedFinding.ensemble_score?.toFixed(3)}
                {" · "}
                <strong>Votes:</strong> {selectedFinding.votes_vulnerable}/
                {selectedFinding.total_models}
              </div>

              <div className="details-section">
                <strong>CVSS:</strong>{" "}
                {selectedFinding.cvss_score
                  ? `${selectedFinding.cvss_score} (${selectedFinding.cvss_severity})`
                  : "N/A"}
                {selectedFinding.cvss_cve && (
                  <>
                    {" · "}
                    <strong>CVE:</strong> {selectedFinding.cvss_cve}
                  </>
                )}
              </div>

              <div className="details-section">
                <strong>Snippet:</strong>
                <pre>{selectedFinding.snippet}</pre>
              </div>

              <div className="details-section">
                <strong>Model outputs:</strong>
                <pre>
                  {JSON.stringify(
                    selectedFinding.model_outputs || [],
                    null,
                    2
                  )}
                </pre>
              </div>

              <div className="details-section">
                <strong>Patch suggestion:</strong>
                {selectedFinding.patch && selectedFinding.patch.success ? (
                  <>
                    <div style={{ marginBottom: "0.25rem" }}>
                      <em>{selectedFinding.patch.explanation}</em>
                    </div>
                    <div className="diff-block">
                      {(selectedFinding.patch.patch_diff || "")
                        .split("\n")
                        .map((line, i) => {
                          let cls = "";
                          if (line.startsWith("+")) cls = "diff-add";
                          else if (line.startsWith("-")) cls = "diff-del";
                          return (
                            <div key={i} className={cls}>
                              {line}
                            </div>
                          );
                        })}
                    </div>
                  </>
                ) : (
                  <div style={{ fontSize: "0.8rem", color: "#9ca3af" }}>
                    {selectedFinding.patch
                      ? selectedFinding.patch.explanation ||
                        "No patch available."
                      : "No patch generated (severity too low or patcher disabled)."}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div style={{ fontSize: "0.8rem", color: "#9ca3af" }}>
              Select a finding on the middle panel to view details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
