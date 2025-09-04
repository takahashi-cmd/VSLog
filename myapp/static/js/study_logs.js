// study_logsの動作

// 日付を動的に表示
const dateInput = document.getElementById('study_date');
const form = document.getElementById('study-date-form');

dateInput.addEventListener('change', () => {
    form.submit();
})

    // 初回表示時にも実行（今日の学習記録を描画）
    // submitForm();

// 学習記録の新しい行の追加
const addRowLogs = (btn) => {
    const table = document.getElementById('study-logs');
    const newRow = document.createElement('tr');
    newRow.className = 'study-tr logs';
    const rowNum = table.rows.length;
    const selected_date = document.getElementById('selected_date');
    const date = selected_date.dataset.selectedDate;

    newRow.innerHTML = `
    <td class="table-num">${rowNum}</td>
    <td class="table-hour"><input type="number" step="0.1" min="0" max="24" name="hours[]" value=""></td>
    <td class="table-fieldname">
        <input type="text" name="fieldname[]" value="" list="field_list2">
    </td>
    <td class="table-content"><textarea name="contents[]" rows="" cols=""></textarea></td>
    <td class="table-delete">
        <input type="hidden" name="study_dates[]" value="${date}">
        <input type="hidden" name="study_log_id[]" value="">
        <input type="hidden" name="row_action[]" value="new">
        <button class="delete-button" type="button" onclick="removeRow(this)">🗑️</button>
    </td>`;
    table.appendChild(newRow);
}

// 既存行の削除
const markDeleted = (btn) => {
    const result = window.confirm('本当に学習記録を削除しますか？\n削除した場合、復元できません！')
    if (result) {
        const row = btn.closest('tr');
        row.querySelector('input[name="row_action[]"]').value = 'delete';
        document.forms['study_logs_process'].submit();
    }
};

// // FetchAPIによる非同期通信
// function submitForm() {
//     const formData = new FormData(form);
//     const jsonData = {};
//     formData.forEach((value, key) => {
//         jsonData[key] = value;
//     })
//     fetch(form.action, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(jsonData)
//     })
//     .then(response => response.json())
//     .then(data => {
        
//     }
// }

