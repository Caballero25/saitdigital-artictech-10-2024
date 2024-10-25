document.addEventListener('DOMContentLoaded', () => {
    const fInput = document.getElementById('fileInput');
    const pBar = document.getElementById('progressBar');
    const pText = document.getElementById('progressText');
    const fName = document.getElementById('fileName');
    const modal = document.getElementById('myModal');
    const cModal = document.getElementById('closeModal');
    const pContainer = document.getElementById('previewContainer');
    const cBtn = document.getElementById('clearButton');
    const sendBtn = document.getElementById('sendFileButton');

    const prohibitedExtensions = ['.pdf', '.exe', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.doc', '.docx'];

    sendBtn.display = 'none';

    fInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (file && !prohibitedExtensions.includes(`.${fileExtension}`)) {
            const reader = new FileReader();
            reader.onloadstart = () => {
                pBar.style.width = '0%';
                pText.style.display = 'block';
                pText.innerText = '0%';
                pContainer.style.display = 'none';
                cBtn.style.display = 'none';
                sendBtn.style.display = 'none'
            };
            reader.onprogress = (event) => {
                if (event.lengthComputable) {
                    const progress = (event.loaded / event.total) * 100;
                    pBar.style.width = `${progress}%`;
                    pText.innerText = `${Math.round(progress)}%`;
                }
            };
            reader.onload = () => {
                const uploadTime = 3000;
                const interval = 10;
                const steps = uploadTime / interval;
                let currentStep = 0;
                const updateProgress = () => {
                    const progress = (currentStep / steps) * 100;
                    pBar.style.width = `${progress}%`;
                    pText.innerText = `${Math.round(progress)}%`;
                    currentStep++;

                    if (currentStep <= steps) {
                        setTimeout(updateProgress, interval);
                    } else {
                        pBar.style.width = '100%';
                        pText.innerText = '100%';
                        fName.innerText = `Nombre del archivo: ${file.name}`;
                        pContainer.innerHTML = `<p>Archivo cargado con éxito.</p>`;
                        pContainer.style.display = 'block';
                        cBtn.style.display = 'block';
                        sendBtn.style.display = 'block'
                    }
                };
                setTimeout(updateProgress, interval);
            };
            reader.readAsArrayBuffer(file); // read as binary file
        } else {
            alert('The selected file type is not allowed.');
            fInput.value = '';
        }
    });

    cModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    cBtn.addEventListener('click', () => {
        fInput.value = '';
        pBar.style.width = '0%';
        pText.style.display = 'none';
        fName.innerText = '';
        pContainer.style.display = 'none';
        cBtn.style.display = 'none';
        sendBtn.display = 'none'
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});