<<<<<<< HEAD
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
        const response = await fetch('https://lottery-filters-1.onrender.com/filters', {
=======
let currentCombinations = [];

// Update the API endpoint and add progress tracking
const applyFilter = async (filterData) => {
    const startTime = performance.now();
    const filterId = filterData.activeFilter;
    
    // Show calculating status
    const filterRow = $(`.filter-row:has([data-filter="${filterId}"])`);
    const statusEl = filterRow.find('.filter-status');
    statusEl.html('Calculating...');

    try {
        const response = await fetch('https://lottery-filters.onrender.com/filters', {
>>>>>>> fb1564456748f3c28f316fd970f3762227d553d9
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

<<<<<<< HEAD
        // Calculate execution time
        const endTime = performance.now();
        const executionTime = ((endTime - startTime) / 1000).toFixed(2);
        
        // Update status to complete with time
        progressText.text('Complete');
        timeText.text(`${executionTime}s`);
=======
        // Calculate and show completion time
        const endTime = performance.now();
        const calculationTime = ((endTime - startTime) / 1000).toFixed(2);
        statusEl.html(`Complete (${calculationTime}s)`);
>>>>>>> fb1564456748f3c28f316fd970f3762227d553d9
        
        state.combinations = data.combinations;
        displayResults(data.combinations);

        return data;
    } catch (error) {
<<<<<<< HEAD
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
=======
        statusEl.html('Error');
        console.error('Filter error:', error);
        throw error;
    }
};
function showError(message, containerId = 'results') {
    const resultsDiv = document.getElementById(containerId);
    resultsDiv.innerHTML = `<div class="alert alert-danger" role="alert">${message}</div>`;
}

function showFilterProgress(filterId, show = true) {
    const progressElement = document.getElementById(`${filterId}Progress`);
    if (progressElement) {
        progressElement.classList.toggle('active', show);
    }
}

function updateStatPill(id, value) {
    const element = document.querySelector(`#${id} span`);
    if (element) {
        element.textContent = value ? value.toLocaleString() : '-';
    }
}

function generateInitialCombinations() {
    const drawSize = parseInt(document.getElementById('drawSize').value);
    const totalNumbers = parseInt(document.getElementById('totalNumbers').value);

    if (isNaN(drawSize) || isNaN(totalNumbers) || drawSize > totalNumbers) {
        showError('Please enter valid numbers. Draw size must be less than total numbers.');
        return;
    }

    showFilterProgress('base', true);
    document.getElementById('results').innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';

    fetch('/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'initial',
            drawSize: drawSize,
            totalNumbers: totalNumbers
        })
    })
    .then(response => response.json())
    .then(data => {
        showFilterProgress('base', false);
        currentCombinations = data.combinations;
        updateStatPill('stat-initial', data.combinations.length);
        document.getElementById('totalCombos').textContent = data.combinations.length.toLocaleString();
        displayResults(data.combinations);
    })
    .catch(error => {
        showFilterProgress('base', false);
        showError('Error generating combinations: ' + error.message);
    });
}

function applyFilter(filterType) {
    if (!currentCombinations || currentCombinations.length === 0) {
        showError('Please generate initial combinations first');
        return;
    }

    let filterValue;
    switch(filterType) {
        case 'odd':
            const oddMin = document.getElementById('oddMin').value;
            const oddMax = document.getElementById('oddMax').value;
            filterValue = { min: oddMin, max: oddMax };
            break;
        case 'distance':
            const distMin = document.getElementById('distanceMin').value;
            const distMax = document.getElementById('distanceMax').value;
            filterValue = { min: distMin, max: distMax };
            break;
        case 'sum':
            const sumMin = document.getElementById('sumMin').value;
            const sumMax = document.getElementById('sumMax').value;
            filterValue = { min: sumMin, max: sumMax };
            break;
        case 'include':
            filterValue = document.getElementById('mustInclude').value;
            break;
        case 'exclude':
            filterValue = document.getElementById('mustExclude').value;
            break;
        case 'random':
            filterValue = document.getElementById('randomCount').value;
            break;
    }

    showFilterProgress(filterType, true);

    fetch('/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: filterType,
            combinations: currentCombinations,
            value: filterValue
        })
    })
    .then(response => response.json())
    .then(data => {
        showFilterProgress(filterType, false);
        currentCombinations = data.combinations;
        updateStatPill(`stat-${filterType}`, data.combinations.length);
        document.getElementById('filteredCount').textContent = data.combinations.length.toLocaleString();
        displayResults(data.combinations);
    })
    .catch(error => {
        showFilterProgress(filterType, false);
        showError('Error applying filter: ' + error.message);
    });
}

function displayResults(combinations) {
    const resultsDiv = document.getElementById('results');
    if (combinations.length === 0) {
        resultsDiv.innerHTML = '<div class="alert alert-warning">No combinations found matching the filters</div>';
        return;
    }

    const resultsHtml = combinations.slice(0, 100).map(combo => 
        `<div class="combination">${combo.join(', ')}</div>`
    ).join('');
    
    resultsDiv.innerHTML = `
        <div class="mb-3">Showing first 100 of ${combinations.length.toLocaleString()} combinations</div>
        <div class="combinations-grid">${resultsHtml}</div>
    `;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Base calculation button
    document.querySelector('[data-filter="base"]').addEventListener('click', generateInitialCombinations);

    // Filter run buttons
    document.querySelectorAll('.btn-run').forEach(button => {
        button.addEventListener('click', function() {
            const filterType = this.getAttribute('data-filter');
            if (filterType !== 'base') {
                applyFilter(filterType);
            }
        });
    });

    // Skip buttons
    document.querySelectorAll('.btn-skip').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('.filter-row');
            row.classList.toggle('filter-skipped');
            row.querySelectorAll('input').forEach(input => {
                input.disabled = row.classList.contains('filter-skipped');
            });
        });
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Copy to clipboard functionality
    document.addEventListener('click', function(e) {
        if (e.target.matches('.combination')) {
            navigator.clipboard.writeText(e.target.textContent);
            const tooltip = document.getElementById('copyTooltip');
            tooltip.classList.add('show');
            setTimeout(() => tooltip.classList.remove('show'), 2000);
        }
    });
});
    
>>>>>>> fb1564456748f3c28f316fd970f3762227d553d9
