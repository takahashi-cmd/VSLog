// study_logsの動作

// 日付を動的に表示
const dateInput = document.getElementById('study_date');
const studyDateForm = document.getElementById('study-date-form');
console.log(dateInput.value)

dateInput.addEventListener('change', () => {
    submitForm();
})

// FetchAPIによる非同期通信
function submitForm() {
    const formData = new FormData(studyDateForm);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    })
    fetch(studyDateForm.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.studyDicts) {
            console.log(data.studyDicts);
            
        //     data.studyDicts.forEach((dict) => {

        // })
        }
        else {
            console.log('データなし')
        }
    })
}

// 初回表示時にも実行（今日の学習記録を描画）
submitForm();

// 学習記録の新しい行の追加
const addRowLogs = (btn) => {
    const tableBody = document.querySelector('#study-logs tbody');
    const newRow = document.createElement('tr');
    newRow.classList.add('study-tr', 'logs');
    newRow.innerHTML = `
    <td class="table-num"></td>
    <td class="table-hour"><input type="number" step="0.1" min="0" max="24" name="hours[]" value=""></td>
    <td class="table-fieldname">
        <input type="text" name="fieldname[]" value="" list="field_list">
    </td>
    <td class="table-content"><textarea name="contents[]" rows="" cols=""></textarea></td>
    <td class="table-delete">
        <input type="hidden" name="study_dates[]" value="${dateInput.value}">
        <input type="hidden" name="study_log_id[]" value="">
        <input type="hidden" name="row_action[]" value="new">
        <button class="delete-button" type="button" onclick="removeRow(this)">🗑️</button>
    </td>`;
    tableBody.appendChild(newRow);

    // 追加後に番号を振り直す
    renumberRows();
}

// 番号の振り直し
const renumberRows = () => {
    const rows = document.querySelectorAll('#study-logs tbody tr.study-tr.logs');
    rows.forEach((row, index) => {
        const numCell = row.querySelector('.table-num');
        if (numCell) {
            numCell.textContent = index + 1
        }
    })
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



