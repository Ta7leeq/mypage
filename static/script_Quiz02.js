'use strict';


// Create an input element for dynamic use
const dynamicInput = document.createElement('input');
const startButtonClick=new MouseEvent('click');

dynamicInput.setAttribute('type', 'text');
dynamicInput.setAttribute('class', 'answer');
let sentence;
let i=1;
let inputAnswer;
let QuestionHead;
let score=100;
let Count
document.querySelector('.wrongMark').style.display = 'none';
document.querySelector('.Answer02').style.display = 'none';

document.querySelector('.again').addEventListener('click', againButton);

fetch('/get-questions02')
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



document.querySelector('.check').addEventListener('click', function () {
  
   // Get the user's entered text
   let enteredText = document.querySelector('.Answer02').value;
   //console.log(inputAnswer)
   if (enteredText === inputAnswer) {
     //document.querySelector('body').style.backgroundColor = '#60b347';
     document.querySelector('.wrongMark').style.display = 'none';
     document.querySelector('.checkMark').style.display = 'block';
     document.querySelector('.Answer02').value = '';
     //alert('Correct!'); // Replace with your desired feedback
     i=i+1;


     setTimeout(function () {
      document.querySelector('.again').dispatchEvent(startButtonClick);
      }, 2000);   

     //document.querySelector('.again').addEventListener('click', againButton);
     
        
     
   } else {
     //alert('Incorrect. Try again.'); // Replace with your desired feedback
     score=score-(100/(Count-1));
     console.log(score)
     document.querySelector('.wrongMark').style.display = 'block';
     
     const audioPlayer = document.querySelector('.audioPlayer');

     // Add a cache-busting parameter to the URL
    const cacheBuster = new Date().getTime(); // This generates a unique timestamp
    //const updatedUrl = `${"http://192.168.0.31:8080/Test/output07.mp3"}?v=${cacheBuster}`;
    const updatedUrl = `${"http://127.0.0.1:8000/Test/output07.mp3"}?v=${cacheBuster}`;
    
     
     audioPlayer.src = updatedUrl;
     audioPlayer.play();
     
   }

  
});


function againButton() {
  document.querySelector('.checkMark').style.display = 'none';
  document.querySelector('.Answer02').style.display = 'block';
  fetch('/get-questions02', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "Name": document.getElementById('excerciseName').value, 
    "Score":score,
    "Counter":i
    
  
  })
    })
  .then(response => response.json())
  .then(data => {
  // Use the data received from the server
  //console.log(data.numberOfRows);
  Count=data.count;  
  const Question=data.Question[i];
  const Answer=data.Answer[i];
  const img=data.Photos[i];
  QuestionHead=data.Question[0]
  

  console.log(img)  
  document.querySelector('.questionPhoto').src=img;  
  if (i<Count){
    document.querySelector('.head').textContent=QuestionHead;
    document.querySelector('.sentence').textContent = Question;

  }
  else{
    document.querySelector('.Answer02').style.display = 'none';
    document.querySelector('.sentence').textContent = "Note "+ convertToGrade(score);
    
  }
    // Input the Question and gap Answer
  const inputQuestion = Question;
  
  inputAnswer = Answer;

  
  //console.log(Question)
  
  


  })

  .catch(error => {
    console.error('Error:', error);
  });

  
  
  


  

  
};


function convertToGrade(scorePercent) {
  if (scorePercent >= 90) {
    return 1;
  } else if (scorePercent >= 80) {
    return 2;
  } else if (scorePercent >= 60) {
    return 3;
  } else if (scorePercent >= 50) {
    return 4;
  } else if (scorePercent >= 25) {
    return 5;
  } else {
    return 6;
  }
}
