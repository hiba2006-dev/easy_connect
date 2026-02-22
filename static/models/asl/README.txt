Place your trained ASL A-Z TensorFlow.js model files in this folder:

Required:
- model.json
- one or more *.bin weight files referenced by model.json

Optional:
- labels.json (array of class labels, e.g. ["A","B",...,"Z"])

Expected input used by this app:
- 63 float features per frame (21 hand landmarks x 3 coordinates)
- landmarks are normalized around wrist (index 0) and scaled by wrist-to-middle-MCP distance

If model files are missing, the app falls back to simple heuristic detection (A/B/L only).
