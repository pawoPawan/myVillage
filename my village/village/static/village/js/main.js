// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Handle contribution form
    const contributionForm = document.getElementById('contribution-form');
    if (contributionForm) {
        contributionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const amount = document.getElementById('contribution-amount').value;
            const description = document.getElementById('contribution-description').value;
            
            // Here you would typically send this data to your backend
            console.log('Contribution submitted:', { amount, description });
            
            // Show success message
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success alert-dismissible fade show';
            alertDiv.innerHTML = `
                Thank you for your contribution of ₹${amount}!
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            contributionForm.parentNode.insertBefore(alertDiv, contributionForm);
            
            // Reset form
            contributionForm.reset();
        });
    }

    // Handle relationship form
    const relationshipForm = document.getElementById('relationship-form');
    if (relationshipForm) {
        relationshipForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const relatedUser = document.getElementById('related-user').value;
            const relationshipType = document.getElementById('relationship-type').value;
            const description = document.getElementById('relationship-description').value;
            
            // Here you would typically send this data to your backend
            console.log('Relationship added:', { relatedUser, relationshipType, description });
            
            // Show success message
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success alert-dismissible fade show';
            alertDiv.innerHTML = `
                Relationship with ${relatedUser} has been added!
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            relationshipForm.parentNode.insertBefore(alertDiv, relationshipForm);
            
            // Reset form
            relationshipForm.reset();
        });
    }

    // Handle event filtering
    const eventFilter = document.getElementById('event-filter');
    if (eventFilter) {
        eventFilter.addEventListener('change', function() {
            const selectedType = this.value;
            const eventCards = document.querySelectorAll('.event-card');
            
            eventCards.forEach(card => {
                const eventType = card.getAttribute('data-event-type');
                if (selectedType === 'all' || eventType === selectedType) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Handle service filtering
    const serviceFilter = document.getElementById('service-filter');
    if (serviceFilter) {
        serviceFilter.addEventListener('change', function() {
            const selectedType = this.value;
            const serviceCards = document.querySelectorAll('.service-card');
            
            serviceCards.forEach(card => {
                const serviceType = card.getAttribute('data-service-type');
                if (selectedType === 'all' || serviceType === selectedType) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Handle village search
    const villageSearch = document.getElementById('village-search');
    if (villageSearch) {
        villageSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const villageCards = document.querySelectorAll('.village-card');
            
            villageCards.forEach(card => {
                const villageName = card.querySelector('.village-name').textContent.toLowerCase();
                const villageDistrict = card.querySelector('.village-district').textContent.toLowerCase();
                const villageState = card.querySelector('.village-state').textContent.toLowerCase();
                
                if (villageName.includes(searchTerm) || 
                    villageDistrict.includes(searchTerm) || 
                    villageState.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}); 