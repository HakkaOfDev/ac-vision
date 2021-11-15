let network = null;
const container = document.getElementById("myworkflow");

function popupContainer(text) {
    const container = document.createElement("div");
    container.classList.add("bg-blue-900", "text-gray-100", "text-sm", "p-2");
    container.innerHTML = text;
    return container;
}

function destroy() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
}

function draw() {
    destroy()

    const options = {
        autoResize: true,
        clickToUse: false,
        height: '100%',
        width: '100%',
        layout: {
            hierarchical: {
                enabled: true,
                direction: "UD",
                sortMethod: "directed",
                blockShifting: true,
                edgeMinimization: true
            },
        },
        interaction: {
            zoomView: false
        }
    };

    let edges = [];
    let nodes = [];

    // FAI
    nodes.push(
        {
            id: 0,
            label: "FAI",
            shape: "image",
            image: "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
            font: {
                strokeWidth: 3
            }
        }
    )

    let token = JSON.parse($.cookie('user')).acces_token

    fetch('http://ac-vision/api/v1.0/ressources/ubiquiti/olt', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((olt) => {
        nodes.push(
            {
                id: 2,
                label: olt.displayName,
                shape: "image",
                image: "/static/img/models/olt-ubiquiti.png",
                font: {
                    strokeWidth: 3
                },
                title: popupContainer(
                    "Name: <span class='text-yellow-400'>" + olt.displayName + "</span><br>" +
                    "MAC: <span class='text-yellow-400'>" + olt.mac + "</span><br>" +
                    "IP: <span class='text-yellow-400'>" + olt.ip + "</span><br>" +
                    "Uptime: <span class='text-yellow-400'>" + olt.uptime + "</span><br>" +
                    "Temperature: <span class='text-yellow-400'>" + olt.temperature + "°</span><br>" +
                    "Site: <span class='text-yellow-400'>" + olt.site.name + "</span><br>"
                ),
            }
        )
        edges.push(
            {
                from: 0,
                to: 2,
                color: olt.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                length: 25,
                title: popupContainer(
                    olt.status === "active" ?
                        "Status: <span class='text-green-500'>" + olt.status + "</span>" : "Status: <span class='text-red-500'>" + olt.status + "</span>"
                )
            }
        )
    });

    // UBIQUITI ONUS
    let i = 10;
    fetch('http://ac-vision/api/v1.0/ressources/ubiquiti/onus', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((onus) => {
        onus.forEach((onu) => {
            nodes.push(
                {
                    id: i,
                    label: onu.displayName,
                    shape: "image",
                    image: "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
                    font: {
                        strokeWidth: 3
                    },
                    title: popupContainer(
                        "Name: <span class='text-yellow-400'>" + onu.displayName + "</span><br>" +
                        "SerialNumber: <span class='text-yellow-400'>" + onu.serialNumber + "</span><br>" +
                        "Port: <span class='text-yellow-400'>" + onu.port + "</span><br>" +
                        "MAC: <span class='text-yellow-400'>" + onu.mac + "</span><br>" +
                        "IP: <span class='text-yellow-400'>" + onu.ip + "</span><br>" +
                        "Uptime: <span class='text-yellow-400'>" + onu.uptime + "</span><br>" +
                        "Distance: <span class='text-yellow-400'>" + onu.distance + "m</span><br>" +
                        "Site: <span class='text-yellow-400'>" + onu.site.name + "</span><br>"
                    ),
                });
            edges.push(
                {
                    from: 2,
                    to: i,
                    color: onu.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                    length: 325,
                    label: "" + parseInt(onu.rxPower) + " dBm",
                    title: popupContainer(
                        onu.status === "active" ?
                            "Status: <span class='text-green-500'>" + onu.status + "</span><br>RxPower: <span class='text-green-500'>" + onu.rxPower + " dBm</span>" :
                            "Status: <span class='text-red-500'>" + onu.status + "</span><br>RxPower: <span class='text-red-500'>" + onu.rxPower + " dBm</span>"
                    ),
                }
            );
            i++;
        })
    })

    fetch('http://ac-vision/api/v1.0/ressources/dasan/olt', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((olt) => {
        nodes.push(
            {
                id: 1,
                label: olt.displayName,
                shape: "image",
                image: "/static/img/models/olt-dasan.png",
                font: {
                    strokeWidth: 3
                },
                title: popupContainer(
                    "Name: <span class='text-yellow-400'>" + olt.displayName + "</span><br>" +
                    "MAC: <span class='text-yellow-400'>" + olt.mac + "</span><br>" +
                    "IP: <span class='text-yellow-400'>" + olt.ip + "</span><br>" +
                    "Uptime: <span class='text-yellow-400'>" + olt.uptime + "</span><br>" +
                    "Temperature: <span class='text-yellow-400'>" + olt.temperature + "°</span><br>" +
                    "Site: <span class='text-yellow-400'>" + olt.site.name + "</span><br>"
                ),
            }
        )
        edges.push(
            {
                from: 0,
                to: 1,
                color: olt.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                length: 25,
                title: popupContainer(
                    olt.status === "active" ?
                        "Status: <span class='text-green-500'>" + olt.status + "</span>" : "Status: <span class='text-red-500'>" + olt.status + "</span>"
                )
            }
        )
    });

    // DASAN ONUS
    let x = 100;
    fetch('http://ac-vision/api/v1.0/ressources/dasan/onus', {
        headers: {
            'Accept': 'application/json', 'Authorization': 'Bearer ' + token
        }
    }).then((response) => {
        return response.json()
    }).then((onus) => {
        onus.forEach((onu) => {
            nodes.push(
                {
                    id: x,
                    label: onu.displayName,
                    shape: "image",
                    image: "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
                    font: {
                        strokeWidth: 3
                    },
                    title: popupContainer(
                        "Name: <span class='text-yellow-400'>" + onu.displayName + "</span><br>" +
                        "Port: <span class='text-yellow-400'>" + onu.port + "</span><br>" +
                        "MAC: <span class='text-yellow-400'>" + onu.mac + "</span><br>" +
                        "IP: <span class='text-yellow-400'>" + onu.ip + "</span><br>" +
                        "Uptime: <span class='text-yellow-400'>" + onu.uptime + "</span><br>" +
                        "Distance: <span class='text-yellow-400'>" + onu.distance + "m</span><br>" +
                        "Site: <span class='text-yellow-400'>" + onu.site.name + "</span><br>"
                    ),
                });
            edges.push(
                {
                    from: 1,
                    to: x,
                    color: onu.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                    length: 325,
                    label: "" + parseInt(onu.rxPower) + " dBm",
                    title: popupContainer(
                        onu.status === "active" ?
                            "Status: <span class='text-green-500'>" + onu.status + "</span><br>RxPower: <span class='text-green-500'>" + onu.rxPower + " dBm</span>" :
                            "Status: <span class='text-red-500'>" + onu.status + "</span><br>RxPower: <span class='text-red-500'>" + onu.rxPower + " dBm</span>"
                    ),
                }
            );
            x++;
        })

        const data = {
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(edges),
        };

        network = new vis.Network(container, data, options);
    })
}

window.addEventListener('load', () => {
    draw();
    setInterval(draw, 60000);
});