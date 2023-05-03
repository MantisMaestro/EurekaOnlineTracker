const button = document.getElementById("refreshButton")

button.addEventListener("click", (event) => {
    RetrieveOnlinePlayers()
    GetPlaytimeLeaders()
});

window.onload = (event) => {
    RetrieveOnlinePlayers()
    GetPlaytimeLeaders()
}

function RetrieveOnlinePlayers() {
    let response = fetch('https://eureka.agamemnon.dev/api/online_players')
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

function GetPlaytimeLeaders() {
    let response = fetch('https://eureka.agamemnon.dev/api/top_players/5')
        .then(response => response.json())
        .then(jsonData => {
            const rows = document.querySelectorAll("#playerTimeLeaderBoard > tbody > tr")
            rows.forEach(element => element.remove())
            const tableBody = document.querySelector("#playerTimeLeaderBoard > tbody")

            let players = jsonData["players"], objects = [];
            for(let i in players) {
                objects.push(players[i].time_online_seconds)
            }

            let sortedPlayers = players.sort((a,b) => (a.time_online_seconds > b.time_online_seconds) ? -1 : ((b.time_online_seconds > a.time_online_seconds) ? 1 : 0));

            sortedPlayers.forEach(element => {
                if (element.name != "Anonymous Player") {
                    let rowElement = buildPlaytimeTableRow(element.name, secondsToTimeString(element.time_online_seconds))
                    tableBody.insertAdjacentHTML('beforeend', rowElement)
                }
            })
        })
}

function secondsToTimeString(seconds) {
    const hours = Math.floor(seconds / 3600);
    const remainingSeconds = seconds % 3600;
    const minutes = Math.floor(remainingSeconds / 60);
    if (hours === 0) {
        if (minutes === 1) return `${minutes} Minute`;
        return `${minutes} Minutes`;
    }

    if (hours === 1) return `${hours} Hour ${minutes} Minutes`;
    return `${hours} Hours ${minutes} Minutes`;
}

function buildOnlineTableRow(playerName) {
    return `
    <tr>
        <th>${playerName}</th>
        <td>
            <img src="https://cravatar.eu/helmavatar/${playerName}/64.png" alt="Player Icon for ${playerName}">
        </td>
    </tr>
    `
}

function buildPlaytimeTableRow(playerName, playtime) {
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