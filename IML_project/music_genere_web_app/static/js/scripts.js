document.getElementById('customFile').addEventListener('change', function(event) {
    const audioPlayer = document.getElementById('audioPlayer');
    const fileInput = event.target;

    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        const audioFile = URL.createObjectURL(fileInput.files[0]);
        audioPlayer.src = audioFile;
        audioPlayer.load();

        document.querySelector('.custom-file-label').innerText = fileName;
    } else {
        audioPlayer.src = '';
        document.querySelector('.custom-file-label').innerText = 'Choose file';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const predictedGenreLabel = document.getElementById('predictedGenreLabel');
        const predictedGenre = document.getElementById('predictedGenre');

        if (data.hasOwnProperty('genre')) {
            predictedGenre.innerText = data.genre;
            if (data.genre.trim() !== '') {
                predictedGenreLabel.style.display = 'block';
            }
        } else if (data.hasOwnProperty('error')) {
            console.error('Server Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});
