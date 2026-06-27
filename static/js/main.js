// Sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const isOpen = sidebar.getAttribute('data-open') === 'true';
    if (isOpen) {
        sidebar.style.transform = 'translateX(-100%)';
        overlay.style.display = 'none';
        sidebar.setAttribute('data-open', 'false');
    } else {
        sidebar.style.transform = 'translateX(0)';
        overlay.style.display = 'block';
        sidebar.setAttribute('data-open', 'true');
    }
}

// My QRs Dropdown
function toggleQRDropdown() {
    const dropdown = document.getElementById('qrDropdown');
    const arrow = document.getElementById('qrArrow');
    const isHidden = dropdown.style.display === 'none' || dropdown.style.display === '';
    dropdown.style.display = isHidden ? 'flex' : 'none';
    arrow.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
}

// QR Image Modal
function openQR(imageUrl) {
    document.getElementById('qrImage').src = imageUrl;
    document.getElementById('qrModal').style.display = 'flex';
}

function closeQR() {
    document.getElementById('qrModal').style.display = 'none';
}

// Copy Short URL
function copyShort(id) {
    const text = document.getElementById(id).innerText.trim();
    navigator.clipboard.writeText(text);
}

// Short Code Edit Modal
function openShortEdit(qrId, currentCode) {
    document.getElementById('shortEditInput').value = currentCode;
    document.getElementById('shortEditForm').action = '/edit-qr/' + qrId + '/';
    document.getElementById('shortEditModal').style.display = 'flex';
}

function closeShortEdit() {
    document.getElementById('shortEditModal').style.display = 'none';
}

// Edit Short buttons via event delegation
document.addEventListener('click', function(e) {
    const btn = e.target.closest('.edit-short-btn');
    if (btn) {
        const qrId = btn.getAttribute('data-qrid');
        const code = btn.getAttribute('data-shortcode');
        openShortEdit(qrId, code);
    }
});
