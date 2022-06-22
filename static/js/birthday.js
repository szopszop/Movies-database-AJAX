const monthInput = document.querySelector('#months2');
const nameInput = document.querySelector('#actor_name');
const actorsList = document.querySelector('#month_actors');

const requestMonthActors = async (month, searchPhrase) => {
    const response = await fetch('/birthday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'month': month, 'name': searchPhrase})
    });

    return await response.json()
};

const updateMonthActors = () => {
    const actors = monthInput.value;
    const searchPhrase = nameInput.value;


    requestMonthActors(actors, searchPhrase)
        .then(data => {
            console.log(data)
            actorsList.innerHTML = '';

            data.forEach(actor => {
                console.log(actor)
                actorsList.innerHTML += `<li>${actor.name}</li>
                                        <li>${actor.month}</li>
                                        <li>${actor.shows}</li>`

            });
        })
        .catch(err => console.log(err));
};

const init = () => {
    monthInput.addEventListener('change', updateMonthActors);
    nameInput.addEventListener('input', updateMonthActors);
};

init();