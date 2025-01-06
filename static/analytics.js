// Enhanced Analytics Tracking for G-9WMYL5KKJK

// Filter Usage Events
function trackFilterUsage(filterType, filterValue) {
    gtag('event', 'filter_used', {
        'event_category': 'Filter Interaction',
        'event_label': filterType,
        'value': filterValue,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Combination Generation Events
function trackGeneratedCombinations(count) {
    gtag('event', 'combinations_generated', {
        'event_category': 'Generation',
        'event_label': 'Initial Combinations',
        'value': count,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Export Events
function trackExport() {
    gtag('event', 'export_results', {
        'event_category': 'Conversion',
        'event_label': 'CSV Export',
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Filter Results Events
function trackFilterResults(filterType, beforeCount, afterCount) {
    const reduction = beforeCount - afterCount;
    const reductionPercentage = ((reduction / beforeCount) * 100).toFixed(2);
    
    gtag('event', 'filter_results', {
        'event_category': 'Filter Performance',
        'event_label': filterType,
        'value': afterCount,
        'metric1': reduction,
        'metric2': reductionPercentage,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Error Tracking
function trackError(errorType, errorMessage) {
    gtag('event', 'error_occurred', {
        'event_category': 'Error',
        'event_label': errorType,
        'value': errorMessage,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// User Engagement Events
function trackEngagement(action) {
    gtag('event', 'user_engagement', {
        'event_category': 'Engagement',
        'event_label': action,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Page Load Performance
window.addEventListener('load', function() {
    if (window.performance) {
        const timeSincePageLoad = Math.round(performance.now());
        gtag('event', 'page_performance', {
            'event_category': 'Performance',
            'event_label': 'Page Load Time',
            'value': timeSincePageLoad,
            'metric1': timeSincePageLoad,
            'send_to': 'G-9WMYL5KKJK'
        });
    }
});

// Session Start
gtag('event', 'session_start', {
    'event_category': 'Session',
    'event_label': 'New Session',
    'send_to': 'G-9WMYL5KKJK'
});

// Filter Skip Events
function trackFilterSkip(filterType) {
    gtag('event', 'filter_skipped', {
        'event_category': 'Filter Interaction',
        'event_label': filterType,
        'send_to': 'G-9WMYL5KKJK'
    });
}

// Filter Clear Events
function trackFilterClear(filterType) {
    gtag('event', 'filter_cleared', {
        'event_category': 'Filter Interaction',
        'event_label': filterType,
        'send_to': 'G-9WMYL5KKJK'
    });
}
