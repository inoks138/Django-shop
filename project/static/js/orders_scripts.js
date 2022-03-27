document.addEventListener("DOMContentLoaded", function(event) {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var order_items = document.getElementById('order-items');
    var total_price_el = document.getElementById("total-price");

    var remove_order_forms = document.getElementsByClassName('order-item-delete-form');
    function removeOrderItemEventHandler(event){
        event.preventDefault();

        const csrftoken = getCookie('csrftoken');
        url = this.action;

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(json => removeOrderItemRender(json));
    };
    function removeOrderItemRender(data){
        total_price_el.innerText = `${Number(data['total_price'])} грн`;

        order_item = document.getElementById(`order-item-${data['slug']}`)
        order_items.removeChild(order_item);
    }
    for (var i = 0; i < remove_order_forms.length; i++) {
        remove_order_forms[i].addEventListener('submit', removeOrderItemEventHandler);
    }
});