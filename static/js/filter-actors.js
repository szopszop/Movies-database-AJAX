const genresInput = document.querySelector('#genres');
const searchInput = document.querySelector('#name');
const actors = document.querySelector('#actors');

const requestActors = async (genre, searchPhrase) => {
    const response = await fetch('/filter-actors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'genre': genre, 'name': searchPhrase})
    });

    return await response.json()
};

const updateActors = () => {
    const genre = genresInput.value;
    const searchPhrase = searchInput.value;

    requestActors(genre, searchPhrase)
        .then(data => {
            actors.innerHTML = '';

            data.forEach(actor => {
                actors.innerHTML += `<li>${actor.name}</li>`
            });
        })
        .catch(err => console.log(err));
};

const init = () => {
    genresInput.addEventListener('change', updateActors);
    searchInput.addEventListener('input', updateActors);
};

init();