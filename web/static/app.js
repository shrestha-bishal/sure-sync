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


function openModal() {
    document.getElementById("modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

// Delete with animation
function deleteRow(btn) {
    const row = btn.closest(".account-row");

    row.classList.add("deleting");

    setTimeout(() => {
        row.remove();
    }, 250);
}

// click outside modal closes it
document.getElementById("modal").addEventListener("click", function(e) {
    if (e.target === this) closeModal();
});