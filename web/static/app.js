async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        
        if (!response.ok)
            throw new Error(`HTTP error! status: ${response.status}`);
        
        const stats = await response.json();
        console.log(stats)
        document.getElementById('files-processed').innerText = stats.metrics.processed || 0
        document.getElementById('files-success').innerText = stats.metrics.success || 0
        document.getElementById('files-failed').innerText = stats.metrics.failed || 0
    } catch (error) {
    } finally {
        setTimeout(updateDashboardStats, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateStats();
});