// index.htmlのグラフ切替時の動作

// 変数定義
const graphForm = document.getElementById('graphForm');
const graphArea = document.getElementById('home-graph')
const periodSelect = document.getElementById('period');
const yearContainer= document.getElementById('year-container')
const monthContainer = document.getElementById('month-container')
const yearSelect = document.getElementById('year')
const monthYearSelect = document.getElementById('month-year')
const monthSelect = document.getElementById('month')
const horizontalAxisSelect = document.getElementById('horizontalAxis');
const verticalAxisSelect = document.getElementById('verticalAxis');
const graphType = document.getElementById('graphType');

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

// 画面起動時にformを自動送信
submitForm();

// プルダウンメニュー選択時に自動でformを送信
periodSelect.addEventListener('change', () => {
    const selected = periodSelect.value;
    yearContainer.classList.remove('home-display-add');
    yearContainer.classList.add('hidden');
    monthContainer.classList.remove('home-display-add');
    monthContainer.classList.add('hidden');

    if (selected === 'year') {
        yearContainer.classList.remove('hidden');
        yearContainer.classList.add('home-display-add');
    } else if (selected === 'month') {
        monthContainer.classList.remove('hidden');
        monthContainer.classList.add('home-display-add');
    };
    submitForm();
});

// 年・月・横軸・縦軸の変更時も自動送信
yearSelect.addEventListener('change', submitForm);
monthYearSelect.addEventListener('change', submitForm);
monthSelect.addEventListener('change', submitForm);
horizontalAxisSelect.addEventListener('change', submitForm);
verticalAxisSelect.addEventListener('change', submitForm);
graphType.addEventListener('change', submitForm);

// FetchAPIによる非同期通信
function submitForm() {
    const formData = new FormData(graphForm);
    console.log(formData);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    })
    fetch(graphForm.action, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.svg) {
            const src = `data:image/svg+xml;base64,${data.svg}`;
            graphArea.innerHTML = `<object class="home-graph-data" data="${src}" type="image/svg+xml">`;
        } else {
            graphArea.innerHTML = `<p style='color:var(--base-text-color);'>学習記録がありません。</p>`;
        }
        document.getElementById('total_day').textContent = `${data.total_day}日`;
        document.getElementById('total_hour').textContent = `${data.total_hour}時間`;
        document.getElementById('avg_hour').textContent = `${data.avg_hour}時間/日`;
    })
    .catch(error => {
        graphArea.innerHTML = `<p style="color:var(--error-text-color);">エラーが発生しました：${error}</p>`;
    });
}

// 折れ線グラフと分野別の組み合わせが選択できないようガード処理
const fieldsOption = horizontalAxisSelect.querySelector('option[value="fields"]');
const lineOption = graphType.querySelector('option[value="line"]');
console.log(fieldsOption, lineOption);

function syncAxisAvailability() {
    fieldsOption.disabled = graphType.value === 'line';
    lineOption.disabled = horizontalAxisSelect.value === 'fields'
}

horizontalAxisSelect.addEventListener('change', syncAxisAvailability);
graphType.addEventListener('change', syncAxisAvailability);

