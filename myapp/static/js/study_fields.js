// study_fieldsの動作

// 学習分野の新しい行の追加
const addRowFields = (btn) => {
    const table = document.getElementById('study-fields');
    const newRow = document.createElement('tr');
    const rowNum = table.rows.length
    newRow.innerHTML = `
    <td class="table-num">${rowNum}</td>
    <td><input type="text" name="fieldname[]" value=""></td>
    <td class="table-field-color"><input type="color" name="color_code[]" value="#000000"></td>
    <td>
    <input type="hidden" name="field_id[]" value="">
    <input type="hidden" name="row_action[]" value="new">
    <button class="delete-button" type="button" onclick="removeRow(this)">🗑️</button>
    </td>`;
    table.appendChild(newRow);
}
