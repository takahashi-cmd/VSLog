// study_fields, study_logsの共通動作

function markDeleted(btn) {
    const row = btn.closest('tr');
    row.querySelector('input[name="row_action[]"]').value = 'delete';
    row.style.opacity = 0.5;
};
function removeRow(btn) {
    btn.closest('tr').remove();
}