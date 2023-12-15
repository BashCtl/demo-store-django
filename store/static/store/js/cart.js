let addBtn = document.getElementById("add-cart");

if (addBtn !== null) {
  addBtn.addEventListener("click", function () {
    let productId = this.dataset.product;
    let quantity = document.getElementById("product-quantity").value;
    updateUserOrder(productId, quantity);
  });
}

export function updateUserOrder(productId, quantity) {
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

export function deleteItem(productId) {
  let url = "/delete-item/" + productId;

  fetch(url, {
    method: "delete",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}

let removeItemBtns = document.getElementsByClassName("remove-item");

for (let btn of removeItemBtns) {
  btn.addEventListener("click", function () {
    let productId = this.dataset.product;
    deleteItem(productId);
  });
}

let updateBtns = document.getElementsByClassName("update-cart");

for (let btn of updateBtns) {
  btn.addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let quantity = 0;

    if (action === "add") {
      quantity += 1;
    }
    if (action === "remove") {
      quantity -= 1;
    }

    updateUserOrder(productId, quantity);
  });
}
