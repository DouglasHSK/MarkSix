let allDraws = [];

document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');
    const exportCsvButton = document.getElementById('export-csv');
    const saveToDbButton = document.getElementById('save-to-db');
    const predictButton = document.getElementById('predict');

    async function fetchMarkSixData() {
        resultsContainer.innerHTML = '<div class="loading">Loading...</div>';
        try {
            // Using a proxy to bypass CORS issues
      
            const response = await fetch('/get-latest-result');
            const data = await response.json();
            
            // Get the latest result from the GraphQL response
            const latestResult = data.data.lotteryDraws[0];

            if (latestResult) {
                const drawDate = latestResult.drawDate;
                const winningNumbers = latestResult.drawResult.drawnNo;
                const extraNumber = latestResult.drawResult.xDrawnNo;

                resultsContainer.innerHTML = `
                    <div class="draw-info">
                        <strong>Date:</strong> ${drawDate}
                    </div>
                    <div class="draw-numbers">
                        ${winningNumbers.map(num => `<div class="number">${num}</div>`).join('')}
                        <div class="number extra-number">${extraNumber}</div>
                    </div>
                `;
            } else {
                resultsContainer.innerHTML = '<div class="error">Could not find the latest draw information.</div>';
            }
        } catch (error) {
            console.error('Error fetching Mark Six data:', error);
            resultsContainer.innerHTML = '<div class="error">Failed to load Mark Six results. Please try again later.</div>';
        }
    }

    function exportToCsv() {
        const exportButton = document.getElementById('export-csv');
        exportButton.disabled = true;
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';

        const worker = new Worker('export-worker.js');

        worker.onmessage = function(event) {
            const progressBar = document.getElementById('progress-bar');
            const exportButton = document.getElementById('export-csv');
            const progressContainer = document.getElementById('progress-container');

            switch (event.data.type) {
                case 'progress':
                    progressBar.style.width = `${event.data.progress}%`;
                    progressBar.textContent = `${event.data.progress}%`;
                    break;
                case 'done':
                    const blob = event.data.blob;
                    const url = URL.createObjectURL(blob);

                    const link = document.createElement("a");
                    link.setAttribute("href", url);
                    link.setAttribute("download", "mark_six_results.csv");
                    link.style.visibility = 'hidden';
                    document.body.appendChild(link);

                    link.click();

                    setTimeout(() => {
                        progressContainer.style.display = 'none';
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                        exportButton.disabled = false;
                    }, 2000);
                    break;
                case 'error':
                    alert(event.data.error);
                    progressContainer.style.display = 'none';
                    exportButton.disabled = false;
                    break;
            }
        };

        worker.onerror = function(error) {
            console.error('Error in worker:', error);
            alert('An error occurred during the export process.');
            progressContainer.style.display = 'none';
            exportButton.disabled = false;
        };

        worker.postMessage({ action: 'start-export' });
    }



    exportCsvButton.addEventListener('click', exportToCsv);
    saveToDbButton.addEventListener('click', saveToDb);

    predictButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/predict');
            const data = await response.json();
            const predictionContainer = document.getElementById('prediction-container');
            let html = '<h3>Predicted Next 10 Draws:</h3>';
            html += '<ul class="prediction-list">';
            data.predictions.forEach((prediction, index) => {
                html += `<li><strong>Set ${index + 1}:</strong> ${prediction.join(', ')}</li>`;
            });
            html += '</ul>';
            html += '<button id="copy-predictions">Copy to Clipboard</button>';
            predictionContainer.innerHTML = html;
            predictionContainer.style.display = 'block';

            const copyButton = document.getElementById('copy-predictions');
            copyButton.addEventListener('click', () => {
                const predictionText = data.predictions.map((p, i) => `Set ${i + 1}: ${p.join(', ')}`).join('\n');
                navigator.clipboard.writeText(predictionText).then(() => {
                    alert('Predictions copied to clipboard!');
                }, () => {
                    alert('Failed to copy predictions.');
                });
            });
        } catch (error) {
            console.error('Error fetching prediction:', error);
        }
    });

    fetchMarkSixData();

        function saveToDb() {
        const saveButton = document.getElementById('save-to-db');
        saveButton.disabled = true;

        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';

        const worker = new Worker('save-to-db-worker.js');

        worker.onmessage = async function(event) {
            switch (event.data.type) {
                case 'progress':
                    progressBar.style.width = `${event.data.progress}%`;
                    progressBar.textContent = `${event.data.progress}%`;
                    break;
                case 'done':
                    const allDraws = event.data.data;
                    try {
                        const response = await fetch('/save-to-db', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(allDraws),
                        });

                        if (response.ok) {
                            alert('Data saved successfully!');
                        } else {
                            alert('Failed to save data.');
                        }
                    } catch (error) {
                        console.error('Error saving data:', error);
                        alert('An error occurred while saving the data.');
                    } finally {
                        progressContainer.style.display = 'none';
                        saveButton.disabled = false;
                    }
                    break;
                case 'error':
                    alert(event.data.error);
                    progressContainer.style.display = 'none';
                    saveButton.disabled = false;
                    break;
            }
        };

        worker.onerror = function(error) {
            console.error('Error in worker:', error);
            alert('An error occurred during the save process.');
            progressContainer.style.display = 'none';
            saveButton.disabled = false;
        };

        worker.postMessage({ action: 'start-save' });
    }
});