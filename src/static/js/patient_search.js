// patient_search.js

document.addEventListener('DOMContentLoaded', function () {
    const patientSearchInput = document.getElementById('patient-search');
    const patientResultsContainer = document.getElementById('patient-results');
    let selectedPatientIds = [];

    // Select patients from the search results
    patientSearchInput.addEventListener('input', function () {
        const query = patientSearchInput.value;

        if (query.length > 0) {
            fetch(`/search/patient/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    patientResultsContainer.innerHTML = '';
                    if (data.results.length > 0) {
                        data.results.forEach(patient => {
                            const resultItem = document.createElement('div');
                            resultItem.classList.add('result-item');
                            resultItem.textContent = patient.name;

                            resultItem.addEventListener('click', () => {
                                // Update the search input with the selected patient's name
                                patientSearchInput.value = patient.name;

                                // Add selected patient ID to the list
                                selectedPatientIds.push(patient.id);

                                // Optionally, display the selected patient in the results
                                const selectedPatientDiv = document.createElement('div');
                                selectedPatientDiv.classList.add('selected-patient');
                                selectedPatientDiv.textContent = patient.name;
                                patientResultsContainer.appendChild(selectedPatientDiv);

                                // Hide the results container after selection
                                patientResultsContainer.style.display = 'none';

                                // Optionally, store the selected patient IDs in a global variable
                                window.selectedPatientIds = selectedPatientIds;
                            });

                            patientResultsContainer.appendChild(resultItem);
                        });
                        patientResultsContainer.style.display = 'block';
                    } else {
                        patientResultsContainer.style.display = 'none';
                    }
                })
                .catch(error => console.error('Error fetching patients:', error));
        } else {
            patientResultsContainer.style.display = 'none';
        }
    });
});
