// Main JavaScript for Blood Bank Management System

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

    // Form validation
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

    // Blood type selection
    const bloodTypeSelects = document.querySelectorAll('.blood-type-select');
    bloodTypeSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedType = this.value;
            const bloodTypeInfo = document.getElementById('blood-type-info');
            if (bloodTypeInfo) {
                updateBloodTypeInfo(selectedType);
            }
        });
    });

    // Dynamic form fields
    const urgencySelect = document.querySelector('#urgency_level');
    if (urgencySelect) {
        urgencySelect.addEventListener('change', function() {
            updatePriceCalculation();
        });
    }

    const unitsInput = document.querySelector('#units_needed');
    if (unitsInput) {
        unitsInput.addEventListener('input', function() {
            updatePriceCalculation();
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Search functionality
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Filter functionality
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            applyFilters();
        });
    });

    // Date picker enhancement
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        input.setAttribute('min', today);
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = '(' + value;
                if (value.length > 4) {
                    value = value.substring(0, 4) + ') ' + value.substring(4);
                }
                if (value.length > 9) {
                    value = value.substring(0, 9) + '-' + value.substring(9);
                }
                if (value.length > 14) {
                    value = value.substring(0, 14);
                }
            }
            this.value = value;
        });
    });

    // Password strength indicator
    const passwordInput = document.querySelector('#id_password1');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                showFilePreview(file, this);
            }
        });
    });

    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
});

// Blood type information
function updateBloodTypeInfo(bloodType) {
    const bloodTypeInfo = document.getElementById('blood-type-info');
    const info = {
        'A+': 'Can donate to: A+, AB+ | Can receive from: A+, A-, O+, O-',
        'A-': 'Can donate to: A+, A-, AB+, AB- | Can receive from: A-, O-',
        'B+': 'Can donate to: B+, AB+ | Can receive from: B+, B-, O+, O-',
        'B-': 'Can donate to: B+, B-, AB+, AB- | Can receive from: B-, O-',
        'AB+': 'Can donate to: AB+ | Can receive from: All blood types',
        'AB-': 'Can donate to: AB+, AB- | Can receive from: A-, B-, AB-, O-',
        'O+': 'Can donate to: A+, B+, AB+, O+ | Can receive from: O+, O-',
        'O-': 'Can donate to: All blood types | Can receive from: O-'
    };
    
    if (bloodTypeInfo && info[bloodType]) {
        bloodTypeInfo.textContent = info[bloodType];
        bloodTypeInfo.style.display = 'block';
    }
}

// Price calculation
function updatePriceCalculation() {
    const urgencySelect = document.querySelector('#urgency_level');
    const unitsInput = document.querySelector('#units_needed');
    const priceDisplay = document.querySelector('#price-display');
    
    if (urgencySelect && unitsInput && priceDisplay) {
        const urgency = urgencySelect.value;
        const units = parseInt(unitsInput.value) || 0;
        
        const basePrice = 100.00;
        const urgencyMultiplier = {
            'normal': 1.0,
            'urgent': 1.5,
            'emergency': 2.0
        };
        
        const pricePerUnit = basePrice * urgencyMultiplier[urgency];
        const totalPrice = units * pricePerUnit;
        
        priceDisplay.textContent = `$${totalPrice.toFixed(2)}`;
    }
}

// Apply filters
function applyFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    const tableRows = document.querySelectorAll('tbody tr');
    
    tableRows.forEach(row => {
        let showRow = true;
        
        filterSelects.forEach(select => {
            const filterValue = select.value;
            const filterColumn = select.getAttribute('data-filter');
            
            if (filterValue && filterValue !== 'all') {
                const cellValue = row.querySelector(`[data-${filterColumn}]`).getAttribute(`data-${filterColumn}`);
                if (cellValue !== filterValue) {
                    showRow = false;
                }
            }
        });
        
        row.style.display = showRow ? '' : 'none';
    });
}

// Password strength checker
function checkPasswordStrength(password) {
    const strengthIndicator = document.querySelector('#password-strength');
    if (!strengthIndicator) return;
    
    let strength = 0;
    let feedback = '';
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    switch (strength) {
        case 0:
        case 1:
            feedback = 'Very Weak';
            strengthIndicator.className = 'text-danger';
            break;
        case 2:
            feedback = 'Weak';
            strengthIndicator.className = 'text-warning';
            break;
        case 3:
            feedback = 'Medium';
            strengthIndicator.className = 'text-info';
            break;
        case 4:
            feedback = 'Strong';
            strengthIndicator.className = 'text-success';
            break;
        case 5:
            feedback = 'Very Strong';
            strengthIndicator.className = 'text-success';
            break;
    }
    
    strengthIndicator.textContent = feedback;
}

// File preview
function showFilePreview(file, input) {
    const previewContainer = document.querySelector('#file-preview');
    if (!previewContainer) return;
    
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewContainer.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
        };
        reader.readAsDataURL(file);
    } else {
        previewContainer.innerHTML = `<p class="text-muted">Selected file: ${file.name}</p>`;
    }
}

// Initialize charts
function initializeCharts() {
    // Blood inventory chart
    const inventoryCtx = document.getElementById('inventory-chart');
    if (inventoryCtx) {
        new Chart(inventoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                datasets: [{
                    data: [12, 8, 15, 6, 4, 2, 20, 10],
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Donation trend chart
    const trendCtx = document.getElementById('trend-chart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Donations',
                    data: [65, 59, 80, 81, 56, 55],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Export functions for global use
window.BloodBankUtils = {
    formatDate,
    formatCurrency,
    updateBloodTypeInfo,
    updatePriceCalculation
}; 