const refreshButton = document.getElementById("refreshButton")
const dateSelectorButton = document.getElementById("dateSelectorButton")

refreshButton.addEventListener("click", (event) => {
    RetrieveOnlinePlayers()
    GetPlaytimeLeaders()
});

dateSelectorButton.addEventListener("click", (event) => {
    const fromDate = document.getElementById("from_date").value;
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(fromDate)) {
        console.log("Invalid date format. Please use the format YYYY-MM-DD.");
    }

    const toDate = document.getElementById("to_date").value;
    if (!dateRegex.test(toDate)) {
        console.log("Invalid date format. Please use the format YYYY-MM-DD.");
    }

    if (fromDate > toDate) {
        console.log("to_date must be after from_date.");
    }

    GetPlaytimeLeaders(fromDate, toDate);
});



window.onload = (event) => {
    RetrieveOnlinePlayers()
    GetPlaytimeLeaders()
}

function RetrieveOnlinePlayers() {
    let url = getBaseURL() + "online_players"
    let response = fetch(url)
        .then(response => response.json())
        .then(jsonData => {
            const rows = document.querySelectorAll("#playerOnlineTable > tbody > tr")
            rows.forEach(element => element.remove())
            const tableBody = document.querySelector("#playerOnlineTable > tbody")

            let players = jsonData["players"]
            players = players.filter(player => player.name !== "Anonymous Player");
            for (let i = 0; i < players.length; i++) {
                let rowElement = buildOnlineTableRow(players[i]["name"])
                tableBody.insertAdjacentHTML('beforeend', rowElement)
            }
        })
}

function GetPlaytimeLeaders(fromDate, toDate) {
    let url = `${getBaseURL()}top_players/5`;
    if (fromDate && toDate) {
        url += `?from_date=${fromDate}&to_date=${toDate}`;
    }
    let response = fetch(url)
        .then(response => response.json())
        .then(jsonData => {
            const rows = document.querySelectorAll("#playerTimeLeaderBoard > tbody > tr")
            rows.forEach(element => element.remove())
            const tableBody = document.querySelector("#playerTimeLeaderBoard > tbody")

            let objects = [];
            for(let i in jsonData) {
                objects.push(jsonData[i])
            }

            objects = objects.filter(player => player.name !== "Anonymous Player");
            let sortedPlayers = objects.sort((a,b) => (a.time_online_seconds > b.time_online_seconds) ? -1 : ((b.time_online_seconds > a.time_online_seconds) ? 1 : 0));
            let sortedSubset = sortedPlayers.slice(0, 5)

            sortedSubset.forEach(element => {
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

function getBaseURL() {
    // return "http://127.0.0.1:5000/"
    return "https://eureka.agamemnon.dev/api/"
}

function getShortDateStrin(date) {
    return date.toLocaleDateString("en-US", {year: 'numeric', month: 'short', day: 'numeric'})
}