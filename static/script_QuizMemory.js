'use strict';


// Create an input element for dynamic use
const dynamicInput = document.createElement('input');
const startButtonClick=new MouseEvent('click');

dynamicInput.setAttribute('type', 'text');
dynamicInput.setAttribute('class', 'answer');
let sentence;
let i=1;
let inputAnswer
let QuestionHead

//document.querySelector('.quizName').textContent="Hello World";





fetch('/get-questions02')
  .then(response => response.json())
  .then(data => {
  
  const tables=data.rTables
  
  const parentR = document.querySelector('.quizName');
  

  for (var j of tables){
    
    const R = document.createElement("p");
    //R.className="addedExcercise";
  
    R.textContent = j; // Set the content of the child div
    //console.log(R.textContent)
  
    parentR.appendChild(R); // Add the child div to the parent div
  
  }
  

  
  })

  .catch(error => {
    console.error('Error:', error);
  });





 
  


  

  
