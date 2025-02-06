"use strict";
/*
questo file si occupa di rendere dinamico l'aspetto delle pagine /podcast/
getBrowser() capisce se si sta usando chrome o firefox e cambia quindi il colore della playbar per matchare quello dei riproduttori audio di default dei due browser
openPlayBar() apre la playbar quando viene premuto il play button, mentre closeplaybar() la chiude
expandcomments() apre e chiuse la sezione commenti cambiando anche il contenuto del tasto 
expanddescription() apre e chiude la descrizione al click di un episodio
followbutton() cambia l'aspetto del pulsante follow a seconda che si segua o meno lo show
formtagset() copia i tag attualmente attivi per il podcast nel form di modifica
livesearch() implementa la ricerca in tempo reale nel testo degli episodi
*/

function getBrowser()
{
  let userAgent = navigator.userAgent;
  let playBar = document.getElementsByClassName('playBar');
  for (let i = 0; i < playBar.length; i++) 
  {
      if(userAgent.match(/firefox|fxios/i))
      {
          playBar[i].classList.remove("chrome");
          playBar[i].classList.add("firefox");  
      }
  }
}

function openPlayBar()
{
  let audioBar = document.getElementsByClassName('audioBar');
  let playButtons = document.getElementsByClassName('play-button');
  let playBar = document.getElementsByClassName('playBar');
  for (let i = 0; i < playButtons.length; i++) 
  {
    playButtons[i].addEventListener('click', function()
    {
      for (let j = 0; j < playBar.length; j++) 
      {
        audioBar[j].pause();
        playBar[j].classList.remove("show");
      }

      let str = this.getAttribute('aria-roledescription');
      let playBarEp = document.getElementsByClassName(str);
      for (let k = 0; k < playBar.length; k++) 
      {
        playBarEp[k].classList.add("show");     
      }
    });
  }
}

function closePlayBar()
{
  let audioBar = document.getElementsByClassName('audioBar');
  let playBar = document.getElementsByClassName('playBar');
  let closeButtons = document.getElementsByClassName('closePlayBar');
  for (let i = 0; i < closeButtons.length; i++)
  {
    closeButtons[i].addEventListener("click", function()
    {
      for (let j = 0; j < playBar.length; j++) 
      {
        playBar[j].classList.remove("show");
        audioBar[j].pause();
      }
    });
  }
}

function expandComments()
{
  let commentsButtons = document.getElementsByClassName('commentsButton')
  let str;
  for (let i = 0; i < commentsButtons.length; i++) 
  {
      commentsButtons[i].addEventListener('click', function() 
      {

          if(this.innerText === 'show comments')
          {
            this.innerText = 'hide comments';
          }
          else
          {
            this.innerText = 'show comments';
          }
          let episode = this.getAttribute('aria-roledescription');
          str = '.sComments' + episode
          document.querySelector(str).classList.toggle('expand');

      });
  }
}

function expandDescription()
{
  let episodes = document.getElementsByClassName('episode')
  for (let i = 0; i < episodes.length; i++) 
  {
      episodes[i].addEventListener('click', function(e) 
      {
        if(e.target == this)
        {
          this.querySelector('.expandDescription').classList.toggle('expand');
        }
      });
  }
}

function followButton()
{
  let button = document.body.querySelector('.follow');
  if(button)
  {
    button.addEventListener('click', function() 
    {
      if(button.innerText === 'follow') 
      {
        button.innerText = 'following';
        button.value = 'following';
      }
      else 
      {
        button.innerText = 'follow';
        button.value = 'follow';
      }
    })
  }
}

function formTagsSet()
{
  let tag = document.querySelector("#tagComedy");
  if(typeof(tag) != 'undefined' && tag != null)
    document.getElementById("btncheck1").checked = "true";

  tag = document.querySelector("#tagPolitics");
  if(typeof(tag) != 'undefined' && tag != null)
    document.getElementById("btncheck2").checked = "true";

  tag = document.querySelector("#tagHistory");
  if(typeof(tag) != 'undefined' && tag != null)
    document.getElementById("btncheck3").checked = "true";

  tag = document.querySelector("#tagCrime");
  if(typeof(tag) != 'undefined' && tag != null)
    document.getElementById("btncheck4").checked = "true";
}

function liveSearch() 
{
  let cards = document.querySelectorAll('.episode')
  let query = document.getElementById("searchbox").value;

  for (let i = 0; i < cards.length; i++) 
  {
    if(cards[i].innerText.toLowerCase().includes(query.toLowerCase())) 
      {
        cards[i].classList.remove("is-hidden");
      } 
    else 
    {
      cards[i].classList.add("is-hidden");
    }
  }
}

const getB = getBrowser();
const openP = openPlayBar();
const closeP = closePlayBar();
const expC = expandComments();
const expD = expandDescription();
const followB = followButton();
const formT = formTagsSet();
const liveS = liveSearch();