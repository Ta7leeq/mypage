
 

'use strict';

/*
console.log(document.querySelector('.message').textContent);
document.querySelector('.message').textContent = '🎉 Correct Number!';
document.querySelector('.number').textContent = 13;
document.querySelector('.score').textContent = 10;
document.querySelector('.guess').value = 23;
console.log(document.querySelector('.guess').value);
*/


let startTime,endTime
let count=0
let score=0
let highscore=0
let t=0
let playerName=""


  
let secretN=0;
let secretL1=0;
let secretL2=0;
let secretL3=0;
let secretR1=0;
let secretR2=0;
let secretR3=0;

const startButton=document.querySelector('.again');
const startButtonClick=new MouseEvent('click');

//let initTime = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
let initTime = new Date();
document.querySelector('.time').textContent = 0;
//const audio1=new Audio("http://localhost:8080/Music/Playlists/game%20start.m4a");

const audio1=new Audio("http://10.252.0.162:8080/Music/Playlists/round1.m4a");
const audioFinalWinning=new Audio("http://localhost:8080/Music/Playlists/Who_Wants_To_Be_Millionair_FinalWinning/Who_Wants_To_Be_Millionair_FinalWinning.m4a");
const audioApplaus=new Audio("http://localhost:8080/Music/Playlists/Applaus.wav");
const displayMessage = function (message) {
  
  document.querySelector('.message').textContent = message;
  
};



document.querySelector('.check').addEventListener('click', function () {
  document.querySelector('#B').disabled = true;
  const guess = Number(document.querySelector('#guess').value);
  const L1 = Number(document.querySelector('#L1').value);
  const L2 = Number(document.querySelector('#L2').value);
  const L3 = Number(document.querySelector('#L3').value);
  const R1 = Number(document.querySelector('#R1').value);
  const R2 = Number(document.querySelector('#R2').value);
  const R3 = Number(document.querySelector('#R3').value);
  
  
  console.log(guess, typeof guess);
  
  
  
  // When there is no input
  if (!guess) {
    // document.querySelector('.message').textContent = '⛔️ No number!';
    displayMessage('⛔️ No number!');

    // When player wins
  } else if (L1*guess===R1 && L2*guess===R2 && L3*guess===R3 && R1+R2===R3) {
    //startButton.addEventListener('click', startButtonHandler);
    if (count<=3){

      document.querySelector('#C').disabled = true;
      document.querySelector('body').style.backgroundColor = '#6276ce';
      startButton.dispatchEvent(startButtonClick);
      
    }
    else{
      document.querySelector('body').style.backgroundColor = '#60b347';
      audioApplaus.play();

    }
    let eTime = new Date();
    audio1.pause();
    audioFinalWinning.play();
    //let eTimeFormat=eTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    count=count+1;
    t=t+Math.round((eTime-initTime)/1000);
    score=(count/t)*0.1*3600;
    
    document.querySelector('.zahl').textContent = count;
    document.querySelector('.score').textContent = Math.round(score * 10) / 10;
    
    
    document.querySelector('.time').textContent = Math.round((eTime-initTime)/1000);
    
    document.querySelector('.totalTime').textContent = t;
    //document.querySelector('.Bear_Name').submit();
    //document.querySelector('#B').submit();

    //console.log(t);
    
    //console.log(eTime);
    
    document.querySelector('.number').style.width = '30rem';
    // document.querySelector('.message').textContent = '🎉 Correct Number!';
    displayMessage('🎉 Correct Number!');
    //document.querySelector('.number').textContent = secretNumber;
    playerName=document.querySelector('.name').value;
    console.log(playerName);
    
    fetch('/send-data', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "Name": playerName,"Score": score })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    
  
    
    
    

    // When guess is wrong
  } else  {
    
      // document.querySelector('.message').textContent =
      // guess > secretNumber ? '📈 Too high!' : '📉 Too low!';
      displayMessage('Falsch gerechnet!' );
      audio1.pause();
      const audioGameOver=new Audio("http://localhost:8080/Music/Playlists/game-over.m4a")
      audioGameOver.play();
      //score--;
      document.querySelector('.score').textContent = score;
    
  }


});



function startButtonHandler () {
  //document.querySelector('#C').disabled = true;
  
  
  
  //const audio2=new Audio("http://localhost:8080/Music/Playlists/African_fun_long.mp3")
  audio1.play();
  //audio1.addEventListener('ended',  audio2.play());
  //audio2.addEventListener('ended',  audio2.play());

  //new Audio("https://clyp.it/qcr1brad").play();
  https://clyp.it/qcr1brad
  console.log("sound played");

  document.querySelector('#B').disabled = false;
  document.querySelector('.time').textContent = 0;
  let secretNumber = Math.trunc(Math.random() * 9) + 1;
  
  //Mathematical Model 

 

  do{
    secretN = Math.trunc(Math.random() * 8) + 2;
    secretR3 =  (Math.floor(Math.random() * (999 / secretN)) * secretN + secretN); // generates a random number between 1 and 999 that is divisible by the random factor
    secretR3=secretR3*10
    secretL3 =secretR3/secretN


    secretR1  = Math.floor(Math.random() * (secretR3 / secretN)) * secretN + secretN; // generates a random number between 1 and secretR3 that is divisible by the random factor

    secretL1 =secretR1/secretN  
    secretL2 =secretL3-secretL1 
    secretR2 =secretL2*secretN

  }while((secretR3/(secretN))>99);



  
  //console.log(startTime);


  
  //document.querySelector('body').style.backgroundColor = '#3f3f3d';
  
 

  document.querySelector('#guess').value=secretN

    
  document.querySelector('#L1').value=null
  document.querySelector('#L2').value=secretL2
  document.querySelector('#L3').value=null

  document.querySelector('#R1').value=null
  document.querySelector('#R2').value=null
  document.querySelector('#R3').value=secretR3

  fetch('/get-data')
  .then(response => response.json())
  .then(data => {
    // Use the data received from the server
    //console.log(data.message);
    document.querySelector('.highscore').textContent = data.message+" done by: "+data.id;
  })
  .catch(error => {
    console.error('Error:', error);
  });

  // document.querySelector('.message').textContent = 'Start guessing...';
  //displayMessage('Start guessing...');
  //document.querySelector('.score').textContent = score;
  //document.querySelector('.number').textContent = '?';
  //document.querySelector('.guess').value = '';

  
  
  document.querySelector('.number').style.width = '15rem';
};
startButton.addEventListener('click', startButtonHandler);

//startButton.dispatchEvent(startButtonClick);

