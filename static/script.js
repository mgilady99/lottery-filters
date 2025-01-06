// Global state
let currentCombinations = [];
let startTime = null;

function updateProgress(filterId, status, timeElapsed = null) {
    const progressText = $(`#${filterId} .filter-progress .progress-text`);
    const timeText = $(`#${filterId} .filter-progress .time-text`);
    
    progressText.text(status);
    if (timeElapsed !== null) {
        timeText.text(`(${timeElapsed.toFixed(2)}s)`);
    } else {
        timeText.text('');
    }
}

function updateFilterStats(filterId, totalResults) {
    const statsDiv = $(`#${filterId} .filter-stats`);
    if (!statsDiv.length) {
        const statsHtml = `
            <div class="filter-stats mt-2">
                <div class="alert alert-info">
                    Results: ${totalResults} combinations
                </div>
            </div>`;
        $(`#${filterId} .filter-content`).append(statsHtml);
    } else {
        statsDiv.find('.alert').text(`Results: ${totalResults} combinations`);
    }
}

async function applyFilter(type, data = {}) {
    const filterId = type === 'base' ? 'baseFilter' : `${type}Filter`;
    startTime = performance.now();
    
    try {
        updateProgress(filterId, 'Running...');
        
        const requestData = {
            type: type,
            previousCombinations: currentCombinations,
            ...data
        };

        const response = await fetch('/filters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();
        const endTime = performance.now();
        const timeElapsed = (endTime - startTime) / 1000;

        if (result.error) {
            updateProgress(filterId, 'Error', timeElapsed);
            alert(result.error);
            return;
        }

        currentCombinations = result.combinations;
        updateProgress(filterId, 'Complete', timeElapsed);
        updateFilterStats(filterId, currentCombinations.length);
        
        // Update results display
        displayResults(currentCombinations);

    } catch (error) {
        const endTime = performance.now();
        const timeElapsed = (endTime - startTime) / 1000;
        updateProgress(filterId, 'Error', timeElapsed);
        console.error('Error:', error);
        alert('An error occurred while applying the filter');
    }
}

function displayResults(combinations) {
    const resultsDiv = $('#results');
    if (combinations.length === 0) {
        resultsDiv.html('<div class="alert alert-warning">No combinations match the current filters</div>');
        return;
    }

    let html = '<div class="combinations-grid">';
    combinations.forEach((combo, index) => {
        html += `
            <div class="combination-card">
                <div class="combination-numbers">${combo.join(', ')}</div>
                <button class="btn btn-sm btn-outline-secondary copy-btn" data-combo="${combo.join(', ')}">
                    <i class="fas fa-copy"></i>
                </button>
            </div>`;
    });
    html += '</div>';
    resultsDiv.html(html);
}

$(document).ready(function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover'
        });
    });

    // Base Settings
    $('#baseFilter .btn-run').click(async function() {
        const totalNumbers = parseInt($('#totalNumbers').val());
        const drawSize = parseInt($('#drawSize').val());
        
        if (isNaN(totalNumbers) || isNaN(drawSize) || totalNumbers < drawSize) {
            alert('Please enter valid numbers. Total numbers must be greater than draw size.');
            return;
        }
        
        await applyFilter('base', {
            totalNumbers: totalNumbers,
            drawSize: drawSize
        });
    });

    // Odd Numbers Filter
    $('#oddFilter .btn-run').click(async function() {
        const minOdd = $('#oddMin').val() ? parseInt($('#oddMin').val()) : null;
        const maxOdd = $('#oddMax').val() ? parseInt($('#oddMax').val()) : null;
        
        await applyFilter('odd_even', {
            minOdd: minOdd,
            maxOdd: maxOdd
        });
    });

    // Distance Filter
    $('#distanceFilter .btn-run').click(async function() {
        const minDistance = $('#distanceMin').val() ? parseInt($('#distanceMin').val()) : null;
        const maxDistance = $('#distanceMax').val() ? parseInt($('#distanceMax').val()) : null;
        
        await applyFilter('distance', {
            minDistance: minDistance,
            maxDistance: maxDistance
        });
    });

    // Sum Filter
    $('#sumFilter .btn-run').click(async function() {
        const sumMin = $('#sumMin').val() ? parseInt($('#sumMin').val()) : null;
        const sumMax = $('#sumMax').val() ? parseInt($('#sumMax').val()) : null;
        
        await applyFilter('sum', {
            sumMin: sumMin,
            sumMax: sumMax
        });
    });

    // Must Include Filter
    $('#includeFilter .btn-run').click(async function() {
        const numbersStr = $('#mustInclude').val();
        const numbers = numbersStr ? numbersStr.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n)) : [];
        
        await applyFilter('include', {
            numbers: numbers
        });
    });

    // Must Exclude Filter
    $('#excludeFilter .btn-run').click(async function() {
        const numbersStr = $('#mustExclude').val();
        const numbers = numbersStr ? numbersStr.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n)) : [];
        
        await applyFilter('exclude', {
            numbers: numbers
        });
    });

    // Random Selection
    $('#randomFilter .btn-run').click(async function() {
        const count = parseInt($('#randomCount').val());
        
        if (isNaN(count) || count <= 0) {
            alert('Please enter a valid number of combinations to select');
            return;
        }
        
        await applyFilter('random', {
            count: count
        });
    });

    // Skip buttons
    $('.btn-skip').click(function() {
        const filterId = $(this).closest('.filter-row').find('.filter-content').attr('id');
        updateProgress(filterId, 'Skipped');
    });

    // Copy button functionality
    $(document).on('click', '.copy-btn', function() {
        const combo = $(this).data('combo');
        navigator.clipboard.writeText(combo);
        
        const tooltip = $('#copyTooltip');
        tooltip.addClass('show');
        setTimeout(() => tooltip.removeClass('show'), 2000);
    });
});
