let editingAccountId = null;

async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        
        if (!response.ok)
            throw new Error(`HTTP error! status: ${response.status}`);
        
        const stats = await response.json();
        document.getElementById('files-processed').innerText = stats.metrics.processed || 0
        document.getElementById('files-success').innerText = stats.metrics.success || 0
        document.getElementById('files-failed').innerText = stats.metrics.failed || 0
    } catch (error) {
    } finally {
        setTimeout(updateStats, 3000);
    }
}

let lastFetchedDate = null;
const seenTransactions = new Set();

let total = 0;
let success = 0;
let failed = 0;
let duplicate = 0;

async function loadTransactions() {
    try {
        let url = '/api/transactions';

        if (lastFetchedDate) {
            url += `?start_date=${encodeURIComponent(lastFetchedDate)}`;
        }

        const response = await fetch(url);

        if (!response.ok)
            throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();

        if (!data.length) return;

        const tbody = document.getElementById('uploads-tbody');

        for (let i = 0; i < data.length; i++) {
            const tx = data[i];

            if (seenTransactions.has(tx.id)) continue;
            seenTransactions.add(tx.id);

            let statusClass = '';
            let iconStatus = 'failed';
            let icon = '';

            if (tx.is_successful && !tx.is_duplicate) {
                statusClass = 'success-row';
                icon = 'fa-circle-check';
                iconStatus = 'success';
                success++;
            } else if (tx.is_duplicate) {
                statusClass = 'duplicate-row';
                icon = 'fa-circle-xmark';
                iconStatus = 'duplicate';
                duplicate++;
            } else if (tx.is_failed) {
                statusClass = 'failed-row';
                icon = 'fa-circle-xmark';
                iconStatus = 'failed';
                failed++;
            }

            const row = document.createElement('tr');
            row.classList.add(statusClass);
            row.classList.add('new-row');

            const amount = new Intl.NumberFormat('en-AU', {
                style: 'currency',
                currency: 'AUD'
            }).format(tx.amount);

            row.innerHTML = `
                <td>${tx.date}</td>
                <td>${tx.description}</td>
                <td>${amount}</td>
                <td>${mapped_accounts.find(a => a.id === tx.account_id)?.name || 'Unknown'}</td>
                <td class="status ${iconStatus}" title="${tx.message || ''}">
                    <i class="fa-solid ${icon}"></i>
                </td>
            `;

            tbody.prepend(row);

            total++;

            await new Promise(r => setTimeout(r, 120));
        }

        document.getElementById('uploads-total').innerText = total;
        document.getElementById('uploads-success').innerText = success;
        document.getElementById('uploads-failed').innerText = failed;
        document.getElementById('uploads-duplicate').innerText = duplicate;

        const newest = data.reduce((max, tx) => {
            return tx.created_at > max ? tx.created_at : max;
        }, lastFetchedDate || data[0].created_at);

        lastFetchedDate = newest;

    } catch (error) {
        console.error('Failed to load transactions', error);
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
    populateSureAccountNames();
    loadTransactions();
    loadAccountSync();

    setInterval(loadTransactions, 3000);
    setInterval(loadAccountSync, 10000);
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
var modal = document.getElementById("modal");
if(modal) {
    modal.addEventListener("click", function(e) {
        if (e.target === this) closeModal();
    });
}

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

let syncMap = {};

async function loadAccountSync() {
    try {
        const res = await fetch('/api/accounts-sync');

        if (!res.ok) throw new Error('Failed to load account sync');

        const data = await res.json();

        syncMap = Object.fromEntries(
            data.map(a => [String(a.account_id), a.last_synced_at])
        );

        renderSyncTimes();
    } catch (err) {
        console.error('account sync error', err);
    }
}

function populateSureAccountNames() {
    document
        .querySelectorAll(".sure-account-name")
        .forEach(el => {
            const id = String(el.dataset.sureAccountId);

            const account = allSureAccounts.find(
                a => String(a.id) === id
            );

            if (account) {
                el.textContent =
                    `${account.name} (${account.currency})`;
            } else {
                el.remove();
            }
        });
}

function formatLastSync(utcString) {
    if (!utcString) return "Never";

    const utcDate = new Date(utcString);
    const now = new Date();

    const diffMs = now - utcDate;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHr = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHr / 24);

    if (diffSec < 60) {
        return `${diffSec}s ago`;
    }

    if (diffMin < 60) {
        return `${diffMin}m ago`;
    }

    if (diffHr < 24) {
        return `${diffHr}h ago`;
    }

    if (diffDay === 1) {
        return "Yesterday";
    }

    return utcDate.toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function renderSyncTimes() {
    document.querySelectorAll("[data-account-id]").forEach(el => {
        const id = String(el.dataset.accountId);
        const utc = syncMap[id];

        el.textContent = formatLastSync(utc);
    });
}