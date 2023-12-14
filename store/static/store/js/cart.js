import { updateUserOrder } from "./cart_navbar.js";

let removeItemBtns = document.getElementsByClassName("remove-item");

for (let btn of removeItemBtns) {
  btn.addEventListener("click", function () {
    let productId = this.dataset.product;
    console.log("productId", productId);

    console.log("USER:", user);

    let quantity = 0;
    updateUserOrder(productId, quantity);
  });
}
