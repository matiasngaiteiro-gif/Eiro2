/* EIRO · comportamiento compartido por todas las páginas.
   Clave de acceso, hora de Buenos Aires, menú, GAITEIRO → EIRO, palabra que rota, revelados y sección actual. */
(function(){
  var root=document.documentElement, RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches, started=false;
  var behind=[].slice.call(document.querySelectorAll('body > header, body > main, body > footer'));

  // acceso con clave · cortina de "en construcción", no seguridad: la clave se ve en el código
  var gate=document.getElementById('gate'), form=document.getElementById('gateForm'), key=document.getElementById('gateKey');
  function setInert(on){behind.forEach(function(el){if(on){el.setAttribute('inert','');el.setAttribute('aria-hidden','true')}else{el.removeAttribute('inert');el.removeAttribute('aria-hidden')}})}
  function open(){if(gate)gate.hidden=true;root.classList.remove('locked');root.classList.add('unlocked');setInert(false);start()}
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(key.value.trim()==='4354'){try{localStorage.setItem('eiro-acceso','1')}catch(err){} open()}
      else{form.classList.remove('err');void form.offsetWidth;form.classList.add('err');key.value='';key.focus()}
    });
    key.addEventListener('input',function(){if(key.value.length===4)form.requestSubmit?form.requestSubmit():form.dispatchEvent(new Event('submit',{cancelable:true}))});
  }

  // hora de Buenos Aires
  var clock=document.getElementById('clock');
  function tick(){try{clock.textContent=new Intl.DateTimeFormat('es-AR',{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:'America/Argentina/Buenos_Aires'}).format(new Date())+' BUE'}catch(e){}}
  if(clock){tick(); setInterval(tick,15000)}

  // menú a pantalla completa
  var menu=document.getElementById('menu'), mBtn=document.getElementById('menuBtn'), mClose=document.getElementById('menuClose');
  var menuLinks=menu?[].slice.call(menu.querySelectorAll('nav a')):[];
  function setMenu(on){
    if(on){menu.hidden=false;void menu.offsetWidth;menu.classList.add('open');root.classList.add('menu-open');mBtn.setAttribute('aria-expanded','true');behind.forEach(function(el){el.setAttribute('inert','')});setTimeout(function(){menuLinks[0].focus()},60)}
    else{menu.classList.remove('open');root.classList.remove('menu-open');mBtn.setAttribute('aria-expanded','false');behind.forEach(function(el){el.removeAttribute('inert')});setTimeout(function(){if(!menu.classList.contains('open'))menu.hidden=true},RM?0:350);mBtn.focus()}
  }
  if(menu){
    mBtn.addEventListener('click',function(){setMenu(true)});
    mClose.addEventListener('click',function(){setMenu(false)});
    menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.classList.contains('open'))setMenu(false)});
  }

  function start(){
    if(started) return; started=true;

    // GAITEIRO: ocupa el ancho de su marco; después se borra GAIT y queda EIRO
    var origin=document.getElementById('origin');
    if(origin){
      var fitOrigin=function(){
        var probe=document.createElement('span'); probe.textContent='GAITEIRO';
        probe.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;letter-spacing:-.05em;font:700 100px/1 '+getComputedStyle(origin).fontFamily;
        document.body.appendChild(probe); var ratio=probe.getBoundingClientRect().width/100; probe.remove();
        var avail=origin.parentNode.clientWidth-2*parseFloat(getComputedStyle(origin).left);
        if(ratio>0) origin.style.fontSize=Math.min(380,Math.floor(avail/ratio))+'px';
      };
      var go=function(){fitOrigin();setTimeout(function(){origin.classList.add('is-in')},RM?0:500)};
      if(origin.hasAttribute('data-wait')){ // en páginas internas espera a estar en pantalla
        fitOrigin();
        if('IntersectionObserver' in window&&!RM){var oo=new IntersectionObserver(function(es){if(es[0].isIntersecting){oo.disconnect();(document.fonts?document.fonts.ready:Promise.resolve()).then(go)}},{threshold:.5});oo.observe(origin.parentNode)}else{go()}
      }else{(document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(go)}
      window.addEventListener('resize',fitOrigin);
    }

    // la palabra que rota: recorre los adjetivos una vez y se queda en el último
    var rot=document.getElementById('rot');
    if(rot && !RM){
      var OUT_MS=(parseFloat(getComputedStyle(root).getPropertyValue('--dur-2'))||.35)*1000;
      var words=['inolvidables.','inconfundibles.','deseadas.','auténticas.','rentables.'], wi=0;
      var timer=setInterval(function(){
        if(document.hidden) return;
        if(wi>=words.length-2) clearInterval(timer);
        rot.classList.remove('in'); rot.classList.add('out');
        setTimeout(function(){wi++; rot.textContent=words[wi]; rot.classList.remove('out'); void rot.offsetWidth; rot.classList.add('in')},OUT_MS);
      },2400);
    }

    // revelados · las imágenes arrancan recortadas (clip-path) y el navegador no las cuenta como visibles: se observa su contenedor
    var rev=[].slice.call(document.querySelectorAll('[data-reveal]'));
    function shown(el){el.classList.add('is-in')}
    if(RM || !('IntersectionObserver' in window)){rev.forEach(shown)}
    else{
      var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){shown(e.target.__rev||e.target);ro.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.12});
      rev.forEach(function(el){var t=el.classList.contains('media')?el.parentElement:el; t.__rev=el; ro.observe(t)});
    }

    // placas con scroll: cada [data-scrub] recibe --p de 0 a 1 según cuánto se recorrió;
    // las altas (con .stick) cuentan desde que llegan arriba, las "free" desde que entran hasta que salen
    var scr=[].slice.call(document.querySelectorAll('[data-scrub]'));
    if(scr.length){
      var paint=function(el,p){
        el.style.setProperty('--p',p.toFixed(4));
        var ws=el.__w||(el.__w=[].slice.call(el.querySelectorAll('.wd')));
        if(ws.length){var from=parseFloat(el.getAttribute('data-from')||'0'),q=Math.max(0,(p-from)/(1-from)),n=Math.ceil(q*1.15*ws.length);for(var i=0;i<ws.length;i++)ws[i].classList.toggle('on',i<n)}
      };
      if(RM){scr.forEach(function(el){paint(el,el.getAttribute('data-scrub')==='free'?.5:1)})}
      else{
        var ticking=false;
        var upd=function(){ticking=false;var vh=innerHeight;scr.forEach(function(el){
          var r=el.getBoundingClientRect(),p;
          if(el.getAttribute('data-scrub')==='free'){p=(vh-r.top)/(vh+r.height)}
          else{var t=el.offsetHeight-vh;p=t>0?-r.top/t:1}
          paint(el,Math.min(1,Math.max(0,p)));
        })};
        var req=function(){if(!ticking){ticking=true;requestAnimationFrame(upd)}};
        window.addEventListener('scroll',req,{passive:true});window.addEventListener('resize',req);upd();
      }
    }

    // piezas en movimiento: solo se animan cuando están en pantalla; el botón las pausa (WCAG 2.2.2)
    [].slice.call(document.querySelectorAll('.reels')).forEach(function(r){
      var btn=r.parentNode.querySelector('[data-pause]');
      if(btn) btn.addEventListener('click',function(){var p=r.classList.toggle('paused');btn.textContent=p?'Reproducir':'Pausar';btn.setAttribute('aria-pressed',p?'true':'false')});
      if(RM){r.classList.add('paused');return}
      if('IntersectionObserver' in window){new IntersectionObserver(function(es){r.classList.toggle('play',es[0].isIntersecting)},{threshold:.1}).observe(r)}else{r.classList.add('play')}
    });

    // la cápsula dice en qué sección estás (solo en el inicio, que tiene varias)
    var where=document.getElementById('where'), secs=[].slice.call(document.querySelectorAll('main [data-label]'));
    if(where && secs.length && 'IntersectionObserver' in window){
      var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting) where.textContent=e.target.getAttribute('data-label')})},{rootMargin:'-45% 0px -50% 0px'});
      secs.forEach(function(s){so.observe(s)});
    }
  }

  if(root.classList.contains('unlocked')||!gate){open()}else{root.classList.add('locked');setInert(true);setTimeout(function(){key.focus()},100)}
})();
