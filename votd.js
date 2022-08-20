var votd = ''
var rotd = ''
var deets = {}
const options = { method: 'GET', headers: { Accept: 'application/json' } };

fetch('https://beta.ourmanna.com/api/v1/get?format=json&order=daily', options)
    .then(response => response.json())
    .then(response => deets = response.verse.details)
    // .then(response => rotd = response.verse.details.reference)
    .then(response => console.log(response))
    .then(response => document.getElementById('verse-text').innerHTML = deets.text)
    .then(response => document.getElementById('verse-reference').innerHTML = deets.reference)
    .catch(err => console.error(err));