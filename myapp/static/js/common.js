// 共通動作：ハンバーガーメニューの設定、空白行の削除

// ハンバーガーメニューの設定


// 空白行の削除
const removeRow = (btn) => {
    btn.closest('tr').remove();
    renumberRows();
}


