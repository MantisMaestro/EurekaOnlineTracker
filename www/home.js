const button = document.getElementById("refreshButton")

button.addEventListener("click", (event) => {
    RetrieveOnlinePlayers();
});

window.onload = (event) => {
    RetrieveOnlinePlayers()
    GetPlaytimeLeaders()
}

function RetrieveOnlinePlayers()
{
    let response = fetch('http://127.0.0.1:5000/online_players')
        .then(response => response.json())
        .then(jsonData => {
            const rows = document.querySelectorAll("#playerOnlineTable > tbody > tr")
            rows.forEach(element => element.remove())

            const tableBody = document.querySelector("#playerOnlineTable > tbody")

            let players = jsonData["players"]
            for (let i = 0; i < players.length; i++) {
                let rowElement = buildOnlineTableRow(players[i]["name"])
                tableBody.insertAdjacentHTML('beforeend', rowElement)
            }
        })
}

function GetPlaytimeLeaders()
{
    let response = fetch('http://127.0.0.1:5000/top_players/5')
        .then(response => response.json())
        .then(jsonData => {
            const rows = document.querySelectorAll("#playerTimeLeaderBoard > tbody > tr")
            rows.forEach(element => element.remove())
            
            const tableBody = document.querySelector("#playerTimeLeaderBoard > tbody")
            
            jsonData.forEach(element => {
                
                let rowElement = buildPlaytimeTableRow(element[0], secondsToTimeString(element[1]))
                tableBody.insertAdjacentHTML('beforeend', rowElement)
            })
        })
}

function secondsToTimeString(seconds) {
    const hours = Math.floor(seconds / 3600);
    const remainingSeconds = seconds % 3600;
    const minutes = Math.floor(remainingSeconds / 60);
    if(hours === 0)
    {
        return `${minutes} Minutes`;
    }
    return `${hours} Hours ${minutes} Minutes`;
}

function buildOnlineTableRow(playerName)
{
    return `
    <tr>
        <th>${playerName}</th>
        <td>
            <img src="https://cravatar.eu/helmavatar/${playerName}/64.png" alt="Player Icon for ${playerName}">
        </td>
    </tr>
    `
}

function buildPlaytimeTableRow(playerName, playtime)
{
    return `
    <tr>
        <th>${playerName}</th>
        <td>${playtime}</td>
        <td>
            <img src="https://cravatar.eu/helmavatar/${playerName}/64.png" alt="Player Icon for ${playerName}">
        </td>
    </tr>
    `
}