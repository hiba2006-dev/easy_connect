(function () {
    const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
    const STORAGE_KEY = "asl_calibration_v1";
    const GLOBAL_CALIBRATION_URL = "/static/asl_calibration_global.json";

    const video = document.getElementById("camera");
    const canvas = document.getElementById("camera-overlay");
    const resultEl = document.getElementById("ai-result");
    const startBtn = document.getElementById("start-detection");
    const stopBtn = document.getElementById("stop-detection");
    const letterSelect = document.getElementById("calibration-letter");
    const captureBtn = document.getElementById("capture-sample");
    const clearBtn = document.getElementById("clear-samples");
    const exportBtn = document.getElementById("export-samples");
    const importBtn = document.getElementById("import-samples");
    const importFile = document.getElementById("import-samples-file");
    const infoEl = document.getElementById("ai-calibration-info");

    if (!video || !canvas || !resultEl || !startBtn || !stopBtn || !letterSelect || !captureBtn || !clearBtn || !exportBtn || !importBtn || !importFile || !infoEl) {
        return;
    }

    const ctx = canvas.getContext("2d");
    let camera = null;
    let running = false;
    let lastLandmarks = null;
    const smoothWindow = [];

    let dataset = {};

    function initDataset() {
        LETTERS.forEach((letter) => {
            if (!dataset[letter]) dataset[letter] = [];
        });
    }

    function saveDataset() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(dataset));
    }

    function loadDatasetFromStorage() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            const parsed = JSON.parse(raw);
            if (parsed && typeof parsed === "object") {
                dataset = parsed;
            }
        } catch {
            dataset = {};
        }
        initDataset();
    }

    async function loadGlobalDataset() {
        try {
            const res = await fetch(GLOBAL_CALIBRATION_URL, { cache: "no-store" });
            if (!res.ok) return false;
            const parsed = await res.json();
            const source = parsed && parsed.data ? parsed.data : parsed;
            if (!source || typeof source !== "object") return false;

            const next = {};
            LETTERS.forEach((letter) => {
                const arr = Array.isArray(source[letter]) ? source[letter].filter(isVector) : [];
                next[letter] = arr.slice(0, 200);
            });
            dataset = next;
            saveDataset();
            return true;
        } catch {
            return false;
        }
    }

    function updateCalibrationInfo() {
        const parts = LETTERS.map((l) => `${l}:${dataset[l].length}`);
        infoEl.textContent = `Exemples captures -> ${parts.join(" | ")}`;
    }

    function fillLetters() {
        LETTERS.forEach((letter) => {
            const opt = document.createElement("option");
            opt.value = letter;
            opt.textContent = letter;
            letterSelect.appendChild(opt);
        });
        letterSelect.value = "A";
    }

    function dist(a, b) {
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    function normalizeLandmarks(lm) {
        const wrist = lm[0];
        const middleMcp = lm[9];
        const scale = Math.max(dist(wrist, middleMcp), 1e-5);
        const out = [];
        for (const p of lm) {
            out.push((p.x - wrist.x) / scale);
            out.push((p.y - wrist.y) / scale);
            out.push((p.z - wrist.z) / scale);
        }
        return out;
    }

    function euclidean(a, b) {
        let s = 0;
        for (let i = 0; i < a.length; i += 1) {
            const d = a[i] - b[i];
            s += d * d;
        }
        return Math.sqrt(s);
    }

    function nearestDistance(vec, letterFilter) {
        let best = Number.POSITIVE_INFINITY;
        for (const letter of LETTERS) {
            if (letterFilter && !letterFilter(letter)) continue;
            for (const sample of dataset[letter]) {
                const d = euclidean(vec, sample);
                if (d < best) best = d;
            }
        }
        return best;
    }

    function predictKnn(vec, k = 5) {
        const all = [];
        for (const letter of LETTERS) {
            for (const sample of dataset[letter]) {
                all.push({ letter, d: euclidean(vec, sample) });
            }
        }
        if (all.length === 0) return { label: "--", confidence: 0 };

        all.sort((x, y) => x.d - y.d);
        const top = all.slice(0, Math.min(k, all.length));

        const votes = new Map();
        for (const item of top) {
            const weight = 1 / Math.max(item.d, 1e-6);
            votes.set(item.letter, (votes.get(item.letter) || 0) + weight);
        }

        let bestLabel = "--";
        let bestScore = 0;
        let total = 0;
        for (const [label, score] of votes.entries()) {
            total += score;
            if (score > bestScore) {
                bestScore = score;
                bestLabel = label;
            }
        }

        const confidence = total > 0 ? bestScore / total : 0;
        return { label: bestLabel, confidence };
    }

    function smoothPrediction(pred) {
        smoothWindow.push(pred);
        if (smoothWindow.length > 6) smoothWindow.shift();

        const scores = new Map();
        for (const p of smoothWindow) {
            scores.set(p.label, (scores.get(p.label) || 0) + p.confidence);
        }
        let label = "--";
        let score = 0;
        for (const [l, s] of scores.entries()) {
            if (s > score) {
                score = s;
                label = l;
            }
        }
        return {
            label,
            confidence: Math.min(score / smoothWindow.length, 1),
        };
    }

    function updateCanvasSize() {
        const w = video.videoWidth || 640;
        const h = video.videoHeight || 480;
        canvas.width = w;
        canvas.height = h;
    }

    const hands = new Hands({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
        maxNumHands: 1,
        modelComplexity: 1,
        minDetectionConfidence: 0.6,
        minTrackingConfidence: 0.6,
    });

    hands.onResults((results) => {
        updateCanvasSize();
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
            lastLandmarks = null;
            resultEl.textContent = "Signe detecte: --";
            return;
        }

        const lm = results.multiHandLandmarks[0];
        lastLandmarks = lm;
        drawConnectors(ctx, lm, HAND_CONNECTIONS, { color: "#22c55e", lineWidth: 4 });
        drawLandmarks(ctx, lm, { color: "#2563eb", lineWidth: 2, radius: 3 });

        const vec = normalizeLandmarks(lm);
        const raw = predictKnn(vec, 5);
        const pred = smoothPrediction(raw);
        const pct = Math.round(pred.confidence * 100);
        resultEl.textContent = `Signe detecte: ${pred.label} (${pct}%)`;
    });

    async function startDetection() {
        if (running) return;
        try {
            camera = new Camera(video, {
                onFrame: async () => {
                    if (!running) return;
                    await hands.send({ image: video });
                },
                width: 960,
                height: 540,
            });
            running = true;
            await camera.start();
        } catch {
            running = false;
            resultEl.textContent = "Erreur camera: autorisation refusee ou camera indisponible.";
        }
    }

    function stopDetection() {
        running = false;
        if (camera && camera.video && camera.video.srcObject) {
            const tracks = camera.video.srcObject.getTracks();
            tracks.forEach((t) => t.stop());
        }
        smoothWindow.length = 0;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        resultEl.textContent = "Signe detecte: --";
    }

    function captureSample() {
        if (!lastLandmarks) {
            resultEl.textContent = "Signe detecte: -- (aucune main detectee)";
            return;
        }
        const letter = letterSelect.value;
        const vec = normalizeLandmarks(lastLandmarks);

        // Prevent adding near-identical sample already used by another letter.
        const nearestOther = nearestDistance(vec, (l) => l !== letter);
        if (Number.isFinite(nearestOther) && nearestOther < 0.08) {
            resultEl.textContent = `Signe detecte: -- (capture refusee: trop proche de ${letter} mais aussi d'une autre lettre, changez la pose)`;
            return;
        }

        // Prevent duplicate spam for same letter.
        const nearestSame = nearestDistance(vec, (l) => l === letter);
        if (Number.isFinite(nearestSame) && nearestSame < 0.02) {
            resultEl.textContent = `Signe detecte: -- (capture refusee: doublon ${letter})`;
            return;
        }

        dataset[letter].push(vec);
        if (dataset[letter].length > 80) {
            dataset[letter].shift();
        }
        saveDataset();
        updateCalibrationInfo();
        resultEl.textContent = `Signe detecte: -- (exemple ${letter} enregistre)`;
    }

    function clearSamples() {
        dataset = {};
        initDataset();
        saveDataset();
        updateCalibrationInfo();
    }

    function exportSamples() {
        const payload = {
            version: 1,
            type: "asl_calibration",
            created_at: new Date().toISOString(),
            data: dataset,
        };
        const blob = new Blob([JSON.stringify(payload)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "asl_calibration.json";
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    }

    function isVector(v) {
        return Array.isArray(v) && v.length === 63 && v.every((n) => Number.isFinite(n));
    }

    function importSamplesFromObject(parsed) {
        const source = parsed && parsed.data ? parsed.data : parsed;
        if (!source || typeof source !== "object") {
            throw new Error("Format JSON invalide.");
        }

        const next = {};
        LETTERS.forEach((letter) => {
            const arr = Array.isArray(source[letter]) ? source[letter].filter(isVector) : [];
            next[letter] = arr.slice(0, 200);
        });

        dataset = next;
        saveDataset();
        updateCalibrationInfo();
    }

    async function handleImportFile(file) {
        const text = await file.text();
        const parsed = JSON.parse(text);
        importSamplesFromObject(parsed);
    }

    startBtn.addEventListener("click", startDetection);
    stopBtn.addEventListener("click", stopDetection);
    captureBtn.addEventListener("click", captureSample);
    clearBtn.addEventListener("click", clearSamples);
    exportBtn.addEventListener("click", exportSamples);
    importBtn.addEventListener("click", () => importFile.click());
    importFile.addEventListener("change", async (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        try {
            await handleImportFile(file);
            resultEl.textContent = "Signe detecte: -- (calibration importee)";
        } catch {
            resultEl.textContent = "Signe detecte: -- (echec import JSON)";
        } finally {
            importFile.value = "";
        }
    });

    async function init() {
        fillLetters();
        loadDatasetFromStorage();
        const loadedGlobal = await loadGlobalDataset();
        updateCalibrationInfo();
        if (loadedGlobal) {
            resultEl.textContent = "Signe detecte: -- (calibration globale chargee)";
        }
    }

    init();
})();
