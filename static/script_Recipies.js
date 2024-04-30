
 

'use strict';


//const o=document.getElementById('select_Recipie').querySelector('option[value="1"]').textContent;
//console.log(o);
//document.getElementById('select_Recipie').querySelector('option[value="1"]').textContent=10;

let numberOfIngredients;
let ingredients;
let ingredientIds;
let numberOfRecipies;
let Recipies;
let RecipiesIds;

fetch('/get-ingredients')
.then(response => response.json())
.then(data => {
  // Use the data received from the server
  //console.log(data.numberOfRows);
  numberOfIngredients=data.numberOfRows;
  ingredients=data.Ingredients;
  ingredientIds=data.IngredientIds;
  numberOfRecipies=data.numberOfRowsRecipies;
  Recipies=data.Recipies;
  RecipiesIds=data.RecipiesIds;
  
  function addOptions() {
    console.log(numberOfIngredients);
    // Get a reference to the <select> element
    var select = document.getElementById("select_Ingredient");
    var select_Recipie = document.getElementById("select_Recipie");
    var select_Recipie_ = document.getElementById("select_Recipie_");
  
    // Loop to create and add options
    for (var i = 1; i <= numberOfIngredients; i++) {
      
      var option = document.createElement("option");
      option.value = ingredientIds[i];
      option.text = ingredients[i];
      select.appendChild(option);
      
  }
    
    console.log(numberOfRecipies);
    // Get a reference to the <select> element
    

    // Loop to create and add options
    for (var i = 1; i <= numberOfRecipies; i++) {
    
    var optionR = document.createElement("option");
    optionR.value = RecipiesIds[i];
    optionR.text = Recipies[i];
    select_Recipie.appendChild(optionR);

    var optionR01 = document.createElement("option");
    optionR01.value = RecipiesIds[i];
    optionR01.text = Recipies[i];
    select_Recipie_.appendChild(optionR01);
    
    
}
  }
  addOptions(); // You can place this call anywhere in your code

  //console.log(numberOfRecipies);
  //document.querySelector('.highscore').textContent = data.message+" done by: "+data.id;
  

})

.catch(error => {
  console.error('Error:', error);
});


let x=10;


document.querySelector('.submitIngredient').addEventListener('click', function () {
  fetch('/send-ingredients', {
    
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    
    body: JSON.stringify({ "RecipieName": document.querySelector('#select_Recipie_').value , 
    "IngredientName": document.querySelector('#select_Ingredient').value,
    "Quantity": document.querySelector('#ingredient-quantity').value})
    })

    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});



document.querySelector('.submitRecipie').addEventListener('click',function(){
  //console.log(document.getElementById("select_Recipie").value);

  
  const select_Recipie = document.getElementById("select_Recipie");
  
  
    // Get the selected option
  const selectedOption = select_Recipie.options[select_Recipie.selectedIndex];
  
    // Get the text of the selected option
  const selectedText = selectedOption.text;
  
  
  //console.log(selectedText).selectedOption;
  

  const parentR = document.getElementById('Compiled_Recipes');
  const R = document.createElement("div");
  R.className="addedRecipie";
  
  R.textContent = selectedText; // Set the content of the child div
  
  
  parentR.appendChild(R); // Add the child div to the parent div

  fetch('/einkaufsWagen', {
    
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    
    body: JSON.stringify({ "einkaufsWagenItems": select_Recipie.value })
    })

    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
    

  });


document.querySelector('.Estimate').addEventListener('click',function(){
  
  
  console.log();



});







