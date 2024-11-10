function initSearch({ searchInputId, resultsContainerId, searchUrl, onSelect }) {
    const searchInput = document.getElementById(searchInputId);
    const resultsContainer = document.getElementById(resultsContainerId);

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;

        if (query.length > 0) {
            fetch(`${searchUrl}?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    if (data.results && data.results.length > 0) {
                        data.results.forEach(item => {
                            const resultItem = document.createElement('div');
                            resultItem.classList.add('result-item');
                            resultItem.textContent = item.name;

                            resultItem.addEventListener('click', () => {
                                searchInput.value = item.name;
                                onSelect(item.id);
                                resultsContainer.style.display = 'none';
                            });

                            resultsContainer.appendChild(resultItem);
                        });
                        resultsContainer.style.display = 'block';
                    } else {
                        resultsContainer.style.display = 'none';
                    }
                })
                .catch(error => console.error('Error fetching search results:', error));
        } else {
            resultsContainer.style.display = 'none';
        }
    });
}
