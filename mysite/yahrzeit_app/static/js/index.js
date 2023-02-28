'use strict';


function useAutocomplete() {
    const dateInput = document.getElementById('decedent-date');
    const TODRadios = document.getElementById('TOD-radios');
    TODRadios.style.display = 'none';

    const locationInput = document.getElementById('location');
    const locationOptions = {
        fields: ["formatted_address", "geometry", "name"],
    };

    const autoComplete = new google.maps.places.Autocomplete(locationInput, locationOptions);

    function getSunsetTimes() {
        if (dateInput.value && autoComplete.getPlace()) {
            const place = autoComplete.getPlace();
            const url = `api/get-sunset-time/${dateInput.value}/${place.formatted_address}`;
            fetch(url)
            .then((res) => res.json())
            .then((resData) => {
                const sunsetTime = resData['sunset_time'];
                document.getElementById('before-sunset-label').innerHTML = `Before ${sunsetTime}`;
                document.getElementById('after-sunset-label').innerHTML = `After ${sunsetTime}`;
                TODRadios.style.display = 'block';
            });
        }  
    }

    dateInput.addEventListener('change', getSunsetTimes);

    autoComplete.addListener('place_changed', getSunsetTimes);
}

