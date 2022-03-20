document.addEventListener("DOMContentLoaded", function(event) {

    var dropdowns = document.getElementsByClassName("dropdown");
    function dropdownToggleEventHandler(dropdown, dropdown_head){
        return function(){
            dropdown.classList.toggle("dropdown__show");

            if(dropdown.classList.contains("dropdown__show")){
                dropdown_head.style.borderColor = "white";
            }
            else if (dropdown_head.classList.contains("active")){
                dropdown_head.style.borderColor = "#ffb914";
            }
            else{
                dropdown_head.style.borderColor = "black";
            }
        }
    }
    function dropdownCloseEventHandler(dropdown, dropdown_head){
        document.addEventListener('click', function(e){
            const withinBoundaries = e.composedPath().includes(dropdown);

            if ( ! withinBoundaries ) {
                if(dropdown_head.classList.contains("active")){
                    dropdown_head.style.borderColor = "#ffb914";
                }
                else{
                    dropdown_head.style.borderColor = "black";
                }

                dropdown.classList.remove('dropdown__show');
            }
        })
    }
    for (var i = 0; i < dropdowns.length; i++) {
        var dropdown = dropdowns[i]
        var dropdown_head = dropdown.firstElementChild
        var filter_caption = dropdown_head.firstElementChild

        filter_caption.onclick = dropdownToggleEventHandler(dropdown, dropdown_head)

        dropdownCloseEventHandler(dropdown, dropdown_head)
    }

    function isEmpty(obj){
        return Object.keys(obj).length === 0;
    }
    url = location.toString()
    function getUrl(params){
        if (isEmpty(params)){
            return url.split('?')[0]
        }

        entries = Object.entries(params)
        params_str = '?'

        for (i = 0; i < entries.length; i++) {
            param = entries[i][0] + "=" + entries[i][1];
            params_str += param
            if(i != entries.length - 1)
                params_str += "&"
        }

        return url.split('?')[0] + params_str
    }
    var params = window.location.search.replace('?','').split('&').reduce(function(p,e){
                var a = e.split('=');
                p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
                if (a != "") {return p;}
            }, {});
    if(! params) params = {}

    brand_form = document.forms.filter_brand
    checkboxes = brand_form.elements

    if (! isEmpty(params)){
        if ('brands' in params){
            var brands = params['brands'].split(',')
            for (var i = 0; i < checkboxes.length; i++){
                if(brands.indexOf(checkboxes[i].id) != -1)
                    checkboxes[i].checked = true;
            }
            document.getElementById('brands-remove').onclick = function(){
                delete params['brands']
                location.assign(getUrl(params))
            }
        }
        if('search' in params){
            document.getElementById('search-remove').onclick = function(){
                delete params['search']
                location.assign(getUrl(params))
            }
        }
    }



    var dropdowns_search = document.getElementsByClassName("dropdown__search");
    function dropdownSearchFilterEventHandler(dropdown_search, dropdown_options){
        return function(){
            var regex = new RegExp(dropdown_search.value, "i");
            var checkbox_filters = dropdown_options.children;

            for (var i = 0; i < checkbox_filters.length; i++){
                checkbox_filter = checkbox_filters[i];
                if (!regex.test(checkbox_filter.lastElementChild.innerText))
                    checkbox_filter.classList.add("hidden");
                else if (checkbox_filter.classList.contains("hidden"))
                    checkbox_filter.classList.remove("hidden");
            }
        }
    }
    function dropdownSearchClearFilterEventHandler(dropdown_search, dropdown_options){
        return function(){
            dropdown_search.value = "";

            var checkbox_filters = dropdown_options.children;

            for (var i = 0; i < checkbox_filters.length; i++){
                if (checkbox_filters[i].classList.contains("hidden"))
                    checkbox_filters[i].classList.remove("hidden");
            }
        }
    }
    for (var i = 0; i < dropdowns_search.length; i++){
        var dropdown_search_btn_confirm = dropdowns_search[i].children[0];
        var dropdown__search_input = dropdowns_search[i].children[1];
        var dropdown_search_btn_clear = dropdowns_search[i].children[2]

        var dropdown_options = dropdowns_search[i].parentElement.nextElementSibling

        dropdown_search_btn_confirm.onclick = dropdownSearchFilterEventHandler(dropdown__search_input, dropdown_options)
        dropdown__search_input.oninput = dropdownSearchFilterEventHandler(dropdown__search_input, dropdown_options)
        dropdown_search_btn_clear.onclick = dropdownSearchClearFilterEventHandler(dropdown__search_input, dropdown_options);
    }

    brand_form.addEventListener("submit", function(event){
        event.preventDefault();
        var brands = []

        checkboxes = brand_form.elements
        for (i = 0; i < checkboxes.length; i++) {
            if(checkboxes[i].checked){
                brands.push(checkboxes[i].id)
            }
        }
        console.log(brands)
        console.log(params)
        if(brands.length != 0){
            params['brands'] = brands.join(',');

            location.assign(getUrl(params))
        }
    });
})