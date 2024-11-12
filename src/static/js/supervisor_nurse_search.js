document.addEventListener('DOMContentLoaded', function () {
    initSearch({
        searchInputId: 'supervisor-nurse-search',
        resultsContainerId: 'supervisor-nurse-results',
        searchUrl: '/search/supervisor-nurse/',
        onSelect: (nurseId) => {
            window.selectedSupervisorId = nurseId;
        }
    });
});
