
const noResults = document.querySelector(".no-results")
const noResults2 = document.querySelector(".no-results2")

function mostrarUbicacion(id, latitud, longitud) {
    const mapaDiv = document.getElementById('mapa_' + id);
    if( latitud === null || !longitud === null ) { 
        noResults.style.display = "block"
        noResults2.style.display = "block"
        mapaDiv.style.display = 'none';
    } else { 
        
        map = inicializarMapa(latitud, longitud, mapaDiv);
        mapaDiv.style.display = 'block';
    }
    
}

function inicializarMapa(latitud, longitud, mapaDiv) {
    var myLatlng = new google.maps.LatLng(latitud, longitud);
    var mapOptions = {
        center: myLatlng,
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(mapaDiv, mapOptions);

    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'Ubicación'
    });
}


