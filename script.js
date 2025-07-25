let allDraws = [];

document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');
    const exportCsvButton = document.getElementById('export-csv');

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

    async function exportToCsv() {
        const exportButton = document.getElementById('export-csv');
        exportButton.disabled = true;
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';

        let allDraws = [];
        const totalYears = new Date().getFullYear() - 1993 + 1;

        for (let i = 0; i < totalYears; i++) {
            try {
                const response = await fetch(`/get-results-by-page?page=${i + 1}`);
                const data = await response.json();
                if (data.data && data.data.lotteryDraws) {
                    allDraws = allDraws.concat(data.data.lotteryDraws);
                }

                const progress = Math.round(((i + 1) / totalYears) * 100);
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${progress}%`;

            } catch (error) {
                console.error(`Error fetching data for year ${1993 + i}:`, error);
            }
        }

        if (allDraws.length === 0) {
            alert('No data available to export.');
            progressContainer.style.display = 'none';
            exportButton.disabled = false;
            return;
        }

        sortdata=allDraws.sort((a, b) => b.drawDate > a.drawDate? 1 : -1);

        const headers = ['ID', 'Draw Date', 'No. 1', 'No. 2', 'No. 3', 'No. 4', 'No. 5', 'No. 6', 'Extra Number'];
        const rows = sortdata.map(draw => {
            const id = draw.id;
            const drawDate = draw.drawDate;
            const winningNumbers = draw.drawResult.drawnNo;
            const extraNumber = draw.drawResult.xDrawnNo;
            return [id, drawDate, ...winningNumbers, extraNumber];
        });

        const csvContent = headers.join(",") + "\n" + rows.map(e => e.join(",")).join("\n");
        const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });
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

    }

    exportCsvButton.addEventListener('click', exportToCsv);
    fetchMarkSixData();
});