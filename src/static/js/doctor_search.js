// doctor_search.js

document.addEventListener('DOMContentLoaded', function () {
    const doctorSearchInput = document.getElementById('doctor-search');
    const doctorResultsContainer = document.getElementById('doctor-results');
    let selectedDoctorId = null;

    // Select doctor from the search results
    doctorSearchInput.addEventListener('input', function () {
        const query = doctorSearchInput.value;

        if (query.length > 0) {
            fetch(`/search/doctor/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    doctorResultsContainer.innerHTML = '';
                    if (data.results.length > 0) {
                        data.results.forEach(doctor => {
                            const resultItem = document.createElement('div');
                            resultItem.classList.add('result-item');
                            resultItem.textContent = doctor.name;
                            resultItem.addEventListener('click', () => {
                                doctorSearchInput.value = doctor.name;
                                selectedDoctorId = doctor.id; // Set the selected doctor ID
                                doctorResultsContainer.style.display = 'none';

                                // Optionally, store the selected doctor ID in a global variable
                                window.selectedDoctorId = selectedDoctorId;
                            });
                            doctorResultsContainer.appendChild(resultItem);
                        });
                        doctorResultsContainer.style.display = 'block';
                    } else {
                        doctorResultsContainer.style.display = 'none';
                    }
                })
                .catch(error => console.error('Error fetching doctors:', error));
        } else {
            doctorResultsContainer.style.display = 'none';
        }
    });
});
