const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container")
const noResults = document.querySelector(".no-results")
const tbody = document.querySelector(".table-body")
let debounceTimer;
tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => { 
    const searchValue = e.target.value;

        if (searchValue.trim().length > 0) {
            console.log('searchValue', searchValue)
            tbody.innerHTML = "";
            fetch("/search-finanza", {
                body: JSON.stringify({ searchText: searchValue }),
                method: "POST"
            })
                .then((res) => res.json())
                .then((data) => {
                    
                    appTable.style.display = "none";
                    paginationContainer.style.display = "none";
                    tableOutput.style.display = "block";
                    if (data.length === 0) {
                        noResults.style.display = "block"
                        tableOutput.style.display = "none"
                    } else {
                        noResults.style.display = "none"
                        data.forEach(item => {
                            tbody.innerHTML += `
                            <tr>
                            <td>
                                <a style="text-align: center;"><a href="{% url 'expense-edit' expense.id %}"
                                    class = "btn btn-secondary btn-sm mx-3">Pago</a></a>
                                <a style="text-align: center;"><a href="{% url 'expense-edit' expense.id %}"
                                    class = "btn btn-info btn-sm">Historial</a></a>
                            </td>
                            <td>${ item.cedula_ruc}</td>
                            <td>${ item.cuota_total}</td>
                            <td>${ item.cuota_ult_fecha}</td>
                            <td>${ item.emitidas}</td>
                            <td>${ item.cuota_nro}</td>
                            <td>${ item.ultimo_pago}</td>
                            <td>${ item.nmesesaportados}</td>
                            <td>${ item.recaudador}}</td>
                            <td>${ item.fechaactualizacion}</td>
                            <td>${ item.fechaultimafact}</td>
                            <td>${ item.idclase}</td>
                            <td>${ item.fecha_ultima_factura}</td>
       
                        </tr>
                                
                        `
                        })
                    }
                });
        } else {
            tableOutput.style.display = "none"
            appTable.style.display = "block";
            paginationContainer.style.display = "block";
        }
    }, 200);
    
});