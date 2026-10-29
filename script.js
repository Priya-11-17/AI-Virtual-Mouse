async function startMouse() {

    const status = document.getElementById("status");
    const button = document.getElementById("startBtn");

    button.disabled = true;

    status.innerText = "Status: Starting...";

    try {

        const response = await fetch("/start", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message);
        }

        status.innerText = "Status: " + data.message;

    } catch (error) {

        status.innerText = "Error: " + error.message;

    } finally {

        button.disabled = false;

    }
}


async function stopMouse() {

    const status = document.getElementById("status");
    const button = document.getElementById("stopBtn");

    button.disabled = true;

    status.innerText = "Status: Stopping...";

    try {

        const response = await fetch("/stop", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message);
        }

        status.innerText = "Status: " + data.message;

    } catch (error) {

        status.innerText = "Error: " + error.message;

    } finally {

        button.disabled = false;

    }
}