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
                let fieldHour = '';
                let content = '';
                if (studyArray) {
                    for (let i = 0; i < studyArray.length; i++) {
                        let hour = studyArray[i]['hour'];
                        let fieldname = studyArray[i]['fieldname'];
                        totalHour += hour;
                        fieldNames.push(fieldname);
                        fieldHour +=
                            `<p class="num">${[i + 1]}</p>
                            <p class="fn">${fieldname}</p>
                            <p class="hour">${hour}時間</p><br>`
                        content +=
                            `<div class="content-head">
                            <p class="num">${[i + 1]}</p>
                            <p class="c-fn">${fieldname}</p>
                            </div>
                            <div class="content">
                            <p>${studyArray[i]['content']}</p>
                            </div>`
                    }
                } else {
                    totalHour = 0;
                    fieldNames = `なし`
                    fieldHour = `<p class="hour">なし</p>`
                    content = `<p class="n-content">なし</p>`
                }
                node.querySelector('.total-hours').textContent = `学習時間：${totalHour}時間`;
                node.querySelector('.fields').textContent = `学習分野：${fieldNames}`;
                node.querySelector('.modal-date').innerHTML = `<h1>${year}年${month}月${d}日</h1>`
                node.querySelector('.modal-total-hour').innerHTML =
                    `<p class="total-hour">${totalHour}時間</p>`
                node.querySelector('.modal-field-hour').innerHTML =
                    `${fieldHour}`
                node.querySelector('.modal-study-content').innerHTML =
                    `${content}`
                frag.appendChild(node);
            }
            studyLogsList.appendChild(frag)
        });
    }
    
    // モーダルウィンドウの設定
    const studyLogsList = document.getElementById('study-logs-list');
    const options = {
        duration: 200,
        easing: 'ease',
        fill: 'forwards'
    };

    function openModal(modal, mask) {
        modal.classList.add('is-open');
        mask.classList.add('is-open');
        modal.animate({ opacity: [0, 1] }, options);
        mask.animate({ opacity: [0, 1] }, options);
    }

    function closeModal(modal, mask) {
        modal.animate({ opacity: [1, 0] }, options).onfinish = () => {
            modal.classList.remove('is-open');
        };
        mask.animate({ opacity: [1, 0] }, options).onfinish = () => {
            mask.classList.remove('is-open');
        };
    }

    studyLogsList.addEventListener('click', (e) => {
        const openBtn = e.target.closest('.open');
        if (openBtn) {
            const card = openBtn.closest('.study-logs-join');
            const modal = card.querySelector('.modal-content');
            const mask = card.querySelector('.mask');
            openModal(modal, mask);
            return;
        }
        const closeBtn = e.target.closest('.close');
        if (closeBtn) {
            const card = closeBtn.closest('.study-logs-join');
            const modal = card.querySelector('.modal-content');
            const mask = card.querySelector('.mask');
            closeModal(modal, mask);
            return;
        }

        if (e.target.classList.contains('mask')) {
            const card = e.target.closest('.study-logs-join');
            const modal = card.querySelector('.modal-content');
            closeModal(modal, e.target);
        }
    })
});

