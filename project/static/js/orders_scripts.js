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
        });

        var item_slug = event.currentTarget.parentNode.id.replace("order-item-", "");
        var item_total_price = Number(document.getElementById(`item-${item_slug}-total-price`).innerText.replace("грн", "").replace(',','.'));
        var total_price = Number(total_price_el.innerText.replace("грн", "").replace(',','.'));
        total_price_el.innerText = `${total_price - item_total_price}грн`

        console.log(item_total_price)
        console.log(total_price)
        order_items.removeChild(event.currentTarget.parentNode);
    };

    for (var i = 0; i < remove_order_forms.length; i++) {
        remove_order_forms[i].addEventListener('submit', removeOrderItemEventHandler);
    }
});