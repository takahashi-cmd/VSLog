// index.htmlのグラフ切替時の動作

// プルダウンメニュー選択時に自動でformを送信
document.addEventListener('DOMContentLoaded', () => {
    const graphForm = document.getElementById('graphForm');
    const periodSelect = document.getElementById('period');
    const yearContainer= document.getElementById('year-container')
    const monthContainer = document.getElementById('month-container')
    const yearSelect = document.getElementById('year')
    const monthYearSelect = document.getElementById('month-year')
    const monthSelect = document.getElementById('month')
    const horizontalAxisSelect = document.getElementById('horizontalAxis');
    const verticalAxisSelect = document.getElementById('verticalAxis');

    const startYear = 2020;
    const endYear = 2040;

    // 年リスト作成
    for (let y = startYear; y <= endYear; y++) {
        const option = new Option(y, y);
        console.log(option);
        yearSelect.add(option.cloneNode(true));
        monthYearSelect.add(option);
    };

    // 月リスト作成
    for (let m = 1; m <= 12; m++) {
        const option = new Option(m, m);
        console.log(option);
        monthSelect.add(option);
    };

    periodSelect.addEventListener('change', () => {
        console.log('form');
        const selected = periodSelect.value;

        if (selected === 'year') {
            yearContainer.classList.remove('hidden');
        } else if (selected === 'month') {
            monthContainer.classList.remove('hidden');
        };
        // graphForm.submit();
    });
});




// 以下、AJAXコード
// const graphForm = document.getElementById('graphForm');
// const graphArea = document.getElementById('home-graph')
// const periodSelect = document.getElementById('period');
// const yearContainer= document.getElementById('year-container')
// const monthContainer = document.getElementById('month-container')
// const yearSelect = document.getElementById('year')
// const monthYearSelect = document.getElementById('month-year')
// const monthSelect = document.getElementById('month')
// const horizontalAxisSelect = document.getElementById('horizontalAxis');
// const verticalAxisSelect = document.getElementById('verticalAxis');

// const startYear = 2020;
// const endYear = 2040;

// // 年リスト作成
// for (let y = startYear; y <= endYear; y++) {
//     const option = new Option(y, y);
//     yearSelect.add(option.cloneNode(true));
//     monthYearSelect.add(option);
// }

// // 月リスト作成
// for (let m = 1; m <= 12; m++) {
//     const option = new Option(m, m);
//     monthSelect.add(option);
// }

// // メイン表示期間の変更イベント
// periodSelect.addEventListener('change', () => {
//     const selected = periodSelect.value;

//     yearContainer.classList.add('hidden');
//     monthContainer.classList.add('hidden');

//     if (selected === 'year') {
//         yearContainer.classList.remove('hidden');
//     } else if (selected === 'month') {
//         monthContainer.classList.remove('hidden');
//     }
//     // 期間変更時にAJAX送信
//     submitForm();
// })

// // 年・月・横軸・縦軸の変更時も自動送信
// yearSelect.addEventListener('change', submitForm);
// monthYearSelect.addEventListener('change', submitForm);
// monthSelect.addEventListener('change', submitForm);
// horizontalAxisSelect.addEventListener('change', submitForm);
// verticalAxisSelect.addEventListener('change', submitForm);

// // AJAXフォーム送信
// const submitForm = () => {
//     const formData = new FormData(graphForm);

//     fetch(graphForm.action, {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         graphArea.innerHTML = data.svg;
//         document.getElementById('total_day').textContent = `${data.total_day}日`;
//         document.getElementById('total_hour').textContent = `${data.total_hour}時間`;
//         document.getElementById('avg_hour').textContent = `${data.avg_hour}時間/日`;
//     })
//     .catch(error => {
//         graphArea.innerHTML = `<p style="color:var(--error-text-color);">エラーが発生しました：${error}<p>`;
//     });
// }

