const buscar = document.getElementById('search_btn');
const filter = document.getElementById('filter_btn');
const search = document.getElementById('search');

const btn = document.getElementById("btn");
const img = document.getElementById("img");
img.style.display = "none";
btn.addEventListener("click", () => {
    if (img.style.display === "none") {
        img.style.display = "block";
        btn.innerHTML = "Ocultar";
    } else {
        img.style.display = "none";
        btn.innerHTML = "Mostrar Grafo";
    }
});

// When buscar is pressed send to the server the search value and redirect to the search page
const markCheckboxesFromQuery = (paramName, checkboxPrefix) => {
    const checkboxes = document.querySelectorAll(`input[name="${paramName}"]`);
    const queryParams = urlParams.getAll(paramName);

    checkboxes.forEach((checkbox) => {
        const checkboxValue = checkbox.id.replace(`${checkboxPrefix}`, '');
        queryParams.forEach((queryParam) => {
            if (queryParam.includes(checkboxValue)) {
                checkbox.checked = true;
            }
        });
    });
}

const urlParams = new URLSearchParams(window.location.search);

// Marcar checkboxes para años
markCheckboxesFromQuery('year_of_release', 'year_of_release_');

// Marcar checkboxes para plataformas
markCheckboxesFromQuery('plataforma', 'plataform_');

// Marcar checkboxes para géneros
markCheckboxesFromQuery('genero', 'genre_');

// Poner el valor de amount
const amount = urlParams.get('amount');
const amountInput = document.getElementById('custom-input-number');
if (amount >= 1)
    amountInput.value = amount;

const searchValue = urlParams.get('search');
if (searchValue)
    search.value = searchValue;

const getPlataformFilterValues = () => {
    const genres = document.querySelectorAll('input[name="plataforma"]');
    const genresFilter = [];
    genres.forEach((pla) => {
        if (pla.checked) {
            genresFilter.push(pla.nextElementSibling.textContent.trim());
        }
    });
    return genresFilter;
}

const getGenresFilterValues = () => {
    const genres = document.querySelectorAll('input[name="genero"]');
    const genresFilter = [];
    genres.forEach((genre) => {
        if (genre.checked) {
            genresFilter.push(genre.nextElementSibling.textContent.trim());
        }
    });
    return genresFilter;
}


const getYearsFilterValues = () => {
    const years = document.querySelectorAll('input[name="year_of_release"]');
    const yearsFilter = [];
    years.forEach((year) => {
        if (year.checked) {
            yearsFilter.push(year.nextElementSibling.textContent.trim());
        }
    });
    return yearsFilter;
}

const getAmountOfGames = () => {
    const amount = document.getElementById('custom-input-number');
    return amount.value;
}

buscar.addEventListener('click', () => {
    const searchValue = search.value;
    const plataformsFilter = getPlataformFilterValues();
    const genresFilter = getGenresFilterValues();
    const agesFilter = getYearsFilterValues();
    const amountOfGames = getAmountOfGames();
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    params.set('search', searchValue);
    if (plataformsFilter.length > 0)
        params.set('plataforma', plataformsFilter);
    else
        params.delete('plataforma');
    if (genresFilter.length > 0)
        params.set('genero', genresFilter);
    else
        params.delete('genero');
    if (agesFilter.length > 0)
        params.set('year_of_release', agesFilter);
    else
        params.delete('year_of_release');
    params.set('amount', amountOfGames);
    window.location.href = `/search-game?${params.toString()}`;
});

filter.addEventListener('click', () => {
    const searchValue = search.value;
    const plataformsFilter = getPlataformFilterValues();
    const genresFilter = getGenresFilterValues();
    const agesFilter = getYearsFilterValues();
    const amountOfGames = getAmountOfGames();
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    params.set('search', searchValue);
    if (plataformsFilter.length > 0)
        params.set('plataforma', plataformsFilter);
    else
        params.delete('plataforma');
    if (genresFilter.length > 0)
        params.set('genero', genresFilter);
    else
        params.delete('genero');
    if (agesFilter.length > 0)
        params.set('year_of_release', agesFilter);
    else
        params.delete('year_of_release');
    params.set('amount', amountOfGames);
    window.location.href = `/search-game?${params.toString()}`;
});