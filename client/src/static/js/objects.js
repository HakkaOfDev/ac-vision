class DEVICE {
    constructor(type, displayName, macAddress, ipAddress, distance, rxPower, uptime, site, status, temperature, serialNumber, gponPort, profile) {
        this.type = type
        this.displayName = displayName
        this.macAddress = macAddress
        this.ipAddress = ipAddress
        this.distance = distance
        this.rxPower = rxPower
        this.uptime = uptime
        this.site = site
        this.status = status
        this.temperature = temperature
        this.gponPort = gponPort
        this.serialNumber = serialNumber
        this.profile = profile
        this.html = ""
    }

    appendPoint() {
        this.html += "<div class='point flex items-center justify-center'>"
        this.html += "<span class='block rounded-full bg-" + (this.status === "active" ? "green" : "red") + "-500 w-2 h-2'></span>"
        this.html += "</div>"
    }

    appendType() {
        this.html += "<div class='type justify-center'><img class='w-12 h-6' src='/static/img/models/" + this.type + ".png' alt></div>"
    }

    appendDisplayName() {
        this.html += "<div class='display-name'><span>" + this.displayName + "</span></div>"
    }

    appendStatus() {
        this.html += "<div class='status items-center'>"
        if (this.status === "active") {
            this.html += "<span class='rounded-full text-xxs py-0.5 px-1 border-2 border-green-500 uppercase text-green-500'>Connected</span>"
        } else {
            this.html += "<span class='rounded-full text-xxs py-0.5 px-1 border-2 border-red-500 uppercase text-red-500'>Disconnected</span>"
        }
        this.html += "</div>"
    }

    appendMacAddress() {
        this.html += "<div class='mac-address'><span>" + this.macAddress + "</span></div>"
    }

    appendIpAddress() {
        this.html += "<div class='ip-address'><span>" + (this.ipAddress !== null ? this.ipAddress : "") + "</a></div>"
    }

    appendSite() {
        this.html += "<div class='site'><span>" + this.site + "</span></div>"
    }

    appendUptime() {
        this.html += "<div class='uptime'>"
        if (this.status === "active") {
            this.html += "<span class='text-green-500'>" + this.uptime + "</span>"
        } else {
            this.html += "<span class='text-red-500'>" + this.uptime + "</span>"
        }
        this.html += "</div>"
    }

    appendTemperature() {
        this.html += "<div class='temperature'><span>" + (this.temperature !== null ? this.temperature + "°" : "") + "</span></div>"
    }

    appendSerialNumber() {
        this.html += "<div class='serial-number'><span>" + (this.serialNumber !== null ? this.serialNumber : "") + "</span></div>"
    }

    appendGponPort() {
        this.html += "<div class='gpon-port'><span>GPON " + (this.gponPort !== null ? this.gponPort : "") + "</span></div>"
    }

    appendProfile() {
        this.html += "<div class='profile'><span>" + (this.profile !== null ? this.profile : "") + "</span></div>"
    }

    appendDistance() {
        this.html += "<div class='distance'><span>" + (this.distance !== null ? this.distance + "m" : "") + "</span></div>"
    }

    appendRxPower() {
        this.html += "<div class='signal flex-row items-center justify-start space-x-2'>"
        if (this.rxPower !== null) {
            if (this.rxPower < -25) {
                this.html += "<div class='overflow-hidden w-1/4 inline-flex h-1.5 flex rounded bg-red-300'>"
                this.html += "<div class='w-1/4 shadow-none whitespace-nowrap bg-red-600'></div>"
            } else if (this.rxPower > -15) {
                this.html += "<div class='overflow-hidden w-1/4 inline-flex h-1.5 flex rounded bg-green-300'>"
                this.html += "<div class='w-3/4 shadow-none whitespace-nowrap bg-green-600'></div>"
            } else {
                this.html += "<div class='overflow-hidden w-1/4 inline-flex h-1.5 flex rounded bg-yellow-300'>"
                this.html += "<div class='w-1/2 shadow-none whitespace-nowrap bg-yellow-600'></div>"
            }
            this.html += "</div><span>" + this.rxPower + " dBm</span></div>"
        } else {
            this.html += "</div>"
        }
    }

    build() {
        this.html += "<div class='h-8 flex items-center text-sm space-x-4 border-b border-gray-300 border-solid'>"
        this.appendPoint()
        this.appendType()
        this.appendDisplayName()
        this.appendMacAddress()
        this.appendIpAddress()
        this.appendDistance()
        this.appendRxPower()
        this.appendUptime()
        this.appendSite()
        this.appendStatus()
        this.appendGponPort()
        this.appendSerialNumber()
        this.appendTemperature()
        this.appendProfile()
        this.html += "</div>"
        return $(this.html)
    }
}