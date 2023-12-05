let addBtn = document.getElementById("add-cart");

addBtn.addEventListener("click", function () {
  let productId = this.dataset.product;
  console.log("productId", productId);

  console.log("USER:", user);
  if (user === "AnonymousUser") {
    // addCookieItem(productId);
  } else {
    let quantity = document.getElementById("product-quantity").value;
    updateUserOrder(productId, quantity);
  }
});

function addCookieItem(productIdn) {
  console.log("User is not authenticated");

  if (cart[productId] === undefined) {
    cart[productId] = { quantity: 1 };
  } else {
    cart[productId]["quantity"] += 1;
  }

  if (cart[productId]["quantity"] <= 0) {
    delete cart[productId];
  }

  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(productId, quantity) {
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
      console.log("Data:", data);
      location.reload();
    });
}
