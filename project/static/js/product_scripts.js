document.addEventListener("DOMContentLoaded", function(event) {
    nav_tabs = document.getElementsByClassName('tabs-nav-item')
    tabs = document.getElementsByClassName('tab')

    function navTabEventHandler(event){
        nav_tab = event.target
        tab = document.getElementsByClassName(nav_tab.id.replace('s-nav', ''))[0]

        for(i = 0; i < nav_tabs.length; i++){
            if(nav_tabs[i] != nav_tab){
                nav_tabs[i].classList.remove("active")
            }
            if(tabs[i] != tab){
                tabs[i].classList.remove("active")
            }
        }

        nav_tab.classList.add("active")
        tab.classList.add("active")
    }

    for(i = 0; i < nav_tabs.length; i++){
        nav_tabs[i].addEventListener('click', navTabEventHandler)
    }
})