
let pass = true,
    mtag = document.querySelector("meta[name=theme-color]"),
    light = "#DDE1E4",
    dark = "#222831"

const bool_IsInView = (el, p, d = true) => {
    const percentVisible = p/100,
    {top:elemTop, bottom:elemBottom, height:elemHeight} = el.getBoundingClientRect(),
    overhang = elemHeight * (1 - percentVisible)
    
    if(!d){return (elemTop >= -overhang && elemBottom <= window.innerHeight + overhang)}
    return elemBottom <= window.innerHeight + overhang
}

const SlideUpOnView = (el, bool) => {
    if(bool_IsInView(el, 50, bool)){
        el.classList.add("inview")
    }
    else el.classList.remove("inview")
}

const raf = requestAnimationFrame || (ts => (setTimeout(ts, 1000/60))),
	cancelRaf = (h) => {
		cancelAnimationFrame ? cancelAnimationFrame(h) : clearTimeout(h)
}

// function for toggling password vissibility
const togglePasswd = (e, el)=>{
    const pwrd = document.querySelector(el)
    fa = e.querySelector('.fa')

    if(pass){
        fa.classList.replace("fa-eye", "fa-eye-slash")
        pwrd.setAttribute("type", "text")
    }else{
        fa.classList.replace("fa-eye-slash", "fa-eye")
        pwrd.setAttribute("type", "password")
    }pass = !pass
    pwrd.focus()
}



// Theme to Dark
const toDark = () => {
    document.documentElement.setAttribute("data-theme", "dark")
    mtag.content = dark
    localStorage.setItem("data-theme", 'dark')

}

// Theme to Light
const toLight = () => {
    document.documentElement.setAttribute("data-theme", "light")
    mtag.content = light
    localStorage.setItem("data-theme", 'light')

}



// Password validator

const checkPwd = () => {
    pwd = document.querySelector('#password')
    info = document.querySelector('#pwd-info')
    pwd.addEventListener("input", (e) =>{
        if(e.target.value.length < 8){
            msg =`<span class="text-danger">Pasword is too short.</span>`
            e.target.setCustomValidity("Password must have at least 8 characters")
        }else if(!/[a-z]/.test(e.target.value)){
            msg =`<span class="text-danger">Include a lowercase letter.</span>`
            e.target.setCustomValidity("Include a lowercase letter.")
        }else if(!/[0-9]/.test(e.target.value)){
            msg =`<span class="text-danger">Include a number.</span>`
            e.target.setCustomValidity("Include a number.")
        }else if(!/[A-Z]/.test(e.target.value)){
            msg =`<span class="text-danger">Include an uppercase letter.</span>`
            e.target.setCustomValidity("Include an uppercase letter.")
        }else if(!/[^0-9a-zA-Z]/.test(e.target.value)){
            msg =`<span class="text-danger">Include a special character.</span>`
            e.target.setCustomValidity("Include a special character.")
        }else{
            msg =`<span class="text-success">Password is good.</span>`
            e.target.setCustomValidity("")
        }
        
        info.innerHTML = e.target.value.length !== 0 ? msg : ""
    })
}

