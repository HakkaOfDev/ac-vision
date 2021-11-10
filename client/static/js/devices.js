let ubiquiti = document.querySelector("#ubiquiti")
let dasan = document.querySelector("#dasan")

ubiquiti.addEventListener('click', (e) => {
    ubiquiti.classList.toggle('active')
    let ubiquiti_content = document.querySelector("#ubiquiti_content")
    if (ubiquiti_content.style.display === "flex") {
      ubiquiti_content.style.display = "none";
    } else {
      ubiquiti_content.style.display = "flex";
    }
})

dasan.addEventListener('click', (e) => {
    dasan.classList.toggle('active')
    let dasan_content = document.querySelector("#dasan_content")
    if (dasan_content.style.display === "flex") {
      dasan_content.style.display = "none";
    } else {
      dasan_content.style.display = "flex";
    }
})