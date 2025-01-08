// Global state
let state = {
    combinations: [],
    activeFilter: null
};

function showToast(message, type = 'info') {
    const toast = $('<div>')
        .addClass(`toast toast-${type}`)
        .text(message)
        .appendTo('body');
    
    setTimeout(() => toast.remove(), 3000);
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

// API calls
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
        showToast(error.message, 'error');
        throw error;
    }
}

// Event Handlers
$(document).ready(function() {
    // Base filter
    $('.btn-run[data-filter="base"]').click(async function() {
        try {
            await applyFilter({
                type: 'base',
                totalNumbers: parseInt($('#totalNumbers').val()),
                drawSize: parseInt($('#drawSize').val())
            });
        } catch (error) {
            console.error('Base filter error:', error);
        }
    });

    // Odd/Even filter
    $('.btn-run[data-filter="odd"]').click(async function() {
        try {
            await applyFilter({
                type: 'odd_even',
                minOdd: parseInt($('#oddMin').val()),
                maxOdd: parseInt($('#oddMax').val())
            });
        } catch (error) {
            console.error('Odd/Even filter error:', error);
        }
    });

    // Distance filter
    $('.btn-run[data-filter="distance"]').click(async function() {
        try {
            await applyFilter({
                type: 'distance',
                minDistance: parseInt($('#distanceMin').val()),
                maxDistance: parseInt($('#maxDistance').val())
            });
        } catch (error) {
            console.error('Distance filter error:', error);
        }
    });

    // Sum filter
    $('.btn-run[data-filter="sum"]').click(async function() {
        try {
            await applyFilter({
                type: 'sum',
                sumMin: parseInt($('#sumMin').val()),
                sumMax: parseInt($('#sumMax').val())
            });
        } catch (error) {
            console.error('Sum filter error:', error);
        }
    });

    // Include filter
    $('.btn-run[data-filter="include"]').click(async function() {
        try {
            const numbers = $('#mustInclude').val()
                .split(',')
                .map(n => parseInt(n.trim()))
                .filter(n => !isNaN(n));
                
            await applyFilter({
                type: 'include',
                numbers: numbers
            });
        } catch (error) {
            console.error('Include filter error:', error);
        }
    });

    // Exclude filter
    $('.btn-run[data-filter="exclude"]').click(async function() {
        try {
            const numbers = $('#mustExclude').val()
                .split(',')
                .map(n => parseInt(n.trim()))
                .filter(n => !isNaN(n));
                
            await applyFilter({
                type: 'exclude',
                numbers: numbers
            });
        } catch (error) {
            console.error('Exclude filter error:', error);
        }
    });

    // Random filter
    $('.btn-run[data-filter="random"]').click(async function() {
        try {
            await applyFilter({
                type: 'random',
                count: parseInt($('#randomCount').val())
            });
        } catch (error) {
            console.error('Random filter error:', error);
        }
    });

    // Skip buttons
    $('.btn-skip').click(function() {
        $(this).closest('.filter-row').addClass('filter-skipped');
    });
});
