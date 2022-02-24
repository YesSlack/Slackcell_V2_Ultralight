let id_max_force = document.getElementById('max_force')
let id_force = document.getElementById('force')
let id_current_draw = document.getElementById('current_draw')
let id_pi_temp = document.getElementById('pi_temp')
let id_pi_load = document.getElementById('pi_load')
let id_pi_disk = document.getElementById('pi_disk')

let id_sampling_rate = document.getElementById("sampling_rate")

function update_force() {
    if (force.length > 0) {
        id_force.innerHTML = force.slice(-1)[0].toFixed(2);
    }
}

function update_max_force() {
    get_api("/max_force").then(val => {
        id_max_force.innerHTML = (val / 1000).toFixed(2)
    });
}

function record_start() {
    get_api("/record_start").then(
        response => {
            let data = JSON.parse(response);
            // let success = data[0]
            let recording = data[1]
            if (recording) {
                document.getElementById('btn_record_start').style.backgroundColor = "red";
            } else {
                document.getElementById('btn_record_start').style.backgroundColor = "#333";
            }
        }
    )
}

function record_stop() {
    get_api("/record_stop").then(
        response => {
            let data = JSON.parse(response);
            let success = data[0][0]
            let recording = data[0][1]
            let csv = data[1]
            if (recording) {
                document.getElementById('btn_record_start').style.backgroundColor = "red";
            } else {
                document.getElementById('btn_record_start').style.backgroundColor = "#333";
            }
            if (success) {
                let recordings = document.getElementById('recordings');
                let entry = document.createElement('li');
                entry.classList.add("list-group-item");
                let anchor = document.createElement("a");
                anchor.textContent = csv;
                anchor.setAttribute('href', "/static/data/" + csv);
                entry.appendChild(anchor);
                recordings.appendChild(entry);
            }
        }
    )
}

function reset_max_force() {
    get_api("/reset_max_force").then(val => {
        id_max_force.innerHTML = val
    });
}

function update_sampling_rate() {
    if (sampling_rate) {
        id_sampling_rate.innerHTML = (1 / sampling_rate).toFixed(1) + " Hz, " + sampling_rate.toFixed(4);
    } else {
        id_sampling_rate.innerHTML = "- Hz, - "
    }
}


let interval_force = setInterval(update_force, 100);
let interval_sampling_rate = setInterval(update_sampling_rate, 100);

let timestamp = [];
let force = [];
let sampling_rate;
let start_time = 0;
let update_rate = 80 / 8;
let storage_time = 10 * update_rate;

const evtSource = new EventSource("/listen");
evtSource.onmessage = function (event) {
    let _data = event.data.split(',')
    timestamp.push(Number(_data[0]) - start_time)
    force.push(Number(_data[1] / 1000))
    if (timestamp.length === 1) {
        start_time = timestamp[0];
        timestamp[0] = 0
    }
    sampling_rate = Number(_data[2])
    let n = force.length
    if (n > storage_time) {
        timestamp = timestamp.slice(n - storage_time)
        force = force.slice(n - storage_time)
    }
    evtSource.addEventListener("max_force", function (event) {
        id_max_force.innerHTML = (event.data / 1000).toFixed(2)
    });
    evtSource.addEventListener("pixels", function (event) {
        let i;
        const data = JSON.parse(event.data);
        for (i = 0; i < pixels.length; i++) {
            pixels[i].style.backgroundColor = data[i];
        }
    });
    evtSource.addEventListener("pi_stats", function (event) {
        const data = JSON.parse(event.data);
        id_pi_temp.innerHTML = data.pi_temp;
        id_pi_load.innerHTML = data.pi_load;
        id_pi_disk.innerHTML = data.pi_disk;
    });
    // sampling_rate.innerHTML = (x[n - 1] - x[n - 2]).toFixed(4)
}

update_max_force();
