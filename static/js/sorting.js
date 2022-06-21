const tableHeaders = document.querySelector('#showsTableHeader').children[0].children
const url = window.location.href;

if (url.includes('asc')) {
    Array.from(tableHeaders).forEach(header => {
        if (url.includes(header.innerText.toLowerCase()) ||
            url.includes('runtime') && header.innerText === 'Runtime (min)' ||
            url.includes('most-rated') && header.innerText === 'Rating') {
            header.children[0].innerText = '⇧' + header.innerText;
        }
    });
} else {
    Array.from(tableHeaders).forEach(header => {
        if (url.includes(header.innerText.toLowerCase()) ||
            url.includes('runtime') && header.innerText === 'Runtime (min)' ||
            url.includes('most-rated') && header.innerText === 'Rating') {
            header.children[0].innerText = '⇩' + header.innerText;
        }
    });
}