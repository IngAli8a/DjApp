let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [0, 5, 6] }
    ],
    pageLength: 4,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listdemandadiaria();

    dataTable = $("#datatable-demandadiaria").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listdemandadiaria = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/list_demandadiaria/");
        const data = await response.json();

        let content = ``;
        data.demanda.forEach((demanda_diaria_db, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${demanda_diaria_db.codigo_id}</td>
                    <td>${demanda_diaria_db.entregado}</td>
                    <td>${demanda_diaria_db.no_entregado}</td>
                    <td>${demanda_diaria_db.fecha} </td>
                    <td>${demanda_diaria_db.total_entre}</td>
                    <td>${demanda_diaria_db.total_noentre}</td>
                 
                    <td>
                        <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>`;
        });
        tableBody_demandadiaria.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});