let refreshInterval = null;
let currentFolderId = null;

function extractFolderId(url) {
    if (url.includes("folders/")) {
        return url.split("folders/")[1].split("?")[0];
    }
    return null;
}

async function importImages() {
    const folderUrl = document.getElementById("folderUrl").value;
    currentFolderId = extractFolderId(folderUrl);

    await fetch("https://image-api-t4am.onrender.com/import/google-drive", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ folder_url: folderUrl })
    });

    startAutoRefresh();
}

function startAutoRefresh() {
    if (refreshInterval) return;
    refreshInterval = setInterval(loadImages, 2000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

async function cancelImport() {
    await fetch("https://image-api-t4am.onrender.com/import/cancel", {
        method: "POST"
    });

    stopAutoRefresh();
}

function clearUI() {
    stopAutoRefresh();

    document.getElementById("gallery").innerHTML = "";
    document.getElementById("folderUrl").value = "";
    currentFolderId = null;
}

async function loadImages() {
    if (!currentFolderId) return;

    const res = await fetch(
        `https://image-api-t4am.onrender.com/images/${currentFolderId}`
    );

    const data = await res.json();

    const gallery = document.getElementById("gallery");
    gallery.innerHTML = "";

    data.images.forEach(img => {
        const image = document.createElement("img");
        image.src = img.storage_path;
        gallery.appendChild(image);
    });
}
