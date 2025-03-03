const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const captureButton = document.getElementById("capture");
const recordButton = document.getElementById("record");
const gallery = document.getElementById("gallery");
const socket = io();

let mediaRecorder;
let recordedChunks = [];

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error("Errore webcam:", err));

captureButton.addEventListener("click", () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/png");

    // Effetto flash
    document.body.classList.add("flash");
    setTimeout(() => document.body.classList.remove("flash"), 300);

    fetch("/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.filename) {
            loadMedia();
        }
    })
    .catch(error => console.error("Errore upload:", error));
});

recordButton.addEventListener("click", () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        mediaRecorder = new MediaRecorder(video.srcObject);
        recordedChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: "video/webm" });
            const formData = new FormData();
            formData.append("file", blob, `video_${Date.now()}.webm`);

            fetch("/upload", {
                method: "POST",
                body: formData
            }).then(() => loadMedia());
        };

        mediaRecorder.start();
        video.classList.add("recording");
        recordButton.textContent = "Stop Registrazione";
    } else {
        mediaRecorder.stop();
        video.classList.remove("recording");
        recordButton.textContent = "Inizia Registrazione";
    }
});

function loadMedia() {
    fetch("/media")
        .then(response => response.json())
        .then(files => {
            gallery.innerHTML = "";
            files.forEach(file => {
                const ext = file.split('.').pop().toLowerCase();
                const container = document.createElement("div");
                container.classList.add("gallery-item");

                if (["png", "jpg", "jpeg", "gif"].includes(ext)) {
                    const imgElement = document.createElement("img");
                    imgElement.src = `/static/uploads/${file}`;
                    container.appendChild(imgElement);
                } else if (["mp4", "webm", "ogg"].includes(ext)) {
                    const videoElement = document.createElement("video");
                    videoElement.controls = true;
                    videoElement.src = `/static/uploads/${file}`;
                    container.appendChild(videoElement);
                }

                gallery.appendChild(container);
            });
        });
}

// Aggiorna la galleria quando un nuovo file viene caricato
socket.on("media_uploaded", () => {
    loadMedia();
});

loadMedia();
