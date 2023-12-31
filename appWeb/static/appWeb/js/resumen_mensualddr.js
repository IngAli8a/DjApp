$(document).ready(function() {
    // Inicializa el DataTable
    var table = $('#datatable-resumenmensual').DataTable();

    // Función para descargar los datos en formato XLS
    $('#btnDescargar').on('click', function() {
        tableToExcel('datatable-resumenmensual', 'Datos');
    });

    // Función para exportar la tabla a Excel
    var tableToExcel = (function() {
        var uri = 'data:application/vnd.ms-excel;base64,';
        var template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>';
        var base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))); };
        var format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }); };

        return function(table, name) {
            if (!table.nodeType) table = document.getElementById(table);
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML };
            var link = document.createElement("a");
            link.download = "Resumen Mensual Demanda Diaria.xls";
            window.location.href = uri + base64(format(template, ctx));
            link.click();
        };
    })();
});
