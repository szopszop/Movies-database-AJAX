const tableHead = document.querySelector('#tableHead');
const tableBody = document.querySelector('#tableBody');

const getOrderedShows = async order => {
    const response = await fetch('/ordered-shows', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'order': order})
    });
    console.log(response)
    return await response.json();
};

const updateTable = data => {
    tableBody.innerHTML = '';

    data.forEach(element => {
        const rating = '☆'.repeat(Math.round(Number(element.rating)));

        tableBody.innerHTML += `<tr>
                                    <td>${element.title}</td>
                                    <td>${rating}</td>
                                </tr>`
    });
};

tableHead.addEventListener('click', event => {
    if(event.target.parentElement.parentElement.dataset.order === 'desc') {
        event.target.parentElement.parentElement.dataset.order = 'asc';
        getOrderedShows('asc').then(response => {
            updateTable(response);
        })
    } else {
        event.target.parentElement.parentElement.dataset.order = 'desc';
        getOrderedShows('desc').then(response => {
            updateTable(response);
        })
    }
});
