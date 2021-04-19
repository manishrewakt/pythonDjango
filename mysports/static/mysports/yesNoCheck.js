function yesnoCheck() {
//    console.log('Selecting Address')
//    if (document.getElementById('yesCheck').checked) {
//        document.getElementById('billingAddress').style.display = "none";
//    }else{
//        document.getElementById('billingAddress').style.display = "block";
//    }
//    };
    var x = document.getElementById('billingAddress');
    console.log('Selecting Address 123');
    if (document.getElementById('yesCheck').checked) {
        x.style.display = 'none';
        console.log('Selecting Address 345');
    } else {
        x.style.display = 'block';
        document.getElementById("address3").required = true
        document.getElementById("city1").required = true
        document.getElementById("state1").required = true
        document.getElementById("country1").required = true
        console.log('Selecting Address 567');
    }
   };
