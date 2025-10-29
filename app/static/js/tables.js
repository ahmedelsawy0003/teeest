export function filterTable(tableId, query) {
    const table = document.getElementById(tableId);
    if (!table) {
        return;
    }
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.style.display = row.textContent.includes(query) ? '' : 'none';
    });
}
