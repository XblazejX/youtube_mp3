document.getElementById('downloadBtn').addEventListener('click', async () => {
    const urlInput = document.getElementById('url');
    const nameInput = document.getElementById('filename');
    const status = document.getElementById('status');

    const url = urlInput.value.trim();
    const filename = nameInput.value.trim();

    if (!url) {
        status.textContent = "⚠️ Wklej link do filmu!";
        return;
    }

    status.textContent = "⏳ Przetwarzanie...";

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ url, filename })
        });

        if (!response.ok) {
            const error = await response.json();
            status.textContent = "❌ Błąd: " + (error.error || "Nieznany błąd");
            return;
        }

        const blob = await response.blob();
        const contentDisposition = response.headers.get("Content-Disposition");
        const match = /filename\*=UTF-8''([^;]+)/.exec(contentDisposition) || /filename="?([^"]+)"?/.exec(contentDisposition);
        const downloadName = match ? decodeURIComponent(match[1]) : 'audio.webm';

        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = downloadName;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(downloadUrl);

        status.textContent = "✅ Gotowe!";
    } catch (e) {
        status.textContent = "❌ Błąd: " + e.message;
    }
});
