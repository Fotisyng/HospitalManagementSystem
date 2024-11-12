document.addEventListener('DOMContentLoaded', function () {
    initSearch({
        searchInputId: 'nurse-search',
        resultsContainerId: 'nurse-results',
        searchUrl: '/search/nurse/',
        onSelect: (nurseId) => {
            if (!window.selectedNurseIds) {
                window.selectedNurseIds = [];
            }
            window.selectedNurseIds.push(nurseId);
        }
    });
});
