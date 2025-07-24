let allDraws = [];

document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');
    const exportCsvButton = document.getElementById('export-csv');

    async function fetchMarkSixData() {
        resultsContainer.innerHTML = '<div class="loading">Loading...</div>';
        try {
            // Using a proxy to bypass CORS issues
      
            const response = await fetch('/get-mark-six-data');
            const data = await response.json();
            allDraws = data.data.lotteryDraws;
            
            // Get the latest result from the GraphQL response
            const latestResult = allDraws[0];

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
        if (allDraws.length === 0) {
            alert('No data available to export.');
            return;
        }

        const headers = ['ID', 'Draw Date', 'No. 1', 'No. 2', 'No. 3', 'No. 4', 'No. 5', 'No. 6', 'Extra Number'];
        const rows = allDraws.map(draw => {
            const id = draw.id;
            const drawDate = draw.drawDate;
            const winningNumbers = draw.drawResult.drawnNo;
            const extraNumber = draw.drawResult.xDrawnNo;
            return [id, drawDate, ...winningNumbers, extraNumber];
        });

        let csvContent = "data:text/csv;charset=utf-8," 
            + headers.join(",") + "\n" 
            + rows.map(e => e.join(",")).join("\n");

        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "mark_six_results.csv");
        document.body.appendChild(link); // Required for FF

        link.click();
        document.body.removeChild(link);
    }

    exportCsvButton.addEventListener('click', exportToCsv);
    fetchMarkSixData();
});