let addBtn = document.getElementById("add-cart");
document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

if (addBtn !== null) {
  addBtn.addEventListener("click", function () {
    let productId = this.dataset.product;
    console.log("productId", productId);

    console.log("USER:", user);

    let quantity = document.getElementById("product-quantity").value;
    updateUserOrder(productId, quantity);
  });
}


export function updateUserOrder(productId, quantity) {
  console.log("Sending data...");
  let url = "/update-item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, quantity: quantity }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}
