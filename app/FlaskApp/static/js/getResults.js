const getResults = poll_id => {
    const results_view = `http://127.0.0.1:5000/api/1.0/results/${poll_id}`;
    fetch(results_view).then(response => {
        if (response.status >= 400){
            return response.json().then(respError => {
                let error = respError;
                throw error;
            });
        }
        return response.json().then(respBody => {
            const total = document.querySelector('span#number-votes');
            const csv = document.querySelector('button#csv');
            total.textContent = respBody.total;
            csv.addEventListener('click', event => {
                event.preventDefault();
                window.location.replace(`${window.origin}/static/csv/${respBody.csv}`);
            });
            const results = respBody.results;
            const labels = Object.keys(results);
            const data = Object.values(results);
            let canvas = document.querySelector('canvas#pollChart').getContext('2d');
            let backgroundColor = [];
            for (let x of data){
                var r = Math.floor(Math.random() * 255);
                var g = Math.floor(Math.random() * 255);
                var b = Math.floor(Math.random() * 255);
                var a = 0.6;
                var rgba = `rgba(${r}, ${g}, ${b}, ${a})`;
                backgroundColor.push(rgba);
            }
            let pollChart = new Chart(canvas, {
                type: 'horizontalBar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Votes',
                        data,
                        backgroundColor,
                        borderWidth: 1,
                        borderColor: '#000',
                        hoverborderWidth: 3,
                        hoverborderColor: '#777'
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: respBody.title,
                        fontSize: 20
                    },
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Votes'
                            },
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        });
    }).catch(respError => {
        console.log(respError);
    });
}