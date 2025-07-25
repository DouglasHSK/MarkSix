self.onmessage = async function(event) {
    if (event.data.action === 'start-export') {
        const totalYears = new Date().getFullYear() - 1993 + 1;
        let allDraws = [];
        let completedRequests = 0;
        const batchSize = 5;
        const pages = Array.from({ length: totalYears }, (_, i) => i + 1);

        for (let i = 0; i < pages.length; i += batchSize) {
            const batch = pages.slice(i, i + batchSize);
            const promises = batch.map(page =>
                fetch(`/get-results-by-page?page=${page}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        completedRequests++;
                        const progress = Math.round((completedRequests / totalYears) * 100);
                        self.postMessage({ type: 'progress', progress: progress });
                        return data.data.lotteryDraws || [];
                    })
                    .catch(error => {
                        console.error(`Error fetching data for page ${page}:`, error);
                        completedRequests++;
                        const progress = Math.round((completedRequests / totalYears) * 100);
                        self.postMessage({ type: 'progress', progress: progress });
                        return [];
                    })
            );
            const batchResults = await Promise.all(promises);
            allDraws = allDraws.concat(...batchResults);
        }

        if (!allDraws || allDraws.length === 0) {
            self.postMessage({ type: 'error', error: 'No data available to export.' });
            return;
        }

        const sortedData = allDraws.sort((a, b) => b.drawDate > a.drawDate ? 1 : -1);

        const headers = ['ID', 'Draw Date', 'No. 1', 'No. 2', 'No. 3', 'No. 4', 'No. 5', 'No. 6', 'Extra Number'];
        const rows = sortedData.map(draw => {
            const id = draw.id;
            const drawDate = draw.drawDate;
            const winningNumbers = draw.drawResult.drawnNo;
            const extraNumber = draw.drawResult.xDrawnNo;
            return [id, drawDate, ...winningNumbers, extraNumber];
        });

        const csvContent = headers.join(",") + "\n" + rows.map(e => e.join(",")).join("\n");
        const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });

        self.postMessage({ type: 'done', blob: blob });
    }
};