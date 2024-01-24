const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container")
const noResults = document.querySelector(".no-results")
const tbody = document.querySelector(".table-body")
tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        console.log('searchValue', searchValue)
        tbody.innerHTML = "";
        fetch("/search-expenses", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST"
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data)
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
                            <td><a href="${expenseEditUrl.replace('item.id', item.id)}"
                class="btn btn-secondary btn-sm">Editar</a></td>
                            <td>${item.cedula_ruc}</td>
                            <td>${item.razon_social}</td>
                            <td>${item.cuota_total}</td>
                            <td>${item.cuota_ult_fecha}</td>
                            <td>${item.emitidas}</td>
                            <td>${item.cuota_nro}</td>
                            <td>${item.fecha_nacimiento}</td>
                            <td>${item.fecha_inscripcion}</td>
                            <td>${item.nombre_comercial}</td>
                            <td>${item.actividad}</td>
                            <td>${item.telefonos}</td>
                            <td>${item.email}</td>
                            <td>${item.pertenece_comite}</td>
                            <td>${item.ultimo_pago}</td>
                            <td>${item.dir_comercial}</td>
                            <td>${item.dir_domicilio}</td>
                            <td>${item.nmesesaportados}</td>
                            <td>${item.nmesesvigencia}</td>
                            <td>${item.tipo_socio}</td>
                            <td>${item.recaudador}</td>
                            <td>${item.genero}</td>
                            <td>${item.linea_negocio}</td>
                            <td>${item.estado}</td>
                            <td>${item.aseguradora}</td>
                            <td>${item.nacionalidad}</td>
                            <td>${item.estado_civil}</td>
                            <td>${item.movil}</td>
                            <td>${item.nombre}</td>
                            <td>${item.representantelegal}</td>
                            <td>${item.conyuge}</td>
                            <td>${item.fechaactualizacion}</td>
                            <td>${item.fechaultimafact}</td>
                            <td>${item.idclase}</td>
                            <td>${item.fecha_ultima_factura}</td>
                            <td>${item.id}</td>
                            
                    `
                    })
                }
            });
    } else {
        tableOutput.style.display = "none"
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
})