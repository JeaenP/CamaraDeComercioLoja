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
        return dateString; // Devuelve la fecha original si no tiene el formato esperado
    }
}
// Función para actualizar la tabla
function updateTable() {
    const searchValue = searchField.value.trim();
    const selectedMonth = monthFilter.value;
    const vigenciaValue = vigenciaField.value.trim();
    const estadoValue = estadoField.value.trim();
    const tipoValue = tipoField.value;
    const edadValue = edadField.value.trim();

    tbody.innerHTML = "";

    if (searchValue.length > 0 || selectedMonth !== '0' || vigenciaValue.length > 0 || estadoValue != '0' || tipoValue != '0' || edadValue.length > 0) {
        fetch("/expor-csv", {
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
        });
    } else {
    }
}

// Agregar eventos al cambio de mes y al escribir en el campo de búsqueda
monthFilter.addEventListener("change", updateTable);
searchField.addEventListener("keyup", updateTable);
vigenciaField.addEventListener("keyup", updateTable);
estadoField.addEventListener("change", updateTable);
tipoField.addEventListener("change", updateTable);
edadField.addEventListener("keyup", updateTable);

// Llamada inicial para manejar el estado inicial de la tabla
updateTable();
