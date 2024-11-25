const video = document.getElementById('video');
const markButton = document.getElementById('markButton');
const removeButton = document.getElementById('removeButton');
const saveButton = document.getElementById('saveButton');
const speedButton = document.getElementById('speedButton');
const timestampList = document.getElementById('timestampList');
const videoLoader = document.getElementById('videoLoader');
const videoUrlInput = document.getElementById('videoUrlInput');
const loadVideoButton = document.getElementById('loadVideoButton');
const controls = document.getElementById('controls');

// Get video URL from query parameters
const urlParams = new URLSearchParams(window.location.search);
const videoUrl = urlParams.get('video-url');

if (videoUrl) {
    loadVideo(videoUrl);
} else {
    videoLoader.style.display = 'block';
}

// Function to load the video
function loadVideo(url) {
    video.src = url;
    video.style.display = 'block';
    controls.style.display = 'block';
    videoLoader.style.display = 'none';
    timestamps = [{
        time: "00:00:00.000",
        frame: 0,
        signLanguage: false
    }];
    updateTimestampList();
}

// Event listener for the "Load Video" button
loadVideoButton.addEventListener('click', () => {
    const url = videoUrlInput.value.trim();
    if (url) {
        loadVideo(url);
    } else {
        alert('Bitte geben Sie eine gültige URL ein.');
    }
});

let timestamps = [{
    time: "00:00:00.000",
    frame: 0,
    signLanguage: false
}];

// Toggle state for playback speed
let isHalfSpeed = false;

// Function to toggle video speed between 0.5x and 1x
function toggleSpeed() {
    if (isHalfSpeed) {
        video.playbackRate = 1.0;
        speedButton.textContent = "1.0x";
    } else {
        video.playbackRate = 0.5;
        speedButton.textContent = "0.5x";
    }
    isHalfSpeed = !isHalfSpeed;
}

// Function to add a new timestamp
function addTimestamp() {
    const currentTime = video.currentTime;
    const formattedTime = formatTime(currentTime);

    const frameRate = getVideoFrameRate();
    const currentFrame = Math.floor(currentTime * frameRate);

    // Toggle signLanguage (alternates between true and false)
    const lastSignLanguage = timestamps[timestamps.length - 1].signLanguage;
    const newSignLanguage = !lastSignLanguage;

    const newEntry = {
        time: formattedTime,
        frame: currentFrame,
        signLanguage: newSignLanguage
    };

    timestamps.push(newEntry);
    updateTimestampList();
}

// Function to remove the last timestamp
function removeLastTimestamp() {
    if (timestamps.length > 1) {
        timestamps.pop();
        updateTimestampList();
    }
}

// Function to save timestamps as JSON
function saveTimestampsAsJSON() {
    const jsonData = JSON.stringify(timestamps, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'timestamps.json';
    a.click();
    URL.revokeObjectURL(url);
}

// Function to update the timestamp list in the DOM
function updateTimestampList() {
    // Clear existing timestamps
    timestampList.innerHTML = "";

    // Append each timestamp as a separate div
    timestamps.forEach((entry, index) => {
        const timestampItem = document.createElement('div');
        timestampItem.classList.add('timestamp-item');

        const timeInfo = document.createElement('span');
        timeInfo.textContent = `Zeit: ${entry.time}, Frame: ${entry.frame}, Sign Language: ${entry.signLanguage}`;

        // Remove button for individual timestamp
        const removeButton = document.createElement('button');
        removeButton.textContent = "Entfernen";
        removeButton.onclick = () => {
            if (index > 0) {
                timestamps.splice(index, 1);
                updateTimestampList();
            }
        };

        timestampItem.appendChild(timeInfo);
        timestampItem.appendChild(removeButton);
        timestampList.appendChild(timestampItem);
    });

    // Scroll to the last timestamp
    timestampList.scrollTop = timestampList.scrollHeight;
}

// Hotkey functionality
document.addEventListener('keydown', (event) => {
    if (event.key === 'a') { // Press "a" to add a timestamp
        addTimestamp();
    } else if (event.key === 'r') { // Press "r" to remove the last timestamp
        removeLastTimestamp();
    } else if (event.key === 's') { // Press "s" to save timestamps as JSON
        saveTimestampsAsJSON();
    } else if (event.key === 'x') { // Press "x" to toggle speed
        toggleSpeed();
    } else if (event.key === ' ') { // Press "Space" to play/pause the video
        if (video.paused) {
            video.play();
        } else {
            video.pause();
        }
    }
});

// Button event listeners for mouse click functionality
markButton.addEventListener('click', addTimestamp);
removeButton.addEventListener('click', removeLastTimestamp);
saveButton.addEventListener('click', saveTimestampsAsJSON);
speedButton.addEventListener('click', toggleSpeed);

// Helper function to format time as HH:MM:SS.MS
function formatTime(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 1000);
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
}

// Helper function to estimate video frame rate
function getVideoFrameRate() {
    const defaultFrameRate = 25;
    return defaultFrameRate;
}
