document.addEventListener("DOMContentLoaded", function(event) {

    var order_items = document.getElementById('order-items');
    var total_price_el = document.getElementById("total-price");

    var remove_order_forms = document.getElementsByClassName('order-item-delete-form');
    function removeOrderItemEventHandler(event){
        event.preventDefault();

        url = this.action;

        fetch(url, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
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