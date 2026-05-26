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

async function saveAccount() {
    const form = document.getElementById('accountForm');
    const formData = new FormData(form);
    
    const data = Object.fromEntries(formData.entries());

    const response = await fetch('/api/accounts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        closeModal();
        location.reload();
    } else {
        alert("Failed to save account.");
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

async function deleteAccount(id) {
    if (!confirm("Are you sure you want to delete this account?")) return;

    const response = await fetch(`/api/accounts/${id}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        location.reload(); // Refresh the page to remove the row
    } else {
        alert("Failed to delete account.");
    }
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