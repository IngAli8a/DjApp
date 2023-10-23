$(document).ready(function () {
    // Variables para mantener el medicamento seleccionado
    var selectedMedicamento = null;

    $('#search-input').on('input', function () {
        // ... Código de búsqueda anterior ...

        // Agrega un evento click para seleccionar un medicamento
        $('#search-results li').on('click', function () {
            selectedMedicamento = $(this).text();
            $('#search-input').val(selectedMedicamento);

            // Limpia los campos de entrada
            $('#entregados-input').val('');
            $('#no-entregados-input').val('');
            $('#fecha-input').val('');

            // Agrega el medicamento seleccionado a la tabla
            $('#demanda-table tbody').html('<tr><td>' + selectedMedicamento + '</td><td><input type="number" id="entregados-input"></td><td><input type="number" id="no-entregados-input"></td><td><input type="date" id="fecha-input"></td><td><button id="guardar-btn">Guardar</button></td></tr>');
        });
    });

    // Manejar el evento de clic en el botón "Guardar"
    $(document).on('click', '#guardar-btn', function () {
        var entregados = $('#entregados-input').val();
        var noEntregados = $('#no-entregados-input').val();
        var fecha = $('#fecha-input').val();

        // Validación de campos
        if (!entregados || !noEntregados || !fecha) {
            alert('Por favor, complete todos los campos.');
            return;
        }

        // Realiza una solicitud AJAX para guardar los datos en el modelo demanda_diarias
        $.ajax({
            url: '/guardar-demanda/',
            method: 'POST',
            data: {
                'medicamento': selectedMedicamento,
                'entregados': entregados,
                'no_entregados': noEntregados,
                'fecha': fecha
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Datos guardados exitosamente.');
                    // Limpia la tabla y los campos de entrada
                    $('#demanda-table tbody').html('');
                    $('#search-input').val('');
                    selectedMedicamento = null;
                } else {
                    alert('Error al guardar los datos.');
                }
            }
        });
    });
});
