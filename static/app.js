$('.edit-user').click(editUser)
$('.delete-user').click(deleteUser)

async function editUser() {
    const id = $(this).data('id')
    await axios.patch(`/user/${id}`)
    alert(`UPDATED ${id}`)
}

async function deleteUser() {
    const id = $(this).data('id')
    await axios.delete(`/user/${id}`)
    alert(`DELETED ${id}`)
}

function get(url) {
    const request = new XMLHttpRequest();
    return new Promise((resolve, reject) => {
        request.onload = function () {
            if (request.readyState !== 4) return;
        
            // Check status code
            if (request.status >= 200 && request.status < 300) {
                resolve({
                    data: JSON.parse(request.response),
                    status: request.status,
                    request: request,
                });
            } else {
                reject({
                    msg: 'Server Error',
                    status: request.status,
                    request: request
                })
            }
        }
        request.onerror = function handleError() {
            reject({
                msg: 'NETWORK ERROR'
            })
            request = null;
        };
        request.open('GET', url);
        request.send(); 
    })
}

get('http://www.7timer.info/bin/api.pl?lon=-98.6189&lat=29.5827&product=civillight&unit=metric&output=json')
    .then(res => {
        console.log(res.data.dataseries[0])    // Grabs today's weather   
        maxTemp = (res.data.dataseries[0].temp2m.max * 9/5) + 32;
        minTemp = (res.data.dataseries[0].temp2m.min * 9/5) + 32;
        weather = res.data.dataseries[0].weather;
        let weatherInfo = document.querySelector('#weather')
        weatherInfo.innerHTML = `Current weather in UTSA &#124; High: ${maxTemp}&#8457;, Low: ${minTemp}&#8457;, Weather: ${weather}`;
    })
    .catch(err => console.log(err))