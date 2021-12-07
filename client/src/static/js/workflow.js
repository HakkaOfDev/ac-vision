function popupContainer(text) {
    const container = document.createElement("div");
    container.classList.add("bg-blue-900", "text-gray-100", "text-sm", "p-2");
    container.innerHTML = text;
    return container;
}

function mainContainer(displayName, macAddress, ipAddress, uptime, temperature, site) {
    return popupContainer("Name: <span class='text-yellow-400'>" + displayName + "</span><br>" +
        "MAC: <span class='text-yellow-400'>" + macAddress + "</span><br>" +
        "IP: <span class='text-yellow-400'>" + ipAddress + "</span><br>" +
        "Uptime: <span class='text-yellow-400'>" + uptime + "</span><br>" +
        "Temperature: <span class='text-yellow-400'>" + temperature + "°</span><br>" +
        "Site: <span class='text-yellow-400'>" + site + "</span><br>");
}

function subContainer(displayName, serialNumber, gponPort, macAddress, ipAddress, uptime, distance, site) {
    return popupContainer("Name: <span class='text-yellow-400'>" + displayName + "</span><br>" +
        "SerialNumber: <span class='text-yellow-400'>" + serialNumber + "</span><br>" +
        "Port: <span class='text-yellow-400'>" + gponPort + "</span><br>" +
        "MAC: <span class='text-yellow-400'>" + macAddress + "</span><br>" +
        "IP: <span class='text-yellow-400'>" + ipAddress + "</span><br>" +
        "Uptime: <span class='text-yellow-400'>" + uptime + "</span><br>" +
        "Distance: <span class='text-yellow-400'>" + distance + "m</span><br>" +
        "Site: <span class='text-yellow-400'>" + site + "</span><br>");
}

function linkContainer(status) {
    return popupContainer("Status: <span class='text-" + (status === "active" ? "green" : "red") + "-500'>" + status + "</span>");
}

class Workflow {
    network = null
    nodes = new vis.DataSet([])
    edges = new vis.DataSet([])

    constructor(container) {
        this.container = container
        this.configure()
    }

    create() {
        let data = {
            nodes: this.nodes,
            edges: this.edges
        };

        this.network = new vis.Network(this.container, data, this.options);
    }

    configure() {
        this.options = {
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
                zoomSpeed: 0.5,
                zoomView: true
            }
        };
    }

    addNode(node) {
        this.nodes.add(node)
    }

    addEdge(edge) {
        this.edges.add(edge)
    }

    updateData() {
        let authToken = JSON.parse($.cookie('user')).access_token
        // RT-STACK
        $.ajax({
            type: "GET", url: "http://ac-vision/api/v1.0/ressources/rt-stack", dataType: 'json', headers:
                {
                    'Authorization': 'Bearer ' + authToken
                }, success: (rtStack) => {
                this.nodes.update([{
                    id: 1,
                    label: rtStack.displayName,
                    shape: "image",
                    image: "/static/img/models/rt-stack.png",
                    font: {
                        strokeWidth: 3
                    },
                    title: mainContainer(rtStack.displayName, rtStack.macAddress, rtStack.ipAddress, rtStack.uptime, rtStack.temperature, rtStack.site.name)
                }]);
                this.edges.update([{
                    from: 0,
                    to: 1,
                    color: rtStack.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                    length: 25,
                    title: linkContainer(rtStack.status)
                }]);
            }
        });

        // OLT DASAN
        $.ajax({
            type: "GET", url: "http://ac-vision/api/v1.0/ressources/dasan/olt", dataType: 'json', headers:
                {
                    'Authorization': 'Bearer ' + authToken
                }, success: (olt) => {
                this.nodes.update([{
                    id: 2,
                    label: olt.displayName,
                    shape: "image",
                    image: "/static/img/models/olt-dasan.png",
                    font: {
                        strokeWidth: 3
                    },
                    title: mainContainer(olt.displayName, olt.macAddress, olt.ipAddress, olt.uptime, olt.temperature, olt.site.name)
                }]);
                this.edges.update([{
                    from: 1,
                    to: 2,
                    color: olt.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                    length: 25,
                    title: linkContainer(olt.status)
                }]);
            }
        });

        // OLT UBIQUITI
        $.ajax({
            type: "GET", url: "http://ac-vision/api/v1.0/ressources/ubiquiti/olt", dataType: 'json', headers:
                {
                    'Authorization': 'Bearer ' + authToken
                }, success: (olt) => {
                this.nodes.update([{
                    id: 3,
                    label: olt.displayName,
                    shape: "image",
                    image: "/static/img/models/olt-ubiquiti.png",
                    font: {
                        strokeWidth: 3
                    },
                    title: mainContainer(olt.displayName, olt.macAddress, olt.ipAddress, olt.uptime, olt.temperature, olt.site.name)
                }])
                this.edges.update([
                    {
                        from: 1,
                        to: 3,
                        color: olt.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                        length: 25,
                        title: linkContainer(olt.status)
                    }])
            }
        });
        let i = 4;
        // UBIQUITI ONUS
        $.ajax({
            type: "GET", url: "http://ac-vision/api/v1.0/ressources/ubiquiti/onus", dataType: 'json', headers:
                {
                    'Authorization': 'Bearer ' + authToken
                }, success: (onus) => {
                onus.forEach((onu) => {
                    this.nodes.update([{
                        id: i,
                        label: onu.displayName,
                        shape: "image",
                        image: "/static/img/models/onu-ubiquiti.png",
                        font: {
                            strokeWidth: 3
                        },
                        title: subContainer(onu.displayName, onu.serialNumber, onu.gponPort, onu.macAddress, onu.ipAddress, onu.uptime, onu.distance, onu.site.name)
                    }])
                    this.edges.update([
                        {
                            from: 3,
                            to: i,
                            color: onu.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                            length: 25,
                            title: linkContainer(onu.status)
                        }])
                    i++;
                })
            }
        });

        // DASAN ONUS
        $.ajax({
            type: "GET", url: "http://ac-vision/api/v1.0/ressources/dasan/onus", dataType: 'json', headers:
                {
                    'Authorization': 'Bearer ' + authToken
                }, success: (onus) => {
                onus.forEach((onu) => {
                    this.nodes.update([{
                        id: i,
                        label: onu.displayName,
                        shape: "image",
                        image: "/static/img/models/onu-dasan.png",
                        font: {
                            strokeWidth: 3
                        },
                        title: subContainer(onu.displayName, onu.serialNumber, onu.gponPort, onu.macAddress, onu.ipAddress, onu.uptime, onu.distance, onu.site.name)
                    }])
                    this.edges.update([
                        {
                            from: 2,
                            to: i,
                            color: onu.status === "active" ? "rgba(16, 185, 129, 1)" : "rgba(239, 68, 68, 1)",
                            length: 25,
                            title: linkContainer(onu.status)
                        }])
                    i++;
                })
            }
        });
    }

    addCloud() {
        this.addNode({
            id: 0,
            shape: "image",
            image: "/static/img/models/cloud.png",
        })
    }

    destroy() {
        if (this.network !== null) {
            this.network.destroy();
            this.network = null;
            this.nodes = null;
            this.edges = null;
        }
    }
}

window.addEventListener('load', () => {
    const container = document.getElementById("myworkflow");
    let workflow = new Workflow(container)
    workflow.create()
    workflow.addCloud()
    workflow.updateData()
    setInterval(workflow.updateData, 10000);
});