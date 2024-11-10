document.addEventListener('DOMContentLoaded', function () {
    const assignButton = document.getElementById('assign-button');

    assignButton.addEventListener('click', function () {
        const selectedDoctorId = window.selectedDoctorId;
        const selectedPatientIds = window.selectedPatientIds || [];

        if (selectedDoctorId && selectedPatientIds.length > 0) {
            const payload = {
                doctor_id: selectedDoctorId,
                patient_ids: selectedPatientIds,
            };

            fetch('/doctors/api/assign-patients/', {
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
                        // Show success toastr message
                        toastr.success(data.message);

                        // Redirect to the doctor detail page after a short delay
                        setTimeout(() => {
                            window.location.href = `/doctors/doctors/${selectedDoctorId}/`;
                        }, 1500);  // Optional delay for user to see the toastr message
                    } else if (data.error) {
                        toastr.error(data.error);
                    }
                })
                .catch(error => {
                    toastr.error('An error occurred while assigning patients.');
                    console.error('Error assigning patients:', error);
                });
        } else {
            toastr.warning('Please select a doctor and at least one patient.');
        }
    });
}, { once: true });
