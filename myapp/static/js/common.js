// 共通動作：行の削除、モータルウィンドウの開閉、ハンバーガーメニューの開閉、エラーメッセージの表示・自動削除等

// 空白行の削除
const removeRow = (btn) => {
    btn.closest('tr').remove();
}


