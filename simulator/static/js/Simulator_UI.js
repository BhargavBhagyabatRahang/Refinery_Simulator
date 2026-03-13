async function fetchData(url){
    const response = await fetch(url)
    return await response.json()
}

function updateLiveStatus(hasData){

    const status = document.getElementById("liveStatus")

    if(hasData){

        status.innerText = "● LIVE"
        status.classList.remove("bg-danger")
        status.classList.add("bg-success")
        status.classList.add("blinking")

    }else{

        status.innerText = "❌ No Data"
        status.classList.remove("bg-success")
        status.classList.remove("blinking")
        status.classList.add("bg-danger")

    }

}

function isRecent(timestamp){

    const dataTime = new Date(timestamp)
    const now = new Date()

    const diff = (now - dataTime) / 1000

    return diff < 60
}

async function loadData(){

    try{

        const thickness = await fetchData("/api/thickness/")
        const dcs = await fetchData("/api/dcs/")
        const lab = await fetchData("/api/lab/")

        let live = false

        if(thickness.length > 0 && isRecent(thickness[0].timestamp)){
            live = true
        }

        if(dcs.length > 0 && isRecent(dcs[0].timestamp)){
            live = true
        }

        if(lab.length > 0 && isRecent(lab[0].timestamp)){
            live = true
        }

        updateLiveStatus(live)

        const thicknessBox = document.getElementById("thicknessFeed")
        const dcsBox = document.getElementById("dcsFeed")
        const labBox = document.getElementById("labFeed")

        // clear previous entries
        thicknessBox.innerHTML = ""
        dcsBox.innerHTML = ""
        labBox.innerHTML = ""

        thickness.forEach(t => {

            const div = document.createElement("div")
            div.className = "log-entry"

            div.innerText =
                `${t.timestamp} | ${t.pipeline__name} | ${t.thickness} mm`

            thicknessBox.appendChild(div)

        })

        dcs.forEach(d => {

            const div = document.createElement("div")
            div.className = "log-entry"

            div.innerText =
                `${d.timestamp} | ${d.unit} | Temp:${d.temperature}`

            dcsBox.appendChild(div)

        })

        lab.forEach(l => {

            const div = document.createElement("div")
            div.className = "log-entry"

            div.innerText =
                `${l.timestamp} | ${l.unit} | Sulfur:${l.sulfur_content}`

            labBox.appendChild(div)

        })

    }
    catch(err){

        updateLiveStatus(false)

    }

}

setInterval(loadData,3000)

loadData()