$(document).ready(function() {
    var $prefatturaData = $('#prefatturaData');
    var prefatturaPk = $prefatturaData.data('pk');
    var filterUrl = $prefatturaData.data('filter-url');
    var editUrl = $prefatturaData.data('edit-url');

    // Funzione per aggiornare la tabella delle righe di listino
    function updateRigheListino() {
        $.ajax({
            url: filterUrl,
            data: $('#filtroForm').serialize(),
            dataType: 'json',
            success: function(data) {
                var tbody = $('#righeListinoTable tbody');
                tbody.empty();
                if (data.length === 0) {
                    tbody.append('<tr><td colspan="7" class="text-center">Nessuna riga di listino disponibile</td></tr>');
                } else {
                    $.each(data, function(i, item) {
                        tbody.append(
                            '<tr>' +
                            '<td>' + item.magazzino + '</td>' +
                            '<td>' + item.mezzo + '</td>' +
                            '<td>' + item.tipologia + '</td>' +
                            '<td>' + item.partenza + '</td>' +
                            '<td>' + item.arrivo + '</td>' +
                            '<td>' + item.costo + '</td>' +
                            '<td>' +
                                '<button type="button" class="personal-button add-riga" title="Aggiungi" data-id="' + item.id + '">' +
                                '<img src="/static/img/aggiungi.png" width="24px" height="24">' +
                                '</button>' +
                            '</td>' +
                            '</tr>'
                        );
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error("Errore nella richiesta AJAX:", status, error);
                $('#righeListinoTable tbody').html('<tr><td colspan="7" class="text-center">Errore nel caricamento delle righe di listino</td></tr>');
            }
        });
    }

    // Applica i filtri quando cambia il valore di qualsiasi select nel form
    $('#filtroForm select').change(function() {
        updateRigheListino();
    });

    // Event listener per il pulsante "Rimuovi Filtri"
    $('#rimuoviFiltri').click(function(e) {
        e.preventDefault();
        $('#filtroForm')[0].reset();
        updateRigheListino();
    });

    // Carica le righe iniziali al caricamento della pagina
    updateRigheListino();

    // Event listener per il pulsante "Aggiungi" su ogni riga di listino
    $(document).on('click', '.add-riga', function() {
        var id = $(this).data('id');
        $('#listino_id').val(id);
        $('#addRigaModal').modal('show');
    });

    // Gestione del submit del form per aggiungere una nuova riga
    $('#addRigaForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: editUrl,
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#addRigaModal').modal('hide');
                location.reload();  // Ricarica la pagina per mostrare la nuova riga
            },
            error: function(xhr, status, error) {
                console.error("Errore nell'aggiunta della riga:", status, error);
                alert("Si è verificato un errore nell'aggiunta della riga. Riprova.");
            }
        });
    });

    // Funzione per confermare l'eliminazione di una riga
    window.confirmDelete = function(id) {
        var isConfirmed = confirm("Sei sicuro di voler eliminare questa riga dalla prefattura?");
        if (isConfirmed) {
            document.getElementById("deleteForm_" + id).submit();
        }
    };

    // Validazione del form
    $('#addRigaForm').validate({
        rules: {
            quantita: {
                required: true,
                number: true,
                min: 1
            }
        },
        messages: {
            quantita: {
                required: "Inserisci una quantità",
                number: "Inserisci un numero valido",
                min: "La quantità deve essere maggiore di zero"
            }
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        }
    });

    // Reset del form modale quando viene chiuso
    $('#addRigaModal').on('hidden.bs.modal', function () {
        $('#addRigaForm')[0].reset();
        $('#addRigaForm').validate().resetForm();
    });
});