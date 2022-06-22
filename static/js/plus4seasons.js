const seasonSearchInput = document.querySelector('#nameSeason')
const seasons = document.querySelector('#tableBodySeasons')

const requestSeasons = async (searchPhrase) => {
    const response = await fetch('plus-4-seasons', {
            method: 'POST',
            headers:{
            'Content-Type':'application/json'
            },
            body: JSON.stringify({'phrase': searchPhrase})
            });
            return await response.json()
    }

    const updateSeasons = () => {
        const searchPhrase = seasonSearchInput.value

        requestSeasons(searchPhrase)
            .then(data => {
                seasons.innerHTML = ''
                data.forEach(season => {
                    console.log(season.title)

                    seasons.innerHTML += `<td>${season.title}</td>
                                        <td>${season.year}</td>
                                        <td>${season.trailer}</td>
                                        <td>${season.number_of_seasons}</td>`
                })
            })
            .catch(err => console.log(err))
    }

    const init = () => {
    seasonSearchInput.addEventListener('input', updateSeasons)
    }

    init()