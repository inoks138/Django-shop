document.addEventListener("DOMContentLoaded", function(event) {

    var dropdowns = document.getElementsByClassName("dropdown");
    function dropdownToggleEventHandler(dropdown, dropdown_head){
        return function(){
            dropdown.classList.toggle("dropdown__show");

            if(dropdown.classList.contains("dropdown__show"))
                dropdown_head.style.borderColor = "white";
            else dropdown_head.style.borderColor = "black";
        }
    }
    function dropdownCloseEventHandler(dropdown, dropdown_head){
        document.addEventListener('click', function(e){
            const withinBoundaries = e.composedPath().includes(dropdown);

            if ( ! withinBoundaries ) {
                dropdown_head.style.borderColor = "black";
                dropdown.classList.remove('dropdown__show');
            }
        })
    }

    for (var i = 0; i < dropdowns.length; i++) {
        var dropdown = dropdowns[i]
        var dropdown_head = dropdown.firstElementChild

        dropdown_head.onclick = dropdownToggleEventHandler(dropdown, dropdown_head)

        dropdownCloseEventHandler(dropdown, dropdown_head)
    }


    var get_params = window.location.search.replace('?','').split('&').reduce(function(p,e){
                var a = e.split('=');
                p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
                if (a != "") {return p;}
            }, {});


    brand_form = document.forms.filter_brand
    checkboxes = brand_form.elements

    if (get_params && 'brands' in get_params){
        var brands = get_params['brands'].split(',')
        for (var i = 0; i < checkboxes.length; i++){
            if(brands.indexOf(checkboxes[i].id) != -1)
                checkboxes[i].checked = true;
        }
    }

    var search_filter_wraps = document.getElementsByClassName("filter-search-wrap");
    function searchFilterEventHandler(search_filter, dropdown_options){
        return function(){
            var regex = new RegExp(search_filter.value, "i");
            var brand_filters = dropdown_options.children;

            for (var i = 0; i < brand_filters.length; i++){
                brand_filter = brand_filters[i];
                console.log(regex.test(brand_filter.lastElementChild.innerText))
                if (!regex.test(brand_filter.lastElementChild.innerText))
                    brand_filter.classList.add("hidden");
                else{
                    if (brand_filter.classList.contains("hidden"))
                         brand_filter.classList.remove("hidden");
                }
            }
        }
    }
    function testFunc(search_filter, dropdown_options){
        return function(){
            search_filter.value = "";

            var brand_filters = dropdown_options.children;

            for (var i = 0; i < brand_filters.length; i++){
                if (brand_filters[i].classList.contains("hidden"))
                    brand_filters[i].classList.remove("hidden");
            }
        }
    }

    for (var i = 0; i < search_filter_wraps.length; i++){
        var button_search_confirm = search_filter_wraps[i].children[0];
        var search_filter = search_filter_wraps[i].children[1];
        var button_search_clear = search_filter_wraps[i].children[2]

        var dropdown_options = search_filter_wraps[i].parentElement.nextElementSibling

        button_search_confirm.onclick = searchFilterEventHandler(search_filter, dropdown_options)
        search_filter.oninput = searchFilterEventHandler(search_filter, dropdown_options)
        button_search_clear.onclick = testFunc(search_filter, dropdown_options);
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

        if(brands.length != 0){
            var url = location.toString();

            if(get_params){
                get_params['brands'] = brands.join(',');
                entries = Object.entries(get_params)
                params_str = '?'

                for (i = 0; i < entries.length; i++) {
                    param = entries[i][0] + "=" + entries[i][1];
                    params_str += param
                    if(i != entries.length - 1)
                        params_str += "&"
                }
                location.assign(url.split('?')[0] + params_str)
            }
            else{
                location.assign(url + "?brands=" + brands.join(','))
            }
        }
    })
})