self.onmessage = async function(event) {
    if (event.data.action === 'start-save') {
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
            self.postMessage({ type: 'error', error: 'No data available to save.' });
            return;
        }

        self.postMessage({ type: 'done', data: allDraws });
    }
};