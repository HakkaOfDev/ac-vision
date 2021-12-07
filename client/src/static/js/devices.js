let ubiquitiHandler = $("#ubiquiti-handler")
let dasanHandler = $("#dasan-handler")

ubiquitiHandler.click((event) => {
    ubiquitiHandler.toggleClass('active')
    let ubiquitiContainer = $("#ubiquiti-container")
    if (ubiquitiContainer.css("display") === "flex") {
        ubiquitiContainer.css("display", "none")
    } else {
        ubiquitiContainer.css("display", "flex")
    }
})


dasanHandler.click((event) => {
    dasanHandler.toggleClass('active')
    let dasanContainer = $("#dasan-container")
    if (dasanContainer.css("display") === "flex") {
        dasanContainer.css("display", "none")
    } else {
        dasanContainer.css("display", "flex")
    }
})

async function getUbiquitiDevices() {
    let ubiquitiDevices = $('#ubiquiti-devices')

    const token = JSON.parse($.cookie('user')).access_token
    $.ajax({
        type: "GET", url: "http://ac-vision/api/v1.0/ressources/ubiquiti/olt", dataType: 'json', headers:
            {
                'Authorization': 'Bearer ' + token
            }, success: (olt) => {
            let device = new DEVICE("olt-ubiquiti", olt.displayName, olt.macAddress, olt.ipAddress, null, null, olt.uptime, olt.site.name, olt.status, olt.temperature, null, null, null)
            ubiquitiDevices.append(device.build());
        }
    });
    $.ajax({
        type: "GET", url: "http://ac-vision/api/v1.0/ressources/ubiquiti/onus", dataType: 'json', headers:
            {
                'Authorization': 'Bearer ' + token
            }, success: (onus) => {
            onus.forEach((onu) => {
                let device = new DEVICE("onu-ubiquiti", onu.displayName, onu.macAddress, onu.ipAddress, onu.distance, onu.rxPower, onu.uptime, onu.site.name, onu.status, null, onu.serialNumber, onu.gponPort, onu.profile)
                ubiquitiDevices.append(device.build());
            });
        }
    });
}

async function getDasanDevices() {
    let dasanDevices = $('#dasan-devices')

    const token = JSON.parse($.cookie('user')).access_token
    $.ajax({
        type: "GET", url: "http://ac-vision/api/v1.0/ressources/dasan/olt", dataType: 'json', headers:
            {
                'Authorization': 'Bearer ' + token
            }, success: (olt) => {
            let device = new DEVICE("olt-dasan", olt.displayName, olt.macAddress, olt.ipAddress, null, null, olt.uptime, olt.site.name, olt.status, olt.temperature, null, null, null)
            dasanDevices.append(device.build());
        }
    });
    $.ajax({
        type: "GET", url: "http://ac-vision/api/v1.0/ressources/dasan/onus", dataType: 'json', headers:
            {
                'Authorization': 'Bearer ' + token
            }, success: (onus) => {
            onus.forEach((onu) => {
                let device = new DEVICE("onu-dasan", onu.displayName, onu.macAddress, onu.ipAddress, onu.distance, onu.rxPower, onu.uptime, onu.site.name, onu.status, null, onu.serialNumber, onu.gponPort, onu.profile)
                dasanDevices.append(device.build());
            });
        }
    });
}

window.addEventListener('load', () => {
    getDasanDevices()
    getUbiquitiDevices()
})