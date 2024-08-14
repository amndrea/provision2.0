$(document).ready(function() {
    console.log("ESEGUE LO SCRIPT PREFATTURA.JS");
    $('#magazzino, #mezzo, #tipologia, #partenza, #arrivo').on('change', function() {
        var id = $(this).attr('id');
        var value = $(this).val();
        switch(id) {
            case 'magazzino':
                magazzinoSelezionato(value);
                break;
            case 'mezzo':
                mezzoSelezionato(value);
                break;
            case 'tipologia':
                tipologiaSelezionata(value);
                break;
            case 'partenza':
                partenzaSelezionata(value);
                break;
            case 'arrivo':
                arrivoSelezionato(value);
                break;
        }
    });

    // Chiamata iniziale per popolare la tabella e le select
    filterRigheListino();
});

// Funzione per il reset del form dei filtri
function resetFormFiltri() {
    console.log("Resetto il form dei filtri");
    document.getElementById("filtroForm").reset();
    document.getElementById("magazzino_selezionato").value = "";
    document.getElementById("mezzo_selezionato").value = "";
    document.getElementById("tipologia_selezionato").value = "";
    document.getElementById("partenza_selezionato").value = "";
    document.getElementById("arrivo_selezionato").value = "";
    resetTabella();
    filterRigheListino();
}

// Funzione per il reset della tabella 
function resetTabella() {
    console.log("Resetto la tabella delle possibili righe da inserire");
    var tableBody = document.querySelector('#righeListinoTable tbody');
    tableBody.innerHTML = '';
}

// Funzioni per gestire la selezione di ciascun filtro
function magazzinoSelezionato(value) {
    document.getElementById("magazzino_selezionato").value = value;
    filterRigheListino();
}

function mezzoSelezionato(value) {
    document.getElementById("mezzo_selezionato").value = value;
    filterRigheListino();
}

function tipologiaSelezionata(value) {
    document.getElementById("tipologia_selezionato").value = value;
    filterRigheListino();
}

function partenzaSelezionata(value) {
    document.getElementById("partenza_selezionato").value = value;
    filterRigheListino();
}

function arrivoSelezionato(value) {
    document.getElementById("arrivo_selezionato").value = value;
    filterRigheListino();
}

function filterRigheListino() {
    var pk = document.getElementById("prefattura_pk").value;
    var magazzino = document.getElementById("magazzino_selezionato").value;
    var mezzo = document.getElementById("mezzo_selezionato").value;
    var tipologia = document.getElementById("tipologia_selezionato").value;
    var partenza = document.getElementById("partenza_selezionato").value;
    var arrivo = document.getElementById("arrivo_selezionato").value;

    console.log("Chiamata AJAX con parametri:", {pk, magazzino, mezzo, tipologia, partenza, arrivo});

    $.ajax({
        url: window.filterRigheListinoUrl,
        type: 'GET',
        data: {pk, magazzino, mezzo, tipologia, partenza, arrivo},
        dataType: 'json',
        success: function(response) {
            console.log("Dati ricevuti:", response);
            resetTabella();

            // Popola la tabella con i nuovi dati
            $.each(response.righe, function(index, item) {
                var newRow = '<tr>' +
                    '<td>' + item.magazzino + '</td>' +
                    '<td>' + item.mezzo + '</td>' +
                    '<td>' + item.tipologia + '</td>' +
                    '<td>' + item.partenza + '</td>' +
                    '<td>' + item.arrivo + '</td>' +
                    '<td>' + item.costo + '</td>' +
                    '<td>' +
                        '<button type="button" class="personal-button" title="Aggiungi" ' +
                        'onclick="aggiungiRiga(' + item.id + ')">' +
                        '<img src="/static/img/aggiungi.png" width="24px" height="24">' +
                        '</button>' +
                    '</td>' +
                '</tr>';
                $('#righeListinoTable tbody').append(newRow);
            });

            // Funzione per popolare le select
            function populateSelect(selectId, data, valueKey, textKey) {
                var select = $('#' + selectId);
                var currentValue = select.val();
                select.empty();
                select.append($('<option>', {
                    value: '',
                    text: 'Tutti'
                }));
                $.each(data, function(index, item) {
                    select.append($('<option>', {
                        value: item[valueKey],
                        text: item[textKey]
                    }));
                });
                select.val(currentValue);
            }

            // Popola tutte le select
            populateSelect('magazzino', response.magazzini, 'magazzino__id', 'magazzino__magazzino_lettera');
            populateSelect('mezzo', response.mezzi, 'mezzo__id', 'mezzo__mezzo_nome');
            populateSelect('tipologia', response.tipologie, 'tipologia__id', 'tipologia__tipologia_nome');
            populateSelect('partenza', response.partenze, 'partenza__id', 'partenza__zona_nome');
            populateSelect('arrivo', response.arrivi, 'arrivo__id', 'arrivo__zona_nome');
        },
        error: function(xhr, status, error) {
            console.error("Errore nella richiesta AJAX:", status, error);
            alert("Si è verificato un errore nel caricamento dei dati. Riprova.");
        }
    });
}

function aggiungiRiga(id) {
    document.getElementById('listino_id').value = id;
    var modal = document.getElementById('addRigaModal');
    if (modal && typeof bootstrap !== 'undefined') {
        var bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    } else {
        console.error('Modal o Bootstrap non trovati');
    }
}

function confirmDelete(id) {
    if (confirm("Sei sicuro di voler eliminare questa riga?")) {
        document.getElementById("deleteForm_" + id).submit();
    }
}