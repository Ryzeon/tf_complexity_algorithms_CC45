const gender_filter = document.getElementById("genre-filter")
const year_filter = document.getElementById("year-filter")
const platform_filter = document.getElementById("platform-filter")

const urlParams = new URLSearchParams(window.location.search);

if (urlParams.has("genero")) {
    gender_filter.value = urlParams.get("genero")
}
if (urlParams.has("year_of_release")) {
    year_filter.value = urlParams.get("year_of_release")
}
if (urlParams.has("plataforma")) {
    platform_filter.value = urlParams.get("plataforma")
}

function onChangeFilter() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    if (gender_filter.value !== "Todos") {
        params.set("genero", gender_filter.value)
    } else {
        params.delete("genero")
    }
    if (year_filter.value !== "Todos") {
        params.set("year_of_release", year_filter.value)
    } else {
        params.delete("year_of_release")
    }
    if (platform_filter.value !== "Todas") {
        params.set("plataforma", platform_filter.value)
    } else {
        params.delete("plataforma")
    }
    if (params.toString() !== "") {
        window.location.href = `/?${params.toString()}`;
    } else {
        window.location.href = `/`;
    }
}

gender_filter.addEventListener("change", onChangeFilter)
year_filter.addEventListener("change", onChangeFilter)
platform_filter.addEventListener("change", onChangeFilter)