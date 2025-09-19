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
    
    // DDT Form specific functionality
    if ($('.ddt-form').length > 0) {
        initDDTForm();
    }
    
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

// DDT Form variables
var ddtForm = null;
var destinazioniUrl = null;
var sediMittenteUrl = null;
var autistiUrl = null;
var targheUrl = null;

// Gestione filtraggio sedi mittente
function loadSediMittente(mittenteId) {
    var sedeMittenteSelect = $('#id_sede_mittente');
    
    if (mittenteId) {
        $.ajax({
            url: sediMittenteUrl + mittenteId + '/',
            method: 'GET',
            success: function(data) {
                sedeMittenteSelect.empty();
                sedeMittenteSelect.append('<option value="">Seleziona sede mittente...</option>');
                
                data.forEach(function(sede) {
                    var optionText = sede.nome;
                    if (sede.codice_stalla) {
                        optionText += ' (' + sede.codice_stalla + ')';
                    }
                    if (sede.sede_legale) {
                        optionText += ' [Sede Legale]';
                    }
                    sedeMittenteSelect.append('<option value="' + sede.id + '">' + optionText + '</option>');
                });
            },
            error: function() {
                console.error('Errore nel caricamento delle sedi del mittente');
            }
        });
    } else {
        sedeMittenteSelect.empty();
        sedeMittenteSelect.append('<option value="">Seleziona prima un mittente</option>');
    }
}

// Gestione caricamento autisti e targhe
function loadAutistiTarghe(vettoreId) {
    var autistaSelect = $('#id_autista');
    var targaSelect = $('#id_targa_vettore');
    var targaSelect2 = $('#id_targa_vettore_2');
    
    if (vettoreId) {
        // Carica autisti
        $.ajax({
            url: autistiUrl + vettoreId + '/',
            method: 'GET',
            success: function(data) {
                autistaSelect.empty();
                autistaSelect.append('<option value="">Seleziona autista...</option>');
                
                data.forEach(function(autista) {
                    var optionText = autista.nome + ' ' + autista.cognome;
                    if (autista.patente) {
                        optionText += ' (' + autista.patente + ')';
                    }
                    autistaSelect.append('<option value="' + autista.id + '">' + optionText + '</option>');
                });
            },
            error: function() {
                console.error('Errore nel caricamento degli autisti');
            }
        });
        
        // Carica targhe per entrambi i campi
        $.ajax({
            url: targheUrl + vettoreId + '/',
            method: 'GET',
            success: function(data) {
                // Popola primo campo targa
                targaSelect.empty();
                targaSelect.append('<option value="">Seleziona targa 1...</option>');
                
                // Popola secondo campo targa
                targaSelect2.empty();
                targaSelect2.append('<option value="">Seleziona targa 2...</option>');
                
                data.forEach(function(targa) {
                    var optionText = targa.targa;
                    if (targa.tipo_veicolo) {
                        optionText += ' - ' + targa.tipo_veicolo;
                    }
                    if (targa.note && targa.note.trim() !== '') {
                        optionText += ' (' + targa.note + ')';
                    }
                    
                    // Aggiungi a entrambi i select
                    targaSelect.append('<option value="' + targa.id + '">' + optionText + '</option>');
                    targaSelect2.append('<option value="' + targa.id + '">' + optionText + '</option>');
                });
            },
            error: function() {
                console.error('Errore nel caricamento delle targhe');
            }
        });
    } else {
        autistaSelect.empty().append('<option value="">Seleziona prima un vettore</option>');
        targaSelect.empty().append('<option value="">Seleziona prima un vettore</option>');
        targaSelect2.empty().append('<option value="">Seleziona prima un vettore</option>');
    }
}

// Gestione dei valori esistenti per autista e targhe
function restoreAutistaTargaValues() {
    var selectedAutista = $('#autista_initial').val();
    var selectedTarga = $('#targa_vettore_initial').val();
    var selectedTarga2 = $('#targa_vettore_2_initial').val();
    
    console.log('Restoring autista/targhe:', { selectedAutista, selectedTarga, selectedTarga2 });
    
    if (selectedAutista) {
        $('#id_autista').val(selectedAutista);
        console.log('Set autista to:', selectedAutista);
    }
    if (selectedTarga) {
        $('#id_targa_vettore').val(selectedTarga);
        console.log('Set targa 1 to:', selectedTarga);
    }
    if (selectedTarga2) {
        $('#id_targa_vettore_2').val(selectedTarga2);
        console.log('Set targa 2 to:', selectedTarga2);
    }
}

// Gestione delle date per la modifica
function restoreDateValues() {
    var dataDocumento = $('#data_documento_initial').val();
    var dataRitiro = $('#data_ritiro_initial').val();
    
    console.log('Restoring dates:', { dataDocumento, dataRitiro });
    
    if (dataDocumento) {
        $('#id_data_documento').val(dataDocumento);
        console.log('Set data documento to:', dataDocumento);
    }
    if (dataRitiro) {
        $('#id_data_ritiro').val(dataRitiro);
        console.log('Set data ritiro to:', dataRitiro);
    }
}

// Gestione della sede mittente
function restoreSedeMittente() {
    var selectedSede = $('#sede_mittente_initial').val();
    console.log('Restoring sede mittente:', selectedSede);
    
    if (selectedSede) {
        $('#id_sede_mittente').val(selectedSede);
        console.log('Set sede mittente to:', selectedSede);
    }
}

// Inizializzazione dei valori esistenti
function initializeExistingValues() {
    console.log('Initializing existing values...');
    
    // Carica le sedi se c'è già un mittente selezionato
    var mittenteId = $('#id_mittente').val();
    console.log('Mittente ID:', mittenteId);
    if (mittenteId) {
        loadSediMittente(mittenteId);
        setTimeout(restoreSedeMittente, 500);
    }
    
    // Carica autisti e targhe se c'è già un vettore selezionato
    var vettoreId = $('#id_vettore').val();
    console.log('Vettore ID:', vettoreId);
    if (vettoreId) {
        loadAutistiTarghe(vettoreId);
        $('#autista-targa-fields').show();
        setTimeout(restoreAutistaTargaValues, 1000);
    }
    
    // Ripristina le date
    setTimeout(restoreDateValues, 100);
    
    // Ripristina la destinazione se esiste
    var destinazioneId = $('#id_destinazione_id').val();
    if (destinazioneId) {
        var destinatarioId = $('#id_destinatario').val();
        if (destinatarioId) {
            var url = destinazioniUrl.replace('0', destinatarioId);
            $.get(url, function(data) {
                var destinazioneSelect = $('#id_destinazione');
                destinazioneSelect.empty();
                destinazioneSelect.append('<option value="">Seleziona destinazione...</option>');
                $.each(data, function(index, destinazione) {
                    var optionText = destinazione.nome;
                    if (destinazione.codice_stalla) {
                        optionText += ' (' + destinazione.codice_stalla + ')';
                    }
                    var isSelected = destinazione.id == destinazioneId;
                    destinazioneSelect.append('<option value="' + destinazione.id + '" data-indirizzo="' + destinazione.indirizzo + '" data-codice-stalla="' + (destinazione.codice_stalla || '') + '"' + (isSelected ? ' selected' : '') + '">' + optionText + '</option>');
                });
                
                // Se c'è una selezione, aggiorna l'anteprima
                if (destinazioneId) {
                    var selectedOption = destinazioneSelect.find('option:selected');
                    var indirizzo = selectedOption.data('indirizzo');
                    var codiceStalla = selectedOption.data('codice-stalla');
                    var nome = selectedOption.text();
                    
                    if (indirizzo && nome !== 'Seleziona destinazione...') {
                        // Rimuovi il codice stalla tra parentesi dal nome se presente
                        var nomePulito = nome.replace(/\s*\([^)]*\)\s*$/, '').trim();
                        var luogoDestinazione = nomePulito;
                        
                        // Aggiungi sempre il codice stalla se presente
                        if (codiceStalla) {
                            luogoDestinazione += '\nCodice Stalla: ' + codiceStalla;
                        }
                        luogoDestinazione += '\n' + indirizzo;
                        $('#luogo-destinazione-preview').html(luogoDestinazione.replace(/\n/g, '<br>'));
                    }
                }
            }).fail(function() {
                console.error('Errore nel caricamento delle destinazioni');
            });
        }
    }
}

// DDT Form initialization
function initDDTForm() {
    console.log('Initializing DDT Form...');
    
    ddtForm = $('.ddt-form');
    destinazioniUrl = ddtForm.data('destinazioni-url');
    sediMittenteUrl = ddtForm.data('sedi-mittente-url');
    autistiUrl = ddtForm.data('autisti-url');
    targheUrl = ddtForm.data('targhe-url');
    
    console.log('URLs loaded:', { destinazioniUrl, sediMittenteUrl, autistiUrl, targheUrl });
    
    // Genera numero DDT automatico
    $('#generate-number').click(function() {
        var url = $('#generate-number').data('url') || '/api/next-ddt-number/';
        $.get(url, function(data) {
            $('#id_numero').val(data.numero);
        });
    });

    // Carica destinazioni quando cambia il destinatario
    $('#id_destinatario').change(function() {
        var destinatarioId = $(this).val();
        if (destinatarioId) {
            var url = destinazioniUrl.replace('0', destinatarioId);
            $.get(url, function(data) {
                var destinazioneSelect = $('#id_destinazione');
                destinazioneSelect.empty();
                destinazioneSelect.append('<option value="">Seleziona destinazione...</option>');
                $.each(data, function(index, destinazione) {
                    var optionText = destinazione.nome;
                    if (destinazione.codice_stalla) {
                        optionText += ' (' + destinazione.codice_stalla + ')';
                    }
                    destinazioneSelect.append('<option value="' + destinazione.id + '" data-indirizzo="' + destinazione.indirizzo + '" data-codice-stalla="' + (destinazione.codice_stalla || '') + '">' + optionText + '</option>');
                });
                
                // Se c'è un errore di validazione, mantieni la selezione precedente
                var selectedValue = destinazioneSelect.data('selected-value');
                if (selectedValue) {
                    destinazioneSelect.val(selectedValue);
                }
            });
        } else {
            $('#id_destinazione').empty().append('<option value="">Seleziona destinazione...</option>');
            $('#id_luogo_destinazione').val('');
        }
    });
    
    // Mostra anteprima luogo destinazione quando cambia la destinazione
    $('#id_destinazione').change(function() {
        var selectedOption = $(this).find('option:selected');
        var indirizzo = selectedOption.data('indirizzo');
        var codiceStalla = selectedOption.data('codice-stalla');
        var nome = selectedOption.text();
        var selectedValue = $(this).val();
        
        // Salva la selezione per il ripristino in caso di errore
        $(this).data('selected-value', selectedValue);
        
        // Popola il campo nascosto destinazione_id
        $('#id_destinazione_id').val(selectedValue);
        
        if (indirizzo && nome !== 'Seleziona destinazione...') {
            // Rimuovi il codice stalla tra parentesi dal nome se presente
            var nomePulito = nome.replace(/\s*\([^)]*\)\s*$/, '').trim();
            var luogoDestinazione = nomePulito;
            
            // Aggiungi sempre il codice stalla se presente
            if (codiceStalla) {
                luogoDestinazione += '\nCodice Stalla: ' + codiceStalla;
            }
            luogoDestinazione += '\n' + indirizzo;
            
            // Mostra anteprima
            $('#luogo-destinazione-preview').html(luogoDestinazione.replace(/\n/g, '<br>'));
            
            // Popola il campo nascosto per il salvataggio
            $('#id_luogo_destinazione').val(luogoDestinazione);
        } else {
            $('#luogo-destinazione-preview').html('<em class="text-muted">Seleziona una destinazione per vedere l\'anteprima...</em>');
            $('#id_luogo_destinazione').val('');
            $('#id_destinazione_id').val('');
        }
    });

    // Gestione aggiunta/rimozione righe
    $('#add-riga').click(function() {
        var formCount = parseInt($('#id_form-TOTAL_FORMS').val());
        var templateForm = $('.riga-form:first');
        
        if (templateForm.length === 0) {
            alert('Errore: Template form non trovato');
            return;
        }
        
        var newForm = templateForm.clone();
        
        // Aggiorna gli indici
        newForm.find('input, select').each(function() {
            var name = $(this).attr('name');
            if (name) {
                name = name.replace(/form-\d+/, 'form-' + formCount);
                $(this).attr('name', name);
            }
            
            var id = $(this).attr('id');
            if (id) {
                id = id.replace(/id_form-\d+/, 'id_form-' + formCount);
                $(this).attr('id', id);
            }
        });
        
        // Pulisci i valori
        newForm.find('input[type="text"], input[type="number"], select').val('');
        newForm.find('input[type="checkbox"]').prop('checked', false);
        
        // Aggiungi pulsante elimina
        newForm.find('.delete-row').remove();
        newForm.find('.col-md-1:last').append('<button type="button" class="btn btn-sm btn-outline-danger delete-row" title="Elimina riga">Elimina</button>');
        
        // Aggiungi al container
        $('#righe-container').append(newForm);
        
        // Aggiorna il contatore
        $('#id_form-TOTAL_FORMS').val(formCount + 1);
    });

    // Gestione eliminazione righe
    $(document).on('click', '.delete-row', function() {
        $(this).closest('.riga-form').remove();
        var formCount = parseInt($('#id_form-TOTAL_FORMS').val());
        $('#id_form-TOTAL_FORMS').val(formCount - 1);
    });
    
    // Gestione toggle tra righe articoli e note centrali
    $('input[name="tipo_articoli"]').change(function() {
        var tipo = $(this).val();
        
        if (tipo === 'righe') {
            $('#righe-container').show();
            $('#add-riga-container').show();
            $('#note-centrali-container').hide();
        } else if (tipo === 'note') {
            $('#righe-container').hide();
            $('#add-riga-container').hide();
            $('#note-centrali-container').show();
        }
    });
    
    // Gestione toggle per note centrali (checkbox)
    $('#tipo_note').change(function() {
        if ($(this).is(':checked')) {
            $('#righe-container').hide();
            $('#add-riga-container').hide();
            $('#note-centrali-container').show();
        } else {
            $('#righe-container').show();
            $('#add-riga-container').show();
            $('#note-centrali-container').hide();
        }
    });

    // Gestione trasporto a mezzo
    function updateTrasportoFields() {
        const trasportoMezzo = $('input[name="trasporto_mezzo"]:checked').val();
        const vettoreField = $('#vettore-field');
        const autistaTargaFields = $('#autista-targa-fields');
        
        console.log('updateTrasportoFields called, trasportoMezzo:', trasportoMezzo);
        
        if (trasportoMezzo === 'vettore') {
            vettoreField.show();
            vettoreField.find('select').prop('required', true);
            // Mostra sempre i campi autista e targa quando trasporto_mezzo è 'vettore'
            autistaTargaFields.show();
            console.log('Showing autista-targa-fields for vettore');
        } else {
            vettoreField.hide();
            vettoreField.find('select').prop('required', false);
            autistaTargaFields.hide();
            console.log('Hiding autista-targa-fields for non-vettore');
        }
    }

    // Inizializza i campi al caricamento
    updateTrasportoFields();

    // Aggiorna i campi quando cambia la selezione
    $('input[name="trasporto_mezzo"]').change(function() {
        updateTrasportoFields();
    });
    
    // Inizializza il toggle in base al contenuto esistente
    if ($('#id_note_centrali').val().trim() !== '') {
        $('#tipo_note').prop('checked', true).trigger('change');
    }
    
    // Inizializza l'anteprima del luogo destinazione se già presente
    if ($('#id_luogo_destinazione').val().trim() !== '') {
        var luogoDestinazione = $('#id_luogo_destinazione').val();
        $('#luogo-destinazione-preview').html(luogoDestinazione.replace(/\n/g, '<br>'));
    }
    
    // Inizializza i valori esistenti
    initializeExistingValues();
}

