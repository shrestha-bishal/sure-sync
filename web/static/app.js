let editingAccountId = null;

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

    const isEditing = editingAccountId !== null;

    const response = await fetch(
        isEditing
            ? `/api/accounts/${editingAccountId}`
            : '/api/accounts',
        {
            method: isEditing ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    );

    if (response.ok) {
        closeModal();
        location.reload();
    } else {
        alert(
            isEditing
                ? "Failed to update account."
                : "Failed to save account."
        );
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateStats();
});


function openModal() {
    editingAccountId = null;
    document.getElementById("modal").style.display = "flex";
    document.querySelector(".modal-header").innerText = "Add Account";
    document.getElementById("accountForm").reset();
    populateSureAccounts();
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

async function editAccount(id) {
    const response = await fetch(`/api/accounts/${id}`);

    if (!response.ok) {
        alert("Failed to load account.");
        return;
    }

    const account = await response.json();

    editingAccountId = id;

    const form = document.getElementById("accountForm");
    populateSureAccounts(account.sure_account_id);
    form.bank_name.value = account.bank_name || "";
    form.bank_id.value = account.bank_id || "";
    form.account_name.value = account.account_name || "";
    form.account_id.value = account.account_id || "";
    form.notes.value = account.notes || "";

    document.querySelector(".modal-header").innerText = "Edit Account";
    document.getElementById("modal").style.display = "flex";
}

function populateSureAccounts(selectedId = null) {
    const select = document.querySelector('[name="sure_account_id"]');

    select.innerHTML = `
        <option value="" disabled selected hidden>
            Mapped Sure Account
        </option>
    `;

    allSureAccounts.forEach(account => {
        const isMapped = mappedSureAccountIds.includes(String(account.id));

        if (!isMapped || String(account.id) === String(selectedId)) {
            const option = document.createElement("option");

            option.value = account.id;

            option.textContent =
                `${account.name} (${account.currency}) ` +
                `[${account.classification}/${account.account_type}]`;

            select.appendChild(option);
        }
    });

    if (selectedId) {
        select.value = String(selectedId);
    }
}