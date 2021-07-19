function confirm() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("chart").style.display = 'none';
            document.getElementById("view").style.display = 'block';
            img_name = this.responseText
            document.getElementById("view").innerHTML = '<img src="./static/img/confirm.jpg" width=500 height=400>'
        }
    };
    xhttp.open("POST", "confirm");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function death() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("chart").style.display = 'none';
            document.getElementById("view").style.display = 'block';
            img_name = this.responseText
            document.getElementById("view").innerHTML = '<img src="./static/img/death.jpg" width=500 height=400>'
        }
    };
    xhttp.open("POST", "death");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function vaccine() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("chart").style.display = 'none';
            document.getElementById("view").style.display = 'block';
            img_name = this.responseText
            document.getElementById("view").innerHTML = '<img src="./static/img/vaccine.jpg" width=500 height=400>'
        }
    };
    xhttp.open("POST", "vaccine");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function gdp() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("chart").style.display = 'none';
            document.getElementById("view").style.display = 'block';
            img_name = this.responseText
            document.getElementById("view").innerHTML = '<img src="./static/img/gdp.jpg" width=500 height=400>'
        }
    };
    xhttp.open("POST", "gdp");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function population() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("chart").style.display = 'none';
            document.getElementById("view").style.display = 'block';
            img_name = this.responseText
            document.getElementById("view").innerHTML = '<img src="./static/img/population.jpg" width=500 height=400>'
        }
    };
    xhttp.open("POST", "population");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function chart_view() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            img_name = this.responseText
            document.getElementById("view").style.display = 'none';
            document.getElementById("chart").style.display = 'block';
            document.getElementById("view1").innerHTML = '<img src="./static/img/covid_gdp_plot1.png" width=95%>'
            document.getElementById("view2").innerHTML = '<img src="./static/img/covid_gdp_plot2.png" width=95%>'
            document.getElementById("view3").innerHTML = '<img src="./static/img/covid_gdp_plot3.png" width=95%>'
        }
    };
    xhttp.open("post", "covidgdp");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function kor_vac() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            aa = this.responseText
            alert("국내 백신 접종 현황 업데이트 완료!")
            document.getElementById("view").style.display = 'none';
            document.getElementById("chart").style.display = 'none';
            document.getElementById("korea").innerHTML = '<img src="./static/img/kor_vaccine.png" width=95%>'
        }
    };
    xhttp.open("post", "kor_vac");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
};


function world_vac() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            bb = this.responseText
            alert("전세계 백신 접종 현황 업데이트 완료!")
        }
    };
    xhttp.open("post", "world_vac");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
};