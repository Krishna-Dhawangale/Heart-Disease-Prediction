document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Convert fields to correct types (int/float)
    const payload = {
        age: parseInt(data.age),
        sex: parseInt(data.sex),
        cp: parseInt(data.cp),
        trestbps: parseInt(data.trestbps),
        chol: parseInt(data.chol),
        fbs: parseInt(data.fbs),
        restecg: parseInt(data.restecg),
        thalach: parseInt(data.thalach),
        exang: parseInt(data.exang),
        oldpeak: parseFloat(data.oldpeak),
        slope: parseInt(data.slope),
        ca: parseInt(data.ca),
        thal: parseInt(data.thal)
    };

    const submitBtn = document.getElementById('predict-btn');
    submitBtn.innerText = 'Analyzing Cardiac Data...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Prediction request failed.');
        }

        const result = await response.json();
        const probability = result.probability;
        const isHighRisk = result.prediction === 1;

        // Show results
        const resultsArea = document.getElementById('results-area');
        resultsArea.classList.remove('hidden');
        resultsArea.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Update score and gauge
        const riskScoreText = document.getElementById('risk-score');
        const riskText = document.getElementById('risk-text');
        const gauge = document.getElementById('gauge-progress');
        const statusBadge = document.getElementById('prediction-status');

        // Animate count up
        animateValue(riskScoreText, 0, probability, 1000);

        // Update Gauge
        const offset = 125 - (probability / 100) * 125;
        gauge.style.strokeDashoffset = offset;
        
        // Update Risk message and colors
        if (isHighRisk) {
            riskText.innerText = "Alert: High Cardiac Risk Detected";
            riskText.style.color = '#ef4444';
            statusBadge.innerText = 'Attention Advised';
            statusBadge.className = 'status-badge status-danger';
        } else {
            riskText.innerText = "Status: Healthy Profile Detected";
            riskText.style.color = '#22c55e';
            statusBadge.innerText = 'Nominal Score';
            statusBadge.className = 'status-badge status-safe';
        }

    } catch (error) {
        console.error(error);
        alert('An error occurred during prediction. Please check your data or server status.');
    } finally {
        submitBtn.innerText = 'Analyze Health Probability';
        submitBtn.disabled = false;
    }
});

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start) + '%';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
