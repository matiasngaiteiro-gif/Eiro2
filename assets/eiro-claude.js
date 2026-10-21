/* /pruebaclaude · menú lateral en celular y saludo según la hora */
(function(){
  var root=document.documentElement,side=document.getElementById('side'),openB=document.querySelector('[data-side-open]');
  function set(on){root.classList.toggle('side-open',on);if(openB)openB.setAttribute('aria-expanded',on?'true':'false');if(on){var a=side.querySelector('a');if(a)a.focus()}else if(openB&&document.activeElement&&side.contains(document.activeElement))openB.focus()}
  if(openB)openB.addEventListener('click',function(){set(true)});
  [].forEach.call(document.querySelectorAll('[data-side-close]'),function(b){b.addEventListener('click',function(){set(false)})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&root.classList.contains('side-open'))set(false)});
  var g=document.querySelector('[data-greet]');
  if(g){var h=new Date().getHours();g.textContent=h<6?'Buenas noches':h<13?'Buen día':h<20?'Buenas tardes':'Buenas noches'}
  // la caja de texto crece con lo que se escribe
  var ta=document.querySelector('.composer textarea');
  if(ta){var fit=function(){ta.style.height='auto';ta.style.height=Math.min(ta.scrollHeight,260)+'px'};ta.addEventListener('input',fit)}
  // con Enter se envía (Shift+Enter hace un salto de línea)
  if(ta)ta.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();var f=ta.form;if(f.requestSubmit)f.requestSubmit();else f.dispatchEvent(new Event('submit',{cancelable:true}))}});
})();
