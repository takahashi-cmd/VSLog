// study_logsの動作

// 日付を動的に表示
const dateInput = document.getElementById('study_date');
const studyDateForm = document.getElementById('study-date-form');
const selectedDate = document.querySelector('.study-date p');
console.log(selectedDate);
console.log(dateInput.value)

dateInput.addEventListener('change', () => {
    submitForm();
})

// 初回表示時に実行（GET時の学習記録を描画）
submitForm();

// FetchAPIによる非同期通信
function submitForm() {
    const formData = new FormData(studyDateForm);
    const jsonData = {};
    formData.forEach((value, key) => {
        console.log(value, key)
        jsonData[key] = value;
    })
    fetch(studyDateForm.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        selectedDate.textContent = `${data.selectedDate}の学習記録`;
        const studyLogsTbody = document.querySelector('.study-logs tbody');
        studyLogsTbody.textContent = '' // 前の日付のtemplateが残らないように初期化
        const studyLogsTemplate = document.getElementById('study-logs-template');
        const frag = document.createDocumentFragment();
        const defaultRowLength = 5

        // data.studyDictsがある場合の処理
        if (data.studyDicts) {
            // 既存行の表示
            for (let i = 0; i < data.studyDicts.length; i++) {
                // template要素の内容を複製
                const node = studyLogsTemplate.content.firstElementChild.cloneNode(true);
                // templateの内容を既存行に書き換え
                node.querySelector('.table-num').textContent = i + 1;
                node.querySelector('input[name="hours[]"]').value = data.studyDicts[i].hour.toFixed(1);
                node.querySelector('input[name="fieldname[]"]').value = data.studyDicts[i].fieldname;
                node.querySelector('textarea[name="contents[]"]').value = data.studyDicts[i].content;
                node.querySelector('input[name="study_dates[]"]').value = data.studyDicts[i].study_date;
                node.querySelector('input[name="study_log_id[]"]').value = data.studyDicts[i].study_log_id
                node.querySelector('input[name="row_action[]"]').value = 'update'
                // ボタン種類の書き換え（既存行削除の関数へ変更）
                const btn = node.querySelector('.delete-button');
                btn.removeAttribute('onclick');
                btn.addEventListener('click', () => markDeleted(btn));
                frag.appendChild(node);
            }
            // 空白行の表示（デフォルト5行表示）
            if (data.studyDicts.length < defaultRowLength) {
                for (let i = 0; i < defaultRowLength - data.studyDicts.length; i++) {
                    // template要素の内容を複製
                    const node = studyLogsTemplate.content.firstElementChild.cloneNode(true);
                    // templateの内容を空白行に書き換え
                    node.querySelector('.table-num').textContent = i + 1 + data.studyDicts.length;
                    node.querySelector('input[name="study_dates[]"]').value = data.selectedDate;
                    node.querySelector('input[name="row_action[]"]').value = 'new'
                    frag.appendChild(node);
                }
            }
        }
        // data.studyDictsが無い場合の処理
        else {
            for (let i = 0; i < defaultRowLength; i++) {
                // template要素の内容を複製
                const node = studyLogsTemplate.content.firstElementChild.cloneNode(true);
                // templateの内容を空白行に書き換え
                node.querySelector('.table-num').textContent = i + 1;
                node.querySelector('input[name="study_dates[]"]').value = data.selectedDate;
                node.querySelector('input[name="row_action[]"]').value = 'new'
                frag.appendChild(node);
            }
        }
        studyLogsTbody.appendChild(frag);
    })
}

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



