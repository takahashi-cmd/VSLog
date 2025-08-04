// study_logsの動作

// 日付を動的に表示
document.addEventListener('DOMContentLoaded', () => {
    const dateInput = document.getElementById('study_date');
    const form = document.getElementById('study-date-form');

    dateInput.addEventListener('change', () => {
        form.submit();
    })
});

// 学習記録の新しい行の追加
const addRowLogs = (btn) => {
    const table = document.getElementById('study-logs');
    const newRow = document.createElement('tr');
    const rowNum = table.rows.length;
    const selected_date = document.getElementById('selected_date');
    const date = selected_date.dataset.selectedDate;

    newRow.innerHTML = `
    <td class="table-num">${rowNum}</td>
    <td><input type="number" step="0.1" min="0" max="24" name="hours[]" value=""></td>
    <td>
        <input type="text" name="fieldname[]" value="" list="field_list2">
    </td>
    <td><textarea name="contents[]"></textarea></td>
    <td>
        <input type="hidden" name="study_dates[]" value="${date}">
        <input type="hidden" name="study_log_id[]" value="">
        <input type="hidden" name="row_action[]" value="new">
        <button class="delete-button" type="button" onclick="removeRow(this)">🗑️</button>
    </td>`;
    table.appendChild(newRow);
}