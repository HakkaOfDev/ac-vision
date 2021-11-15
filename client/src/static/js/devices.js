let ubiquiti_container = document.querySelector("#ubiquiti")
let dasan_container = document.querySelector("#dasan")

ubiquiti_container.addEventListener('click', (e) => {
    ubiquiti_container.classList.toggle('active')
    let ubiquiti_content = document.querySelector("#ubiquiti_content")
    if (ubiquiti_content.style.display === "flex") {
        ubiquiti_content.style.display = "none";
    } else {
        ubiquiti_content.style.display = "flex";
    }
})

dasan_container.addEventListener('click', (e) => {
    dasan_container.classList.toggle('active')
    let dasan_content = document.querySelector("#dasan_content")
    if (dasan_content.style.display === "flex") {
        dasan_content.style.display = "none";
    } else {
        dasan_content.style.display = "flex";
    }
})

function updateUbiquiti() {
    let ubiquiti_olt = $('#ubiquiti_olt')
    let ubiquiti_onus = $('#ubiquiti_onus')

    ubiquiti_olt.innerHTML = ""
    ubiquiti_onus.innerHTML = ""

    let token = JSON.parse($.cookie('user')).acces_token
    let olt_html = ""
    fetch('http://ac-vision/api/v1.0/ressources/ubiquiti/olt', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((olt) => {
        olt_html += "<td class='py-1.5'>" + olt.displayName + "</td>";
        olt_html += "<td class='whitespace-nowrap'>";
        if (olt.status === "active") {
            olt_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-green-500 uppercase text-green-500'>Connected</span>"
        } else {
            olt_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-red-500 uppercase text-red-500'>Disconnected</span>"
        }
        olt_html += "</td>"
        olt_html += "<td>" + olt.mac + "</td>"
        olt_html += "<td>" + olt.ip + "</td>"
        olt_html += "<td>" + olt.temperature + "°</td>"
        if (olt.status === "active") {
            olt_html += "<td class='text-green-500'>" + olt.uptime + "</td>"
        } else {
            olt_html += "<td class='text-red-500'>" + olt.uptime + "</td>"
        }
        ubiquiti_olt.append($(olt_html))
    });

    let onus_html = ""
    onus_html += "<tr class='bg-gray-50'><th class='py-2 px-4'>Name</th><th class='py-2 px-4'>Status</th><th class='py-2 px-4'>Port</th><th class='py-2 px-4'>Serial Number</th><th class='py-2 px-4'>@MAC</th><th class='py-2 px-4'>IP</th><th class='py-2 px-4'>RxPower</th><th class='py-2 px-4'>Distance</th><th class='py-2 px-4'>Uptime</th></tr>";
    fetch('http://ac-vision/api/v1.0/ressources/ubiquiti/onus', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((onus) => {
        onus.forEach((onu) => {
                onus_html += "<tr class='text-gray-800 text-sm'>"
                onus_html += "<td>" + onu.displayName + "</td>"
                onus_html += "<td class='whitespace-nowrap'>"
                if (onu.status === "active") {
                    onus_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-green-500 uppercase text-green-500'>Connected</span>"
                } else {
                    onus_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-red-500 uppercase text-red-500'>Disconnected</span>"
                }
                onus_html += "</td>"
                onus_html += "<td>GPON " + onu.port + "</td>"
                onus_html += "<td>" + onu.serialNumber + "</td>"
                onus_html += "<td>" + onu.mac + "</td>"
                onus_html += "<td>" + onu.ip + "</td>"
                onus_html += "<td class='flex flex-row items-center justify-center space-x-1 py-1.5'>"
                if (onu.rxPower < -25) {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-red-300'>"
                    onus_html += "<div class='w-1/4 shadow-none whitespace-nowrap bg-red-600'></div>"
                } else if (onu.rxPower > -15) {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-green-300'>"
                    onus_html += "<div class='w-3/4 shadow-none whitespace-nowrap bg-green-600'></div>"
                } else {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-yellow-300'>"
                    onus_html += "<div class='w-1/2 shadow-none whitespace-nowrap bg-yellow-600'></div>"
                }
                onus_html += "</div>"
                onus_html += "<span>" + onu.rxPower + " dBm</span>"
                onus_html += "<td>" + onu.distance + "m</td>"
                if (onu.status === "active") {
                    onus_html += "<td class='text-green-500'>" + onu.uptime + "</td>"
                } else {
                    onus_html += "<td class='text-red-500'>" + onu.uptime + "</td>"
                }
                onus_html += '</tr>'
            }
        )
        ubiquiti_onus.append($(onus_html))
    });
}

function updateDasan() {
    let dasan_olt = $('#dasan_olt')
    let dasan_onus = $('#dasan_onus')

    dasan_olt.innerHTML = ""
    dasan_onus.innerHTML = ""

    let token = JSON.parse($.cookie('user')).acces_token
    let olt_html = ""
    fetch('http://ac-vision/api/v1.0/ressources/dasan/olt', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((olt) => {
        olt_html += "<td class='py-1.5'>" + olt.displayName + "</td>";
        olt_html += "<td class='whitespace-nowrap'>";
        if (olt.status === "active") {
            olt_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-green-500 uppercase text-green-500'>Connected</span>"
        } else {
            olt_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-red-500 uppercase text-red-500'>Disconnected</span>"
        }
        olt_html += "</td>"
        olt_html += "<td>" + olt.mac + "</td>"
        olt_html += "<td>" + olt.ip + "</td>"
        olt_html += "<td>" + olt.temperature + "°</td>"
        if (olt.status === "active") {
            olt_html += "<td class='text-green-500'>" + olt.uptime + "</td>"
        } else {
            olt_html += "<td class='text-red-500'>" + olt.uptime + "</td>"
        }
        dasan_olt.append($(olt_html))
    });

    let onus_html = ""
    onus_html += "<tr class='bg-gray-50'><th class='py-2 px-4'>Name</th><th class='py-2 px-4'>Status</th><th class='py-2 px-4'>Port</th><th class='py-2 px-4'>@MAC</th><th class='py-2 px-4'>IP</th><th class='py-2 px-4'>RxPower</th><th class='py-2 px-4'>Distance</th><th class='py-2 px-4'>Uptime</th></tr>";
    fetch('http://ac-vision/api/v1.0/ressources/dasan/onus', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((onus) => {
        onus.forEach((onu) => {
                onus_html += "<tr class='text-gray-800 text-sm'>"
                onus_html += "<td>" + onu.displayName + "</td>"
                onus_html += "<td class='whitespace-nowrap'>"
                if (onu.status === "active") {
                    onus_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-green-500 uppercase text-green-500'>Connected</span>"
                } else {
                    onus_html += "<span class='rounded-full text-xs px-2 py-1 border-2 border-red-500 uppercase text-red-500'>Disconnected</span>"
                }
                onus_html += "</td>"
                onus_html += "<td>GPON " + onu.port + "</td>"
                onus_html += "<td>" + onu.mac + "</td>"
                onus_html += "<td>" + onu.ip + "</td>"
                onus_html += "<td class='flex flex-row items-center justify-center space-x-1 py-1.5'>"
                if (onu.rxPower < -25) {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-red-300'>"
                    onus_html += "<div class='w-1/4 shadow-none whitespace-nowrap bg-red-600'></div>"
                } else if (onu.rxPower > -15) {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-green-300'>"
                    onus_html += "<div class='w-3/4 shadow-none whitespace-nowrap bg-green-600'></div>"
                } else {
                    onus_html += "<div class='overflow-hidden w-1/4 inline-block h-1 flex rounded bg-yellow-300'>"
                    onus_html += "<div class='w-1/2 shadow-none whitespace-nowrap bg-yellow-600'></div>"
                }
                onus_html += "</div>"
                onus_html += "<span>" + onu.rxPower + " dBm</span>"
                onus_html += "<td>" + onu.distance + "m</td>"
                if (onu.status === "active") {
                    onus_html += "<td class='text-green-500'>" + onu.uptime + "</td>"
                } else {
                    onus_html += "<td class='text-red-500'>" + onu.uptime + "</td>"
                }
                onus_html += '</tr>'
            }
        )
        dasan_onus.append($(onus_html))
    });
}

window.addEventListener('load', () => {
    updateUbiquiti();
    updateDasan();
    setInterval(updateUbiquiti, 60000)
    setInterval(updateDasan, 60000)
})