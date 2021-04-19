console.log('Checking out')
if(localStorage.getItem('cart')==null){
  var cart ={};
}
else{
  cart = JSON.parse(localStorage.getItem('cart'));

}
let total = 0;
for(item in cart){
  let name = cart[item][1];
  let quantity = cart[item][0];
  let price = cart[item][2];
  let unitPrice = cart[item][3];
  let productId = cart[item][4];
  let item_id = cart[item][5];
  total = total + cart[item][2];
  itemString = `  <li class="list-group-item d-flex justify-content-between align-items-center"><span class="badge badge-warning badge-pill">${price}</span>  ${quantity} of ${name} @${unitPrice}`;

  itemString1 = ` <span> <a class="btn btn-link"  href='/detail/${productId}' role="button">View product</a><button class='btn btn-link' id='foo' onClick='onRemoveClick(${productId});'>Remove</button></span></li>`;
//  alert(itemString1)
  itemString2 = itemString.concat(itemString1);
  $('#item_list').append(itemString2);


}
//totalPrice = ` <li class ="list-group-item d-flex justify-content-between align-items-center"> <p class="bg-light text-dark">${total}<b>Your total</p></b>
totalPrice = ` <li class ="list-group-item d-flex justify-content-between align-items-center list-group-item-info"> <b>Total value:&nbsp; ${total}</b>
  </li> `
$('#total').val(total);
$('#item_list').append(totalPrice);
$('#items').val(JSON.stringify(cart));

