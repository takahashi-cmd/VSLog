// index.htmlのグラフ切替時の動作

const periodForm = document.getElementById('periodForm');
const period = document.getElementById('period');
const horizontalAxisForm = document.getElementById('horizontalAxisForm');
const horizontalAxis = document.getElementById('horizontalAxis');
const verticalAxisForm = document.getElementById('verticalAxisForm');
const verticalAxis = document.getElementById('verticalAxis');

// プルダウン変更時にフォームの自動送信
period.addEventListener('change', () => {
    periodForm.submit();
});

horizontalAxis.addEventListener('change', () => {
    horizontalAxisForm.submit();
});

verticalAxis.addEventListener('change', () => {
    verticalAxisForm.submit();
})

