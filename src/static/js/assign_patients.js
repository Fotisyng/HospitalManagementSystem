document.addEventListener('DOMContentLoaded', function () {
    const assignButton = document.getElementById('assign-button');

    // Handle assignment of selected patients to a doctor
    assignButton.addEventListener('click', function () {
        const selectedDoctorId = window.selectedDoctorId;
        const selectedPatientIds = window.selectedPatientIds || [];

        if (selectedDoctorId && selectedPatientIds.length > 0) {
            const payload = {
                doctor_id: selectedDoctorId,
                patient_ids: selectedPatientIds,
            };

            fetch('/doctors/api/assign-patients/', {  // New API endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(payload),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                        window.selectedPatientIds = []; // Clear selected patients after assignment
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('Error assigning patients:', error));
        } else {
            alert('Please select a doctor and at least one patient.');
        }
    });
}, { once: true });
