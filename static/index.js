const button = document.querySelectorAll("#del");
button.forEach((btn) => {
  btn.addEventListener('click', function(e){
    btn.classList.add("pirlo");
  })
});