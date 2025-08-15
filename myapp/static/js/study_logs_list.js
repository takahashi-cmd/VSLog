// study_logs_listの動作

document.addEventListener('DOMContentLoaded', () => {
    // 日付を動的に表示
    const dateInput = document.getElementById('study_date');
    const form = document.getElementById('study-date-form');

    // 初回表示時にも実行（今月の一覧を描画）
    submitForm();

    dateInput.addEventListener('change', () => {
        submitForm();
    })
    
    // FetchAPIによる非同期通信
    function submitForm() {
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        })
        console.log(jsonData);
        fetch(form.action, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            console.log(data.selectedDate)
            const selectedDate = document.getElementById('selected_date');
            const [year, month] = data.selectedDate.split('-');
            selectedDate.innerHTML = `<p>${year}年${month}月の学習履歴一覧</p>`;
            
            const totalDays = (year, month) => {
                const getDays = new Date(year, month, 0).getDate();
                return getDays;
            };
            console.log(`year:${year},month:${month},totalDays:${totalDays(year, month)}`);
            const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

            const studyLogsList = document.getElementById('study-logs-list');
            const studyLogsTemplate = document.getElementById('study-logs-template');
            studyLogsList.textContent = '';
            const frag = document.createDocumentFragment();

            for (let d = 1; d < totalDays(year, month) + 1; d++) {
                const dateObj = new Date(year, month - 1, d);
                const node = studyLogsTemplate.content.firstElementChild.cloneNode(true);
                // 日付の取得
                node.querySelector('.study-days').textContent = String(d);
                // 曜日の取得
                node.querySelector('.day-of-week').textContent = weekdays[dateObj.getDay()];
                // 学習時間、学習分野の取得
                const formatted = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
                const studyArray = data.studyDicts[formatted];
                let totalHour = 0;
                let fieldNames = [];
                if (studyArray) {
                    for (let i = 0; i < studyArray.length; i++) {
                        let hour = studyArray[i]['hour'];
                        let fieldname = studyArray[i]['fieldname'];
                        totalHour += hour;
                        fieldNames.push(fieldname);
                    }
                } else {
                    totalHour = 0;
                    fieldNames = `なし`
                }
                node.querySelector('.total-hours').textContent = `学習時間：${totalHour}時間`;
                node.querySelector('.fields').textContent = `学習分野：${fieldNames}`;
                frag.appendChild(node);
            }
            studyLogsList.appendChild(frag)
        });
    }

    // モーダルウィンドウの設定
    const open = document.querySelector('.open');
    const close = document.querySelector('.close');
    const modal = document.querySelector('.modal-content');
    const mask = document.querySelector('.mask');
    console.log(open, close, modal, mask);

    const showKeyframes = {
        opacity: [0, 1],
        display: 'block'
    };
    const hideKeyframes = {
        opacity: [1, 0],
        display: 'none'
    };
    const options = {
        duration: 800,
        easing: 'ease',
        fill: 'forwards'
    };

    // モーダルウィンドウを開く
    open.addEventListener('click', () => {
        modal.animate(showKeyframes, options);
        mask.animate(showKeyframes, options);
    });

    // モーダルウィンドウを閉じる
    close.addEventListener('click', () => {
        modal.animate(hideKeyframes, options);
        mask.animate(hideKeyframes, options);
    });

    // マスクをクリックしてモーダルウィンドウを閉じる
    mask.addEventListener('click', () => {
        close.click();
    });
});

