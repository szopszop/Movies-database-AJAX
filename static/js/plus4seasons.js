const tableBody = document.querySelector('#tableBodySeasons');

const getSeasons = async order => {
    const response = await fetch('/plus-4-seasons', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify()
    });
    console.log(response)
    return await response.json();
};

const updateTableYears = data => {
    tableBody.innerHTML = '';
    console.log(data)

    data.forEach(element => {
        console.log(element)
        tableBody.innerHTML += `<tr>
                                    <td>${element.id}</td>
                                    <td>${element.name}</td>
                                    <td>${element.date}</td>
                                    <td>${element.character}</td>
                                </tr>`
    });
};

tableHead.addEventListener('click', event => {
    if(event.target.parentElement.parentElement.dataset.order === 'desc') {
        event.target.parentElement.parentElement.dataset.order = 'asc';
        getSeasons('asc').then(response => {
            updateTableYears(response);
        })
    } else {
        event.target.parentElement.parentElement.dataset.order = 'desc';
        getSeasons('desc').then(response => {
            updateTableYears(response);
        })
    }
});
