// Visualization handler for quantum channel simulation

class VisualizationManager {
    constructor() {
        // Initialize empty plots
        this.initializePlots();
    }

    initializePlots() {
        // Create subplot layout
        const trace1 = {
            x: [],
            y: [],
            name: 'Cross-correlation',
            type: 'scatter',
            line: {
                color: '#1f77b4',
                width: 2
            }
        };

        const trace2 = {
            x: [],
            y: [],
            name: 'Photon Counts',
            type: 'scatter',
            line: {
                color: '#ff7f0e',
                width: 2
            },
            xaxis: 'x2',
            yaxis: 'y2'
        };

        const layout = {
            title: {
                text: 'Quantum Channel Simulation Results',
                font: { size: 24 }
            },
            showlegend: true,
            legend: {
                x: 1.1,
                y: 1,
                xanchor: 'left'
            },
            grid: {
                rows: 2,
                columns: 1,
                pattern: 'independent',
                roworder: 'top to bottom',
                subplots: [['xy'], ['x2y2']],
                rowheight: [0.5, 0.5]
            },
            height: 800,
            margin: {
                l: 80,
                r: 150,
                t: 100,
                b: 80
            },
            xaxis: {
                title: {
                    text: 'Time Offset (bins)',
                    font: { size: 14 }
                },
                showgrid: true,
                gridcolor: '#e6e6e6',
                zeroline: true,
                zerolinecolor: '#969696',
                zerolinewidth: 1
            },
            yaxis: {
                title: {
                    text: 'Cross-correlation Amplitude',
                    font: { size: 14 }
                },
                showgrid: true,
                gridcolor: '#e6e6e6',
                zeroline: true,
                zerolinecolor: '#969696',
                zerolinewidth: 1
            },
            xaxis2: {
                title: {
                    text: 'Time (ns)',
                    font: { size: 14 }
                },
                showgrid: true,
                gridcolor: '#e6e6e6',
                zeroline: true,
                zerolinecolor: '#969696',
                zerolinewidth: 1
            },
            yaxis2: {
                title: {
                    text: 'Photon Counts',
                    font: { size: 14 }
                },
                showgrid: true,
                gridcolor: '#e6e6e6',
                zeroline: true,
                zerolinecolor: '#969696',
                zerolinewidth: 1
            }
        };

        Plotly.newPlot('chart-placeholder', [trace1, trace2], layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['lasso2d', 'select2d']
        });
    }

    updatePlots(results) {
        // Update plots with simulation results
        const update = {
            'x': [
                results.time_points,  // For cross-correlation
                results.time_points   // For photon counts
            ],
            'y': [
                results.cross_correlation,
                results.counts
            ]
        };

        // Add vertical line at detected peak
        if (results.peak_position !== undefined) {
            const shapes = [{
                type: 'line',
                x0: results.peak_position,
                x1: results.peak_position,
                y0: 0,
                y1: Math.max(...results.cross_correlation),
                xref: 'x',
                yref: 'y',
                line: {
                    color: '#d62728',
                    width: 2,
                    dash: 'dash'
                },
                layer: 'above'
            }];
            
            const annotations = [{
                x: results.peak_position,
                y: Math.max(...results.cross_correlation),
                xref: 'x',
                yref: 'y',
                text: 'Peak Detected',
                showarrow: true,
                arrowhead: 2,
                arrowsize: 1,
                arrowwidth: 2,
                ax: 40,
                ay: -40,
                font: {
                    size: 12,
                    color: '#d62728'
                }
            }];
            
            Plotly.relayout('chart-placeholder', {
                shapes: shapes,
                annotations: annotations
            });
        }

        Plotly.update('chart-placeholder', update);

        // Update statistics display
        this.displayStatistics(results.statistics);
    }

    displayStatistics(stats) {
        // Create statistics display
        const statsHtml = `
            <div class="stats-container">
                <h3>Simulation Results</h3>
                <table class="stats-table">
                    <tr>
                        <td>Total Photon Counts:</td>
                        <td>${stats.total_counts.toExponential(2)}</td>
                    </tr>
                    <tr>
                        <td>Mean Count Rate:</td>
                        <td>${stats.mean_count_rate.toExponential(2)} Hz</td>
                    </tr>
                    <tr>
                        <td>Quantum Bit Error Rate:</td>
                        <td>${(stats.qber * 100).toFixed(2)}%</td>
                    </tr>
                    <tr>
                        <td>Synchronization Status:</td>
                        <td class="${stats.sync_success ? 'success' : 'failure'}">
                            ${stats.sync_success ? 'Successfully synchronized' : 'Synchronization failed'}
                        </td>
                    </tr>
                </table>
            </div>
        `;

        // Add statistics below the plots
        const statsDiv = document.getElementById('simulation-stats');
        if (statsDiv) {
            statsDiv.innerHTML = statsHtml;
        }
    }

    showError(message) {
        // Display error message
        const errorHtml = `
            <div class="error-message">
                <h3>Error</h3>
                <p>${message}</p>
            </div>
        `;

        const statsDiv = document.getElementById('simulation-stats');
        if (statsDiv) {
            statsDiv.innerHTML = errorHtml;
        }
    }
}

// Initialize visualization manager when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.visualizationManager = new VisualizationManager();
});