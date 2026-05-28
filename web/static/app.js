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
        total += data.length;

        const tbody = document.getElementById('uploads-tbody');

        data.forEach(tx => {
            console.log('New transaction:', tx);
            const row = document.createElement('tr');

            let statusClass = '';
            let iconStatus = 'failed';
            let icon = '';

            if(tx.is_successful && !tx.is_duplicate) {
                statusClass = 'success-row';
                icon = 'fa-circle-check';
                iconStatus = 'success';
                success++;
            } else if(tx.is_duplicate) {
                statusClass = 'duplicate-row';
                icon = 'fa-circle-xmark';
                duplicate++;
            } else if(tx.is_failed) {
                statusClass = 'failed-row';
                icon = 'fa-circle-xmark';
                failed++;
            }

            row.className = statusClass;

            const amount = new Intl.NumberFormat('en-AU', {
                style: 'currency',
                currency: 'AUD'
            }).format(tx.amount);

            row.innerHTML = `
                <td>${tx.date}</td>
                <td>${tx.description}</td>
                <td>${amount}</td>
                <td>${tx.account}</td>
                <td class="status ${iconStatus}" title="${tx.message}">
                    <i class="fa-solid ${icon}"></i>
                </td>
            `;

            tbody.prepend(row);

            document.getElementById('uploads-total').innerText = total;
            document.getElementById('uploads-success').innerText = success;
            document.getElementById('uploads-failed').innerText = failed;
            document.getElementById('uploads-duplicate').innerText = duplicate;
        });

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

    setInterval(loadTransactions, 3000);
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