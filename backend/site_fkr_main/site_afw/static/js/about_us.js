'use strict';
let ij = document.querySelector(".ij");
let temas = document.querySelector(".temas");
let teman = document.querySelector(".teman");
let we = document.querySelector(".we");

if (sessionStorage.getItem("temas") !== 0 && sessionStorage.getItem("teman") !== 0){
    temas.style.opacity = sessionStorage.getItem("temas");
    teman.style.opacity = sessionStorage.getItem("teman");
}

ij.addEventListener("click", () => {
    if (window.getComputedStyle(temas).opacity == 1 && window.getComputedStyle(teman).opacity == 0) {
        temas.style.opacity = 0;
        teman.style.opacity = 1;
    } else {
        temas.style.opacity = 1;
        teman.style.opacity = 0;
    }
    sessionStorage.setItem("temas", temas.style.opacity);
    sessionStorage.setItem("teman", teman.style.opacity);
});




let lkj = document.getElementById('lkj');
lkj.addEventListener('click', function(e){
    console.log(document.cookie); //Для теста
    document.cookie = "access_token" + '=; Max-age=-1';
    document.cookie = "refresh_token" + '=; Max-age=-1';
    console.log(document.cookie); //Для теста
    window.location.reload(); //Не обязательно
});




document.getElementById('upload-form').addEventListener('submit', async function(event){

    event.preventDefault();
  
    const file_input = document.getElementById('file-input');
    const form_data = new FormData();
  
    form_data.append('file', file_input.files[0]);
  
    const const_file_name = await fetch('http://127.0.0.1:8000/api/file_name/', {
    method: 'POST',
    body: form_data
    })
    .then(response => {
      if (!response.ok){
        throw new Error('File upload failed: ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      console.log(data.file_name);
      return data.file_name;
    })
    .catch( function(err){
      console.error("Error: ", err)
    });
  
    console.log(const_file_name);
  
  
    const all_file = await fetch('http://127.0.0.1:8000/api/file/', {
      method: 'POST',
      body: form_data
    })
    .then(response => {
      if (!response.ok){
        throw new Error('File upload failed: ' + response.statusText);
      }
      return response.blob();
    })
    .then(blob => {
      return blob;
      
    })
    .catch(err => {
      console.error("Error: ", err);
    });
  
    const container = document.getElementById('download-link-container');
    const elem_container = container.querySelector('a');
  
    let downloadLink;
    if (!elem_container){
      downloadLink = document.createElement('a');
      container.appendChild(downloadLink);
    }
    else{
      downloadLink = elem_container;
    }
  
    downloadLink.textContent = "Скачать файл!!!";
    downloadLink.style.textDecoration = "none";
  
    const url = window.URL.createObjectURL(all_file);
    downloadLink.href = url;
  
    downloadLink.download = const_file_name;
  
    downloadLink.addEventListener('click', () => {
      setTimeout(() => window.URL.revokeObjectURL(url), 100);
    });
});




/* localStorage.setItem("a", temas.width);
console.log(localStorage.getItem("a")); */
/* if (localStorage.getItem("temas") !== null && localStorage.getItem("teman") !== null) {
    console.log("1");
    console.log(window.getComputedStyle(temas).opacity);
    console.log(window.getComputedStyle(teman).opacity);
    temas.style.opacity = localStorage.getItem("temas");
    teman.style.opacity = localStorage.getItem("teman");
    console.log(window.getComputedStyle(temas).opacity);
    console.log(window.getComputedStyle(teman).opacity);
} else {
    console.log("2");
    console.log(window.getComputedStyle(temas).opacity);
    console.log(window.getComputedStyle(teman).opacity);
    // Установка значений в localStorage при первой загрузке
    localStorage.setItem("temas", window.getComputedStyle(temas).opacity);
    localStorage.setItem("teman", window.getComputedStyle(teman).opacity);
    console.log(window.getComputedStyle(temas).opacity);
    console.log(window.getComputedStyle(teman).opacity);
}

console.log("Initial temas opacity:", temas.style.opacity);
console.log("Initial teman opacity:", teman.style.opacity);

ij.addEventListener("click", () => {
    if (window.getComputedStyle(temas).opacity == 1 && window.getComputedStyle(teman).opacity == 0) {
        temas.style.opacity = 0;
        teman.style.opacity = 1;
    } else {
        temas.style.opacity = 1;
        teman.style.opacity = 0;
    }

    // Сохранение значений в localStorage
    localStorage.setItem("temas", window.getComputedStyle(temas).opacity);
    localStorage.setItem("teman", window.getComputedStyle(teman).opacity);

    console.log("Updated temas opacity:", temas.style.opacity);
    console.log("Updated teman opacity:", teman.style.opacity);
}); */

    /* temas.classList.toggle("s");
    teman.classList.toggle("s");
    we.classList.toggle("color_white"); */
