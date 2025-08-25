document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('stateForm');
    const statesDisplay = document.getElementById('statesDisplay');

    function validateInput(value, min, max = null) {
        const num = parseFloat(value);
        if (isNaN(num) || num < min) return false;
        if (max !== null && num > max) return false;
        return true;
    }

    function showError(elementId, show, message = null) {
        const error = document.getElementById(elementId + 'Error');
        if (error) {
            error.textContent = message || error.textContent;
            error.style.display = show ? 'block' : 'none';
        }
    }

    function generateStates(signalPower, decoyPower, signalProb, size) {
        // Create arrays to store states and their types
        const states = new Array(size);
        const types = new Array(size);
        
        for (let i = 0; i < size; i++) {
            // Generate random number between 0 and 1
            const rand = Math.random();
            
            // Assign state based on probability
            if (rand < signalProb) {
                states[i] = signalPower;
                types[i] = 'signal';
            } else {
                states[i] = decoyPower;
                types[i] = 'decoy';
            }
        }
        
        return { states, types };
    }

    function visualizeStates(states, types) {
        // Clear previous visualization
        statesDisplay.innerHTML = '';
        
        // Create visualization container
        const container = document.createElement('div');
        container.style.display = 'flex';
        container.style.flexWrap = 'wrap';
        container.style.gap = '5px';
        container.style.marginBottom = '20px';
        
        // Add states visualization
        states.forEach((state, index) => {
            const stateElement = document.createElement('div');
            stateElement.style.width = '20px';
            stateElement.style.height = '20px';
            stateElement.style.backgroundColor = types[index] === 'signal' ? '#4CAF50' : '#2196F3';
            stateElement.style.borderRadius = '50%';
            stateElement.title = `State ${index + 1}: ${types[index]} (${state.toFixed(3)})`;
            container.appendChild(stateElement);
        });
        
        // Add legend
        const legend = document.createElement('div');
        legend.style.marginBottom = '20px';
        legend.innerHTML = `
            <div style="display: flex; gap: 20px; justify-content: center;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background-color: #4CAF50; border-radius: 50%; margin-right: 8px;"></div>
                    <span>Signal State (${states[0].toFixed(3)})</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background-color: #2196F3; border-radius: 50%; margin-right: 8px;"></div>
                    <span>Decoy State (${states.find(s => s !== states[0]).toFixed(3)})</span>
                </div>
            </div>
        `;
        
        // Add statistics
        const signalCount = types.filter(type => type === 'signal').length;
        const decoyCount = types.filter(type => type === 'decoy').length;
        
        const stats = document.createElement('div');
        stats.innerHTML = `
            <h3>Statistics:</h3>
            <p>Total States: ${states.length}</p>
            <p>Signal States: ${signalCount} (${((signalCount/states.length)*100).toFixed(1)}%)</p>
            <p>Decoy States: ${decoyCount} (${((decoyCount/states.length)*100).toFixed(1)}%)</p>
        `;
        
        statesDisplay.appendChild(legend);
        statesDisplay.appendChild(container);
        statesDisplay.appendChild(stats);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const signalPower = parseFloat(document.getElementById('signalPower').value);
        const decoyPower = parseFloat(document.getElementById('decoyPower').value);
        const signalProb = parseFloat(document.getElementById('signalProb').value);
        const arraySize = parseInt(document.getElementById('arraySize').value);
        
        // Validate inputs
        let isValid = true;
        
        if (!validateInput(signalPower, 0)) {
            showError('signalPower', true);
            isValid = false;
        } else {
            showError('signalPower', false);
        }
        
        if (!validateInput(decoyPower, 0)) {
            showError('decoyPower', true);
            isValid = false;
        } else {
            showError('decoyPower', false);
        }
        
        if (!validateInput(signalProb, 0, 1)) {
            showError('signalProb', true);
            isValid = false;
        } else {
            showError('signalProb', false);
        }
        
        if (!validateInput(arraySize, 1, 1000)) {
            showError('arraySize', true);
            isValid = false;
        } else {
            showError('arraySize', false);
        }
        
        if (isValid) {
            // Generate and visualize states
            const { states, types } = generateStates(signalPower, decoyPower, signalProb, arraySize);
            visualizeStates(states, types);
        }
    });
});