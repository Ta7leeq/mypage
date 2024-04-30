'use strict';

let gapWord=""
// Create an input element for dynamic use
const dynamicInput = document.createElement('input');
const startButtonClick=new MouseEvent('click');

dynamicInput.setAttribute('type', 'text');
dynamicInput.setAttribute('class', 'answer');
let sentence;
let i=0;
document.querySelector('.wrongMark').style.display = 'none';

document.querySelector('.again').addEventListener('click', againButton);

fetch('/get-questions')
  .then(response => response.json())
  .then(data => {
  
  const tables=data.tables
  const parentR = document.getElementById('excerciseName');
  for (var j of tables){
    var R = document.createElement("option");
    R.className="addedExcercise";
  
    R.textContent = j; // Set the content of the child div
  
  
    parentR.appendChild(R); // Add the child div to the parent div
  
  }
  

  
  })

  .catch(error => {
    console.error('Error:', error);
  });

  
  

function createFillTheGapSentence(sentence, gapNumber) {
  // Split the sentence into words
  const words = sentence.split(' ');
  gapWord=words[gapNumber - 1]
  // Check if the gapNumber is valid (you can add error handling here)
  if (gapNumber < 1 || gapNumber > words.length) {
    return "Invalid gap number.";
  }

  // Replace the word at gapNumber - 1 with an input element
  words[gapNumber - 1] = dynamicInput.outerHTML; // You can customize the input element as needed

  // Recreate the sentence with the gap
  const gapSentence = words.join(' ');

  // Return the fill-the-gap sentence
  return gapSentence;
}


document.querySelector('.check').addEventListener('click', function () {
  
   // Get the user's entered text
   let enteredText = document.querySelector('.answer').value;
   //console.log(enteredText);
   
   // Get the word at the gapNumber
   //const wordAtGap = getWordAtGap(inputSentence, inputGapNumber);
 
   // Check if the entered text matches the word at the gap
   if (enteredText === gapWord) {
     //document.querySelector('body').style.backgroundColor = '#60b347';
     document.querySelector('.wrongMark').style.display = 'none';
     document.querySelector('.checkMark').style.display = 'block';
     //alert('Correct!'); // Replace with your desired feedback
     i=i+1;
     setTimeout(function () {
      document.querySelector('.again').dispatchEvent(startButtonClick);
      }, 2000);   

     //document.querySelector('.again').addEventListener('click', againButton);
     
        
     
   } else {
     //alert('Incorrect. Try again.'); // Replace with your desired feedback
     document.querySelector('.wrongMark').style.display = 'block';
   }

  
});


function againButton() {
  document.querySelector('.checkMark').style.display = 'none';
  fetch('/get-questions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "Name": document.getElementById('excerciseName').value})
    })
  .then(response => response.json())
  .then(data => {
  // Use the data received from the server
  //console.log(data.numberOfRows);
  const gapWord=data.gapWord[i];
  const sentence=data.sentence[i];
  const img=data.Photos[i];
  
  console.log(img)


  document.querySelector('.questionPhoto').src=img;  

  console.log(gapWord);
  // Input the sentence and gap number
  const inputSentence = sentence;
  
  const inputGapNumber = gapWord;

  // Generate the fill-the-gap sentence
  const fillTheGapSentence = createFillTheGapSentence(inputSentence, inputGapNumber);

  // Display the fill-the-gap sentence by updating an HTML element
  document.querySelector('.sentence').innerHTML = fillTheGapSentence;
  })

  .catch(error => {
    console.error('Error:', error);
  });

  
  
  


  

  
};