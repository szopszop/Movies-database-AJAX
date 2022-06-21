const tableHead = document.querySelector('#tableHeadYear');
const tableBody = document.querySelector('#tableBodyYear');

const getOrderedYears = async order => {
    const response = await fetch('/year-exam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'order': order})
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
        getOrderedYears('asc').then(response => {
            updateTableYears(response);
        })
    } else {
        event.target.parentElement.parentElement.dataset.order = 'desc';
        getOrderedYears('desc').then(response => {
            updateTableYears(response);
        })
    }
});
