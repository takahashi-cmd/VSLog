// study_logs_listの動作

document.addEventListener('DOMContentLoaded', () => {
    // 日付を動的に表示
    const dateInput = document.getElementById('study_date');
    const form = document.getElementById('study-date-form');

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
            const [year, month] = data.selectedDate.split('-0');
            selectedDate.innerHTML = `<p>${year}年${month}月の学習履歴一覧</p>`;
            
            const totalDays = (year, month) => {
                const getDays = new Date(year, month, 0).getDate();
                return getDays;
            };
            console.log(`year:${year},month:${month},totalDays:${totalDays(year, month)}`);

            const studyLogsList = document.getElementById('study-logs-list');
            const studyLogsJoin = document.getElementById('study-logs-join');
            const originalContent = studyLogsJoin.cloneNode(true);
            console.log(originalContent)
            const studyLogsDate = document.getElementById('study-logs-date');
            const studyLogsContent = document.getElementById('study-logs-content');
            let result = '';
            for (let i = 1; i < totalDays(year, month) + 1; i++) {
                result += originalContent.outerHTML;
                console.log(result)
            }
            studyLogsList.innerHTML = result;
            console.log(studyLogsJoin)




        });
    }
});

