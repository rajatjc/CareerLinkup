    const date = new Date(),
        ftCopy = document.querySelector("#ft-copy"),
        nav = document.querySelector(".navbar")

    // There is no footer on most pages, so guard before writing the year.
    if (ftCopy) ftCopy.textContent = date.getFullYear()
    window.onscroll = function(){
        if(document.documentElement.scrollTop > 100){
            nav.classList.add("header-scrolled")
        }else nav.classList.remove("header-scrolled")
    };

// Fade sections in as they scroll into view. Without IntersectionObserver they just show.
(() => {
    const items = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
        items.forEach(el => el.classList.add("in"));
        return;
    }
    const io = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
        });
    }, { threshold: 0.12 });
    items.forEach(el => io.observe(el));
})();
