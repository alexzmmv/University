document.addEventListener('DOMContentLoaded', function() {
    initRangeSliders();
    
    const countryCheckboxes = document.querySelectorAll('.country-checkbox');
    if (countryCheckboxes.length > 0) {
        countryCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
            });
        });
        
        const applyFiltersBtn = document.getElementById('apply-filters');
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', function(e) {
                e.preventDefault();
                applyAdvancedFilters();
            });
        }
        
        const resetFiltersBtn = document.getElementById('reset-filters');
        if (resetFiltersBtn) {
            resetFiltersBtn.addEventListener('click', function(e) {
                e.preventDefault();
                resetAdvancedFilters();
            });
        }
    }
    
    const countrySelector = document.getElementById('country-selector');
    if (countrySelector && !document.querySelector('.advanced-filters')) {
        countrySelector.addEventListener('change', function() {
            loadDestinationsByCountry(this.value);
        });
    }

    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    if (searchInput && searchButton) {
        searchButton.addEventListener('click', function(e) {
            //e.preventDefault();
            applyAdvancedFilters();
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyAdvancedFilters();
            }
        });
    }

    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this destination?')) {
                e.preventDefault();
            }
        });
    });

    const destinationForm = document.getElementById('destination-form');
    if (destinationForm) {
        destinationForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            const countryInput = document.getElementById('country');
            const costInput = document.getElementById('cost_per_day');
            
            let isValid = true;
            
            if (nameInput.value.trim() === '') {
                showError(nameInput, 'Destination name is required');
                isValid = false;
            } else {
                clearError(nameInput);
            }
            
            if (countryInput.value.trim() === '') {
                showError(countryInput, 'Country name is required');
                isValid = false;
            } else {
                clearError(countryInput);
            }
            
            if (costInput.value.trim() === '' || isNaN(costInput.value) || parseFloat(costInput.value) <= 0) {
                showError(costInput, 'Cost must be a positive number');
                isValid = false;
            } else {
                clearError(costInput);
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});

function initRangeSliders() {
    const minCostInput = document.getElementById('min-cost');
    const maxCostInput = document.getElementById('max-cost');
    const minCostValue = document.getElementById('min-cost-value');
    const maxCostValue = document.getElementById('max-cost-value');
    
    if (minCostInput && maxCostInput) {
        minCostInput.addEventListener('input', function() {
            minCostValue.textContent = '$' + this.value;
            if (parseInt(this.value) > parseInt(maxCostInput.value)) {
                maxCostInput.value = this.value;
                maxCostValue.textContent = '$' + this.value;
            }
        });
        
        maxCostInput.addEventListener('input', function() {
            maxCostValue.textContent = '$' + this.value;
            if (parseInt(this.value) < parseInt(minCostInput.value)) {
                minCostInput.value = this.value;
                minCostValue.textContent = '$' + this.value;
            }
        });
    }
}

function applyAdvancedFilters() {
    const destinationsContainer = document.getElementById('destinations-container');
    const paginationContainer = document.getElementById('pagination-container');
    
    if (!destinationsContainer) return;
    
    destinationsContainer.innerHTML = '<div class="loading"></div>';
    
    const filters = collectFilterValues();
    
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page') || 1;
    
    let url;
    if (window.location.pathname.includes('/pages/')) {
        url = 'ajax_filters.php';
    } else {
        url = 'pages/ajax_filters.php';
    }
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filters: filters,
            page: page
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayDestinations(data.destinations, destinationsContainer);
        displayPagination(data.pagination, paginationContainer, filters);
        updateUrlParams(filters, page);
    })
    .catch(error => {
        destinationsContainer.innerHTML = `<p>Error loading destinations: ${error.message}</p>`;
    });
}

function collectFilterValues() {
    const filters = {};
    
    const selectedCountries = [];
    document.querySelectorAll('.country-checkbox:checked').forEach(checkbox => {
        selectedCountries.push(parseInt(checkbox.value));
    });
    
    if (selectedCountries.length > 0) {
        filters.countries = selectedCountries;
    }
    
    const securityLevelSelect = document.getElementById('security-level');
    if (securityLevelSelect && securityLevelSelect.value && parseInt(securityLevelSelect.value) > 0) {
        filters.security_level = parseInt(securityLevelSelect.value);
    }
    
    const minCost = document.getElementById('min-cost');
    const maxCost = document.getElementById('max-cost');
    
    if (minCost && minCost.value) {
        filters.min_cost = parseFloat(minCost.value);
    }
    
    if (maxCost && maxCost.value) {
        filters.max_cost = parseFloat(maxCost.value);
    }
    
    const searchInput = document.getElementById('search-input');
    if (searchInput && searchInput.value.trim() !== '') {
        filters.search = searchInput.value.trim();
    }
    
    return filters;
}

function resetAdvancedFilters() {
    document.querySelectorAll('.country-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    const securityLevelSelect = document.getElementById('security-level');
    if (securityLevelSelect) {
        securityLevelSelect.value = 0;
    }
    
    const minCost = document.getElementById('min-cost');
    const maxCost = document.getElementById('max-cost');
    const minCostValue = document.getElementById('min-cost-value');
    const maxCostValue = document.getElementById('max-cost-value');
    
    if (minCost && maxCost) {
        minCost.value = minCost.getAttribute('min') || 0;
        maxCost.value = maxCost.getAttribute('max') || 1000;
        
        if (minCostValue) minCostValue.textContent = '$' + minCost.value;
        if (maxCostValue) maxCostValue.textContent = '$' + maxCost.value;
    }
    
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.value = '';
    }
    
    applyAdvancedFilters();
}

function loadDestinationsByCountry(countryId) {
    const destinationsContainer = document.getElementById('destinations-container');
    const paginationContainer = document.getElementById('pagination-container');
    
    if (!destinationsContainer) return;
    
    destinationsContainer.innerHTML = '<div class="loading"></div>';
    
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page') || 1;
    
    let url;
    if (window.location.pathname.includes('/pages/')) {
        url = 'ajax_destinations.php?page=' + page;
    } else {
        url = 'pages/ajax_destinations.php?page=' + page;
    }
    
    if (countryId) {
        url += '&country_id=' + countryId;
    }
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayDestinations(data.destinations, destinationsContainer);
            displayPagination(data.pagination, paginationContainer, data.filters);
        })
        .catch(error => {
            destinationsContainer.innerHTML = `<p>Error loading destinations: ${error.message}</p>`;
        });
}

function displayDestinations(destinations, container) {
    if (!destinations || destinations.length === 0) {
        container.innerHTML = '<p class="no-results">No destinations found matching your criteria.</p>';
        return;
    }
    
    let html = '<div class="destinations-grid">';
    
    let linkPrefix = '';
    if (!window.location.pathname.includes('/pages/')) {
        linkPrefix = 'pages/';
    }
    
    destinations.forEach(destination => {
        let securityText = "Unknown";
        let securityClass = "";
        const securityLevel = destination.security_level ? parseInt(destination.security_level) : 1;
        
        switch(securityLevel) {
            case 1:
                securityText = "High";
                securityClass = "security-high";
                break;
            case 2:
                securityText = "Medium";
                securityClass = "security-medium";
                break;
            case 3:
                securityText = "Low";
                securityClass = "security-low";
                break;
        }
        
        html += `
            <div class="destination-card" onclick="window.location.href='${linkPrefix}view_destination.php?id=${destination.id}'">
                <h3>${destination.name}</h3>
                <div class="country">${destination.country_name}</div>
                <p>${destination.description.substring(0, 100)}${destination.description.length > 100 ? '...' : ''}</p>
                <div class="cost">$${parseFloat(destination.cost_per_day).toFixed(2)} per day</div>
                <div class="security-level">
                    Security Level: 
                    <span class="${securityClass}">${securityText}</span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function displayPagination(pagination, container, filters) {
    if (!container || !pagination || pagination.totalPages <= 1) {
        if (container) container.innerHTML = '';
        return;
    }
    
    let html = '<ul class="pagination">';
    
    if (pagination.currentPage > 1) {
        html += `<li><a href="#" onclick="navigateToPage(${pagination.currentPage - 1}, ${JSON.stringify(filters)}); return false;">Previous</a></li>`;
    }
    
    for (let i = 1; i <= pagination.totalPages; i++) {
        html += `<li class="${i === parseInt(pagination.currentPage) ? 'active' : ''}">
                    <a href="#" onclick="navigateToPage(${i}, ${JSON.stringify(filters)}); return false;">${i}</a>
                 </li>`;
    }
    
    if (pagination.currentPage < pagination.totalPages) {
        html += `<li><a href="#" onclick="navigateToPage(${parseInt(pagination.currentPage) + 1}, ${JSON.stringify(filters)}); return false;">Next</a></li>`;
    }
    
    html += '</ul>';
    container.innerHTML = html;
}

function navigateToPage(page, filters) {
    updateUrlParams(filters, page);
    
    if (document.querySelector('.advanced-filters')) {
        applyAdvancedFilters();
    } else {
        const countryId = filters && filters.countries && filters.countries.length > 0 ? 
            filters.countries[0] : null;
        loadDestinationsByCountry(countryId);
    }
}

function updateUrlParams(filters, page) {
    const url = new URL(window.location);
    
    url.searchParams.set('page', page);
    
    if (filters) {
        if (filters.countries && filters.countries.length > 0) {
            url.searchParams.set('countries', filters.countries.join(','));
        } else {
            url.searchParams.delete('countries');
        }
        
        if (filters.min_cost) {
            url.searchParams.set('min_cost', filters.min_cost);
        } else {
            url.searchParams.delete('min_cost');
        }
        
        if (filters.max_cost) {
            url.searchParams.set('max_cost', filters.max_cost);
        } else {
            url.searchParams.delete('max_cost');
        }
        
        if (filters.security_level) {
            url.searchParams.set('security_level', filters.security_level);
        } else {
            url.searchParams.delete('security_level');
        }
        
        if (filters.search) {
            url.searchParams.set('search', filters.search);
        } else {
            url.searchParams.delete('search');
        }
    }
    
    window.history.pushState({}, '', url);
}


function showError(input, message) {
    const formGroup = input.parentElement;
    const errorElement = formGroup.querySelector('.error-message') || document.createElement('div');
    
    errorElement.className = 'error-message';
    errorElement.style.color = 'var(--danger-color)';
    errorElement.style.fontSize = '0.8rem';
    errorElement.style.marginTop = '0.25rem';
    errorElement.textContent = message;
    
    if (!formGroup.querySelector('.error-message')) {
        formGroup.appendChild(errorElement);
    }
    
    input.style.borderColor = 'var(--danger-color)';
}

function clearError(input) {
    const formGroup = input.parentElement;
    const errorElement = formGroup.querySelector('.error-message');
    
    if (errorElement) {
        formGroup.removeChild(errorElement);
    }
    
    input.style.borderColor = '';
}