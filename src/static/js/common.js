// 共通動作：ハンバーガーメニューの設定、flashメッセージ、空白行の削除

// ハンバーガーメニューの設定
const modalHeader = (img) => {
    const menuIcon = img.closest('.menu-icon');
    const modalHeaderNav = menuIcon.querySelector('.modal-header-nav');
    const modalHeaderOverlay = menuIcon.querySelector('.modal-header-overlay');
    console.log(menuIcon);
    console.log(modalHeaderNav);
    console.log(modalHeaderOverlay);
    // 1.開く処理
    if (!modalHeaderNav.classList.contains('open')) {
        modalHeaderNav.classList.add('open');
        modalHeaderOverlay.classList.add('open');
        return;
    }
    // 2.閉じる処理
    if (modalHeaderNav.classList.contains('open')) {
        modalHeaderNav.classList.remove('open');
        modalHeaderOverlay.classList.remove('open');
        return;
    }
}

// ハンバーガーメニューを背景クリックで閉じる
document.addEventListener('click', (e) => {
    const overlay = e.target.closest('.modal-header-overlay');
    if (overlay && overlay.classList.contains('open')) {
        const menuIcon = overlay.closest('.menu-icon');
        const modalHeaderNav = menuIcon.querySelector('.modal-header-nav');
        modalHeaderNav.classList.remove('open');
        overlay.classList.remove('open');
    }
})

// flashメッセージの表示
const flashMessage = document.querySelectorAll('.message')
console.log(flashMessage);
flashMessage.forEach((message) => {
    setTimeout(() => {
        message.remove()
    }, 5000);
})

// 空白行の削除
const removeRow = (btn) => {
    btn.closest('tr').remove();
    renumberRows();
}


