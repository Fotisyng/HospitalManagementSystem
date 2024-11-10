document.addEventListener('DOMContentLoaded', function () {
    // Initialize `window.selectedPatientIds` as an empty array if it doesn't exist
    window.selectedPatientIds = window.selectedPatientIds || [];

    initSearch({
        searchInputId: 'patient-search',
        resultsContainerId: 'patient-results',
        searchUrl: '/search/patient/',
        onSelect: (patientId) => {
            // Only add unique patient IDs to avoid duplicates
            if (!window.selectedPatientIds.includes(patientId)) {
                window.selectedPatientIds.push(patientId);
            }
        }
    });
});
