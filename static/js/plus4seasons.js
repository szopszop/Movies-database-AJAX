const tableBody = document.querySelector('#tableBodySeasons');
const tableHead = document.querySelector('#tableHeadSeasons');

const getSeasons = async phrase => {
    const response = await fetch('/plus-4-seasons', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'phrase': phrase})
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
