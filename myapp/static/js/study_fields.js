// study_fields（学習分野の登録・編集画面）の動作

function markDeleted(btn) {
    const row = btn.closest('tr');
    row.querySelector('input[name="row_action[]"]').value = 'delete';
    row.style.opacity = 0.5;
};
function removeRow(btn) {
    btn.closest('tr').remove();
}