"use strict"

const reg_form = document.querySelector(".reg");
const submit = document.getElementById('submit');
const submit_2 = document.getElementById("submit_2");

const h_1 = document.querySelector('.er .wrapper h1');
const skr_name = document.querySelector('#skr_name');
const skr_password = document.querySelector('#skr_password');
const skr_2 = document.querySelectorAll('.skr_2');
skr_2.forEach(item => console.log(item));
const wrapper = document.querySelector('.er .wrapper');
const input_box = document.querySelectorAll('.input-box');

const csrfToken = getCookie('csrftoken');

submit.addEventListener("click", async function(event){

    event.preventDefault()

    let tel = document.getElementById('tel').value;
    let maill = document.getElementById('email').value;

    const telPattern = /^8\d{10}$/;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!telPattern.test(tel)) {
        alert("Пожалуйста, введите корректный номер телефона");
        return;
    }
    if (!emailPattern.test(maill)) {
        alert("Пожалуйста, введите корректный адрес почты");
        return;
    }

    console.log(tel);
    console.log(maill);

    if (submit.classList.contains("note_name")){
        const response = await fetch('http://127.0.0.1:8000/api/reg_log/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
            body: JSON.stringify({'tel': tel, 'maill': maill}),
            credentials: "include"
        });
    
        const data = await response.json();
        
        console.log(data);
        console.log(data.email, data.number, data.check_acc_value);

        //document.getElementById('jwt').click();
    }
    else{
        let name = document.getElementById("name").value;
        let password = document.getElementById("password").value;

        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
        if(!passwordPattern.test(password)){
            alert("Пожалуйста, придумайте более надежный пароль");
            return;
        }


        const response = await fetch('http://127.0.0.1:8000/api/reg_log/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
            body: JSON.stringify({'tel': tel, 'maill': maill, 'name': name, 'password': password}),
            credentials: 'include'
        });
    
        const data = await response.json();
    
        console.log(data.tel2, data.maill2, data.name2, data.password2, data.check_acc_value);
        //console.log(data.decoded_jwt);

        document.getElementById('jwt').click();

    }

    // window.location.href = 'http://127.0.0.1:8000/';
    window.open('http://127.0.0.1:8000/', '_blank');

});


submit_2.addEventListener('click', function(event){

    event.preventDefault()
    
    let item;
    for (let y of skr_name.classList){
        if (y === 'skr'){
            item = y;
            console.log(y);
            break;
        }
    }
    
    if (item === 'skr'){
        skr_name.classList.remove("skr");
        skr_password.classList.remove("skr");
        wrapper.style.height = "580px";
        input_box.forEach((item => {
            item.classList.add("skr_2");
        }))
        h_1.textContent = "Регистрация";
        submit.textContent = "Отправить";

        submit.classList.add("name_in_area");
        submit.classList.remove("note_name");
    }
    else{
        skr_name.classList.add("skr");
        skr_password.classList.add("skr");
        skr_name.classList.add("skr_2");
        skr_password.classList.add("skr_2");
        input_box.forEach((item => {
            item.classList.remove("skr_2");
        }))
        wrapper.style.height = "400px";
        h_1.textContent = "Войти";
        submit.textContent = "Вход";

        submit.classList.remove("name_in_area");
        submit.classList.add("note_name");
    }

});


// Функция для получения значения куки по имени
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли кука с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Пример использования функции
const csrftoken = getCookie('csrftoken');
console.log('CSRFTOKEN:', csrftoken);

const sessionid = getCookie('sessionid');
console.log('SESSIONID:', sessionid);

const access_token = getCookie('access_token');
console.log('ACCESS TOKEN:', access_token);

const refresh_token = getCookie('refresh_token');
console.log('REFRESH TOKEN:', refresh_token);


document.getElementById('jwt').addEventListener('click', async function(e){
    const response = await fetch('http://127.0.0.1:8000/api/get_jwt_token_from_cookie/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
        credentials: "include"
    });
})