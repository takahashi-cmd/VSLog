// 共通動作：行の削除、モータルウィンドウの開閉、ハンバーガーメニューの開閉、エラーメッセージの表示・自動削除等

// 既存行の削除
const markDeleted = (btn) => {
    const row = btn.closest('tr');
    row.querySelector('input[name="row_action[]"]').value = 'delete';
    row.style.opacity = 0.5;
};

// 空白行の削除
const removeRow = (btn) => {
    btn.closest('tr').remove();
}


