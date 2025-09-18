// Main JavaScript for DDT Management System

$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Confirm delete actions
    $('.btn-outline-danger[href*="delete"]').click(function(e) {
        if (!confirm('Sei sicuro di voler eliminare questo elemento?')) {
            e.preventDefault();
        }
    });
    
    // Form validation
    $('#ddt-form').on('submit', function(e) {
        var isValid = true;
        var errorMessages = [];
        
        // Check required fields
        $('input[required], select[required], textarea[required]').each(function() {
            if (!$(this).val()) {
                isValid = false;
                $(this).addClass('is-invalid');
                errorMessages.push('Il campo "' + $(this).prev('label').text() + '" è obbligatorio');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        // Check if at least one riga is present
        if ($('.riga-form').length === 0) {
            isValid = false;
            errorMessages.push('È necessario aggiungere almeno un articolo');
        }
        
        if (!isValid) {
            e.preventDefault();
            showAlert('error', 'Errore di validazione', errorMessages.join('<br>'));
        }
    });
    
    // Real-time form validation
    $('input, select, textarea').on('blur', function() {
        if ($(this).prop('required') && !$(this).val()) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Auto-format CAP field
    $('#id_cap').on('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
        if (this.value.length > 5) {
            this.value = this.value.slice(0, 5);
        }
    });
    
    // Auto-format P.IVA field
    $('#id_piva').on('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
        if (this.value.length > 11) {
            this.value = this.value.slice(0, 11);
        }
    });
    
    // Auto-format CF field
    $('#id_cf').on('input', function() {
        this.value = this.value.toUpperCase();
        this.value = this.value.replace(/[^A-Z0-9]/g, '');
        if (this.value.length > 16) {
            this.value = this.value.slice(0, 16);
        }
    });
    
    // Auto-format Provincia field
    $('#id_provincia').on('input', function() {
        this.value = this.value.toUpperCase();
        this.value = this.value.replace(/[^A-Z]/g, '');
        if (this.value.length > 2) {
            this.value = this.value.slice(0, 2);
        }
    });
    
    // Auto-format Targa field
    $('#id_targa').on('input', function() {
        this.value = this.value.toUpperCase();
        this.value = this.value.replace(/[^A-Z0-9]/g, '');
    });
    
    // Search functionality
    $('#search-input').on('keyup', function() {
        var searchTerm = $(this).val().toLowerCase();
        $('.table tbody tr').each(function() {
            var rowText = $(this).text().toLowerCase();
            if (rowText.indexOf(searchTerm) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
    
    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });
    
    // Loading states for buttons
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        submitBtn.prop('disabled', true);
        submitBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Salvataggio...');
    });
    
    // Auto-save functionality (if enabled)
    if (typeof autoSaveEnabled !== 'undefined' && autoSaveEnabled) {
        setInterval(function() {
            autoSaveForm();
        }, 30000); // Auto-save every 30 seconds
    }
});

// Utility functions
function showAlert(type, title, message) {
    var alertClass = 'alert-' + type;
    var iconClass = type === 'success' ? 'fa-check-circle' : 
                   type === 'error' ? 'fa-exclamation-circle' : 
                   type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas ${iconClass} me-2"></i>
            <strong>${title}</strong><br>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container-fluid').prepend(alertHtml);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('it-IT');
}

function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePIVA(piva) {
    return /^\d{11}$/.test(piva);
}

function validateCF(cf) {
    return /^[A-Z0-9]{16}$/.test(cf);
}

function validateCAP(cap) {
    return /^\d{5}$/.test(cap);
}

function validateProvincia(provincia) {
    return /^[A-Z]{2}$/.test(provincia);
}

// Auto-save functionality
function autoSaveForm() {
    var formData = $('#ddt-form').serialize();
    
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: formData + '&auto_save=1',
        success: function(response) {
            if (response.success) {
                showAlert('success', 'Auto-salvataggio', 'Modifiche salvate automaticamente');
            }
        },
        error: function() {
            console.log('Auto-save failed');
        }
    });
}

// Export functions
function exportToPDF() {
    window.open(window.location.href + '?export=pdf', '_blank');
}

function exportToExcel() {
    window.open(window.location.href + '?export=excel', '_blank');
}

// Print functionality
function printPage() {
    window.print();
}

// Keyboard shortcuts
$(document).keydown(function(e) {
    // Ctrl+S to save
    if (e.ctrlKey && e.which === 83) {
        e.preventDefault();
        $('#ddt-form').submit();
    }
    
    // Ctrl+N for new DDT
    if (e.ctrlKey && e.which === 78) {
        e.preventDefault();
        window.location.href = '/ddt/create/';
    }
    
    // Ctrl+F for search
    if (e.ctrlKey && e.which === 70) {
        e.preventDefault();
        $('#search-input').focus();
    }
    
    // Escape to close modals
    if (e.which === 27) {
        $('.modal').modal('hide');
    }
});

// Responsive table handling
function makeTableResponsive() {
    $('.table-responsive').each(function() {
        var table = $(this).find('table');
        var wrapper = $(this);
        
        if (table.width() > wrapper.width()) {
            wrapper.addClass('table-scroll');
        }
    });
}

$(window).resize(function() {
    makeTableResponsive();
});

// Initialize on page load
$(document).ready(function() {
    makeTableResponsive();
});

// Dark mode toggle (if implemented)
function toggleDarkMode() {
    $('body').toggleClass('dark-mode');
    localStorage.setItem('darkMode', $('body').hasClass('dark-mode'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    $('body').addClass('dark-mode');
}

// Form dirty state tracking
var formDirty = false;

$('input, select, textarea').on('change', function() {
    formDirty = true;
});

$(window).on('beforeunload', function() {
    if (formDirty) {
        return 'Hai modifiche non salvate. Sei sicuro di voler lasciare la pagina?';
    }
});

$('form').on('submit', function() {
    formDirty = false;
});

// Notification system
function showNotification(message, type = 'info') {
    var notification = $(`
        <div class="notification notification-${type}">
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle me-2"></i>
            ${message}
        </div>
    `);
    
    $('body').append(notification);
    
    setTimeout(function() {
        notification.fadeOut(function() {
            notification.remove();
        });
    }, 3000);
}

