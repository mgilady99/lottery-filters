// Global state
let state = {
    combinations: [],
    activeFilter: null
};

async function applyFilter(filterData) {
    const filterId = filterData.type;
    const filterRow = $(`.filter-row:has([data-filter="${filterId}"])`);
    const progressText = filterRow.find('.progress-text');
    const timeText = filterRow.find('.time-text');
    const startTime = performance.now();

    // Update status to running
    progressText.text('Calculating...');
    timeText.text('');

    try {
        const response = await fetch('https://lottery-filters.onrender.com/filters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...filterData,
                previousCombinations: state.combinations
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // Calculate execution time
        const endTime = performance.now();
        const executionTime = ((endTime - startTime) / 1000).toFixed(2);
        
        // Update status to complete with time
        progressText.text('Complete');
        timeText.text(`${executionTime}s`);
        
        state.combinations = data.combinations;
        displayResults(data.combinations);

        return data;
    } catch (error) {
        // Update status to error
        progressText.text('Error');
        timeText.text('');
        console.error('Filter error:', error);
        throw error;
    }
}

function displayResults(combinations) {
    const resultsDiv = $('#results');
    resultsDiv.empty();
    
    if (!combinations || combinations.length === 0) {
        resultsDiv.html('<p>No combinations found.</p>');
        return;
    }

    const resultsList = combinations.map((combo, index) => {
        const sortedCombo = [...combo].sort((a, b) => a - b);
        return `<div class="result-item">${index + 1}. [${sortedCombo.join(', ')}]</div>`;
    }).join('');

    resultsDiv.html(resultsList);
}
