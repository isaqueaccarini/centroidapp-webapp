document.getElementById('form-kmeans').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const loader = document.getElementById('loader');
    
    const imgOriginal = document.getElementById('img-original');
    const imgClusters = document.getElementById('img-clusters');
    const imgMetrics = document.getElementById('img-metrics');
    const imgMovement = document.getElementById('img-movement');
    const execLog = document.getElementById('exec-log');
    const btnDownloadZip = document.getElementById('btn-download-zip');
    
    const resultsContainer = document.getElementById('results-container');

    loader.classList.remove('d-none');
    formcont.classList.add('d-none')
    resultsContainer.classList.add('d-none');

    fetch('/exec_kmeans', {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error");
        }
        return response.json();
    })
    .then(data => {
        imgOriginal.src = "data:image/png;base64," + data.original_image_b64;
        imgClusters.src = "data:image/png;base64," + data.clusters_image_b64;
        imgMetrics.src = "data:image/png;base64," + data.metrics_image_b64;
        imgMovement.src = "data:image/png;base64," + data.movement_image_b64;
        
        execLog.textContent = data.log_info;
        
        btnDownloadZip.href = "data:application/zip;base64," + data.zip_bytes_b64;
        btnDownloadZip.download = "kmeans_package.zip";
        
        resultsContainer.classList.remove('d-none');
        loader.classList.add('d-none');
    })
    .catch(error => {
        console.error("Request Error:", error);
        alert("An error has occurred processing the model. Please try again");
        loader.classList.add('d-none');
        window.location.href = '/';
    });
});