let mediaRecorder;
let audioChunks = [];

document.getElementById('startBtn').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = (e) => {
        audioChunks.push(e.data);
    };
    
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.mp3');
        
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        
        const audioUrl = URL.createObjectURL(await response.blob());
        const audioElement = document.getElementById('responseAudio');
        audioElement.src = audioUrl;
        audioChunks = [];
    };
    
    mediaRecorder.start();
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
});

document.getElementById('stopBtn').addEventListener('click', () => {
    mediaRecorder.stop();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
});



