document.addEventListener('DOMContentLoaded', function () {
    initSearch({
        searchInputId: 'doctor-search',
        resultsContainerId: 'doctor-results',
        searchUrl: '/search/doctor/',
        onSelect: (doctorId) => {
            window.selectedDoctorId = doctorId;
        }
    });
});
