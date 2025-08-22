// Simulation interface handler
async function runSimulation() {
    try {
        // Get parameters from form
        const params = {
            alice: {
                mu1: parseFloat(document.getElementById('alice-mu1').value),
                mu2: parseFloat(document.getElementById('alice-mu2').value),
                p1: parseFloat(document.getElementById('alice-p1').value)
            },
            bob: {
                darkCount: parseFloat(document.getElementById('bob-dark-count').value),
                timeBin: parseFloat(document.getElementById('bob-time-bin').value)
            },
            channel: {
                loss: parseFloat(document.getElementById('channel-loss').value),
                syncError: parseFloat(document.getElementById('channel-sync-error').value)
            },
            processing: {
                blockSize: parseInt(document.getElementById('proc-block-size').value),
                maxOffset: parseInt(document.getElementById('proc-max-offset').value)
            }
        };

        // Disable run button and show loading state
        const runButton = document.querySelector('button');
        const originalText = runButton.textContent;
        runButton.disabled = true;
        runButton.textContent = 'Running Simulation...';

        // Clear any previous error messages
        const statsDiv = document.getElementById('simulation-stats');
        statsDiv.innerHTML = '<div class="stats-container">Running simulation...</div>';

        // Send simulation request
        const response = await fetch('http://localhost:5000/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        const data = await response.json();
        
        if (data.status === 'success') {
            // Update plots and statistics
            window.visualizationManager.updatePlots(data.results);
        } else {
            window.visualizationManager.showError(data.message || 'Simulation failed');
        }
    } catch (error) {
        window.visualizationManager.showError(`Failed to run simulation: ${error.message}`);
    } finally {
        // Re-enable run button
        const runButton = document.querySelector('button');
        runButton.disabled = false;
        runButton.textContent = 'Run Simulation';
    }
}

function updateProbabilities() {
    const signalProb = parseFloat(document.getElementById('alice-p1').value);
    if (isNaN(signalProb) || signalProb < 0 || signalProb > 1) return;
    
    const decoyProb = Math.round((1 - signalProb) * 100) / 100;
    document.getElementById('decoy-prob').textContent = decoyProb;
    
    // Update probability bars
    const signalBar = document.querySelector('.signal-prob');
    const decoyBar = document.querySelector('.decoy-prob');
    signalBar.style.width = `${signalProb * 100}%`;
    decoyBar.style.width = `${decoyProb * 100}%`;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initialize probability display
    updateProbabilities();

    // Check backend health
    fetch('http://localhost:5000/api/health')
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'healthy') {
                window.visualizationManager.showError('Backend server is not responding correctly');
            }
        })
        .catch(error => {
            window.visualizationManager.showError('Cannot connect to backend server. Please ensure it is running.');
        });
});