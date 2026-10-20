/* EIRO · comportamiento compartido por todas las páginas.
   Clave de acceso, barra, menú, WhatsApp magnético, testimonios, formulario, palabra que rota, revelados y sección actual. */
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

  // barra: una línea fina debajo cuando la página ya bajó
  function scrolled(){root.classList.toggle('scrolled',scrollY>8)}
  addEventListener('scroll',scrolled,{passive:true});scrolled();

  // WhatsApp: el círculo se acerca al cursor cuando pasa cerca (solo con mouse y sin movimiento reducido)
  var orb=document.getElementById('waOrb');
  if(orb&&!RM&&window.matchMedia('(hover:hover) and (pointer:fine)').matches){
    var R=140,PULL=.4,raf=0,mx=0,my=0;
    addEventListener('pointermove',function(e){
      mx=e.clientX;my=e.clientY;
      if(raf)return; raf=requestAnimationFrame(function(){raf=0;
        var r=orb.getBoundingClientRect(),cx=r.left+r.width/2-(parseFloat(orb.style.getPropertyValue('--mx'))||0),cy=r.top+r.height/2-(parseFloat(orb.style.getPropertyValue('--my'))||0);
        var dx=mx-cx,dy=my-cy,d=Math.sqrt(dx*dx+dy*dy);
        if(d<R){orb.classList.add('near');orb.style.setProperty('--mx',(dx*PULL).toFixed(1)+'px');orb.style.setProperty('--my',(dy*PULL).toFixed(1)+'px')}
        else if(orb.classList.contains('near')){orb.classList.remove('near');orb.style.setProperty('--mx','0px');orb.style.setProperty('--my','0px')}
      });
    },{passive:true});
    document.addEventListener('pointerleave',function(){orb.classList.remove('near');orb.style.setProperty('--mx','0px');orb.style.setProperty('--my','0px')});
  }

  // testimonios: uno por vez, con flechas, teclado y deslizando el dedo
  [].slice.call(document.querySelectorAll('[data-tq]')).forEach(function(tq){
    var sl=[].slice.call(tq.querySelectorAll('.tq-slide')),bars=[].slice.call(tq.querySelectorAll('.tq-bars i')),num=tq.querySelector('[data-tq-n]'),i=0;
    function go(n){sl[i].hidden=true;sl[i].classList.remove('in');i=(n+sl.length)%sl.length;sl[i].hidden=false;if(!RM)sl[i].classList.add('in');bars.forEach(function(b,k){b.classList.toggle('on',k<=i)});num.textContent=i+1}
    tq.querySelector('[data-tq-prev]').addEventListener('click',function(){go(i-1)});
    tq.querySelector('[data-tq-next]').addEventListener('click',function(){go(i+1)});
    tq.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')go(i-1);if(e.key==='ArrowRight')go(i+1)});
    var x0=null;
    tq.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    tq.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)go(dx<0?i+1:i-1);x0=null},{passive:true});
  });

  // formulario breve: arma el mensaje con lo elegido y abre WhatsApp con el estudio
  var brief=document.getElementById('brief');
  if(brief){
    var msg=brief.querySelector('textarea'),nameIn=brief.querySelector('[name=nombre]'),err=document.getElementById('brief-err');
    [].slice.call(brief.querySelectorAll('[data-fill]')).forEach(function(b){
      b.addEventListener('click',function(){var t=b.getAttribute('data-fill');if(msg.value.indexOf(t)<0)msg.value=(msg.value.trim()?msg.value.trim()+' ':'')+t;msg.focus()});
    });
    nameIn.addEventListener('input',function(){if(nameIn.value.trim()){nameIn.removeAttribute('aria-invalid');err.textContent=''}});
    brief.addEventListener('submit',function(e){
      e.preventDefault();
      var nombre=nameIn.value.trim();
      if(!nombre){nameIn.setAttribute('aria-invalid','true');err.textContent='Contanos tu nombre así sabemos con quién hablamos.';nameIn.focus();return}
      var marca=brief.querySelector('[name=marca]').value.trim();
      var nec=[].slice.call(brief.querySelectorAll('[name=necesito]:checked')).map(function(x){return x.value});
      var cu=brief.querySelector('[name=cuando]:checked');
      var lines=['¡Hola, Eiro! Soy '+nombre+(marca?', de '+marca:'')+'.'];
      if(nec.length)lines.push('Necesito: '+nec.join(', ').toLowerCase()+'.');
      if(cu)lines.push('Para cuándo: '+cu.value.toLowerCase()+'.');
      if(msg.value.trim())lines.push(msg.value.trim());
      var url='https://wa.me/'+brief.getAttribute('data-wa')+'?text='+encodeURIComponent(lines.join('\n'));
      var w=window.open(url,'_blank');
      if(w){try{w.opener=null}catch(x){}}else{location.href=url}
    });
  }

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

    // telón de entrada (inicio): EIRO sobre negro, se va por arriba y sube la web. Una vez por visita.
    var curtain=document.getElementById('curtain');
    if(curtain){
      if(root.classList.contains('no-intro')){curtain.classList.add('gone')}
      else{
        try{sessionStorage.setItem('eiro-intro','1')}catch(e){}
        root.classList.add('intro');
        setTimeout(function(){curtain.classList.add('gone');root.classList.remove('intro')},3400);
      }
    }

    // portada: los mockups pasan como un GIF; se pausa con el botón, fuera de pantalla o con movimiento reducido
    var reel=document.querySelector('[data-reel]');
    if(reel){
      var fr=[].slice.call(reel.querySelectorAll('img')),pb=document.querySelector('[data-reel-pause]'),k=0,paused=RM,vis=true;
      var show=function(n){fr[k].classList.remove('on');k=(n+fr.length)%fr.length;fr[k].classList.add('on')};
      if(pb){if(RM){pb.textContent='Reproducir';pb.setAttribute('aria-pressed','true')}
        pb.addEventListener('click',function(){paused=!paused;pb.textContent=paused?'Reproducir':'Pausar';pb.setAttribute('aria-pressed',paused?'true':'false')})}
      if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(reel);
      setInterval(function(){if(!paused&&vis&&!document.hidden)show(k+1)},750);
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
      // cada pieza arranca cuando entra en pantalla: así no se mueven todas a la vez
      [].slice.call(r.querySelectorAll('.reel')).forEach(function(el){
        if('IntersectionObserver' in window){new IntersectionObserver(function(es){el.classList.toggle('play',es[0].isIntersecting)},{threshold:.5}).observe(el)}else{el.classList.add('play')}
      });
    });

  }

  if(root.classList.contains('unlocked')||!gate){open()}else{root.classList.add('locked');setInert(true);setTimeout(function(){key.focus()},100)}
})();
