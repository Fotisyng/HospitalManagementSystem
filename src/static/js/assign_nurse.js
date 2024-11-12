document.addEventListener('DOMContentLoaded', function () {
    const assignButton = document.getElementById('assign-button');

    assignButton.addEventListener('click', function () {
        const selectedSupervisorId = window.selectedSupervisorId;
        const selectedNurseIds = window.selectedNurseIds || [];

        if (selectedSupervisorId && selectedNurseIds.length > 0) {
            const payload = {
                supervisor_nurse_id: selectedSupervisorId,
                nurse_ids: selectedNurseIds,
            };

            fetch('/nurses/api/assign-supervision/', {
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
                        toastr.success(data.message);
                        setTimeout(() => {
                            window.location.href = `/nurses/nurses/${selectedSupervisorId}/`;
                        }, 1500);
                    } else if (data.error) {
                        toastr.error(data.error);
                    }
                })
                .catch(error => {
                    toastr.error('An error occurred while assigning nurses.');
                    console.error('Error assigning nurses:', error);
                });
        } else {
            toastr.warning('Please select a supervisor and at least one nurse to supervise.');
        }
    });
}, { once: true });
