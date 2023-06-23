let navbarItem = document.querySelectorAll('.item')
for (let i = 0; i < navbarItem.length; i++) {
    navbarItem[i].addEventListener('click', function () {
        for (let i = 0; i < navbarItem.length; i++) {
            navbarItem[i].classList.remove('active')
        }
        this.classList.add('active')
    })
}

var typed = new Typed(".type_text", {
    strings: ["Let's Create", "ChatGPT", "Developing interesting","ChatGLM","Stable Diffusion","Let's Develop","Open source ヾ(•ω•`)o"],
    typeSpeed: 50,
    backSpeed: 50,
    backDelay: 1500,
    loop: true
})