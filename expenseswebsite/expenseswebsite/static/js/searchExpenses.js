const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container")
const noResults = document.querySelector(".no-results")
const tbody = document.querySelector(".table-body")
const monthFilter = document.querySelector("#monthFilter");  
const vigenciaField = document.querySelector("#vigenciaFilter");
const estadoField = document.querySelector("#estadoFilter");
const tipoField = document.querySelector("#tipoFilter");
const registrados = document.querySelector(".registrados");
const edadField = document.querySelector("#edadFilter")

tableOutput.style.display = "none";
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).replace(/\//g, '-');
}
function invertirFecha(dateString) {
    const parts = dateString.split('-');
    if (parts.length === 3) {
        return `${parts[1]}-${parts[0]}-${parts[2]}`;
    } else {
        return dateString; 
    }
}

function updateTable() {
    const searchValue = searchField.value.trim();
    const selectedMonth = monthFilter.value;
    const vigenciaValue = vigenciaField.value.trim();
    const estadoValue = estadoField.value.trim();
    const tipoValue = tipoField.value;
    const edadValue = edadField.value.trim();

    tbody.innerHTML = "";

    if (searchValue.length > 0 || selectedMonth !== '0' || vigenciaValue.length > 0 || estadoValue != '0' || tipoValue != '0' || edadValue.length > 0) {
        fetch("/search-expenses", {
            body: JSON.stringify({ 
                searchText: searchValue, 
                searchMonth: selectedMonth, 
                searchVigencia: vigenciaValue,
                searchEstado: estadoValue,
                searchTipo: tipoValue, 
                searchEdad: edadValue
            }),  
            method: "POST"
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            appTable.style.display = "none";
            paginationContainer.style.display = "none";
            tableOutput.style.display = "block";
            if (data.length === 0 ) {
                noResults.style.display = "block"
                tableOutput.style.display = "none"
            } else {
                noResults.style.display = "none"
                registrados.innerText = `${data.total_expenses}`;
                data.expenses_data.forEach(item => {

                    const formattedFechaNacimiento = invertirFecha(formatDate(item.fecha_nacimiento));
                    const formattedFechaInscripcion = invertirFecha(formatDate(item.fecha_inscripcion));
                  
                    
                        tbody.innerHTML += `
                        
                        <tr>
                        <td>
                        <a style="text-align: center;"><a href="${expenseEditUrl.replace('item.id', item.id)}"
                        class="btn btn-secondary btn-sm mx-3">Editar</a></a>
                    <a style="text-align: center;"><a href="${expenseFinanzasUrl.replace('item.id', item.id)}"
                        class="btn btn-info btn-sm">Finanzas</a></a>
                        </td>
                        <td>${  item.cedula_ruc}</td>
                        <td>${ item.razon_social}</td>
                        <td>${ formattedFechaNacimiento}</td>
                        <td>${ formattedFechaInscripcion }</td>
                        <td>${ item.nombre_comercial}</td>
                        <td>${ item.actividad}</td>
                        <td>${ item.telefonos}</td>
                        <td>${ item.email}</td>
                        <td>${ item.pertenece_comite}</td>
                        <td style="min-width: 250px;  font-size:small;"><p style="min-height: 30px;">${ item.dir_comercial}</p> <p style="text-align: center;"><a href="${expenseComercialMapUrl.replace('item.id', item.id)}"
                            class = "btn btn-light btn-sm mt-3"><img src="/static/img/map.png" class="img-fluid mx-2" style="width: 7%;"  alt="">Abrir Mapa</a></p></td>
                        <td style="min-width: 250px;  font-size:small;  "><p style="min-height: 30px;">${ item.dir_domicilio}</p>  <p style="text-align: center;"><a href="${expenseDomicilioMapUrl.replace('item.id', item.id)}"
                            class = "btn btn-light btn-sm mt-3"><img src="/static/img/map.png" class="img-fluid mx-2" style="width: 7%;"  alt="">Abrir Mapa</a></p></td>
                        <td>${ item.nmesesvigencia}</td>
                        <td>${ item.tipo_socio}</td>
                        <td>${ item.recaudador}</td>
                        <td>${ item.genero}</td>
                        <td>${ item.linea_negocio}</td>
                        <td>${ item.estado}</td>
                        <td>${ item.aseguradora}</td>
                        <td>${ item.nacionalidad}</td>
                        <td>${ item.estado_civil}</td>
                        <td>${ item.movil}</td>
                        <td>${ item.nombre}</td>
                        <td>${ item.representantelegal}</td>
                        <td>${ item.conyuge}</td>
                        <td>${ item.latitud_comercial}</td>
                        <td>${ item.longitud_comercial}</td>
                        <td>${ item.latitud_domicilio}</td>
                        <td>${ item.longitud_domicilio}</td>
    
                    </tr>
                    
                        `;
                    
                });
            }
        });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        registrados.innerText = ` --- `;
    }
}


monthFilter.addEventListener("change", updateTable);
searchField.addEventListener("keyup", updateTable);
vigenciaField.addEventListener("keyup", updateTable);
estadoField.addEventListener("change", updateTable);
tipoField.addEventListener("change", updateTable);
edadField.addEventListener("keyup", updateTable);


updateTable();
