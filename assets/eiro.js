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

  // testimonios: un recuadro que se desliza (dedo, arrastre con mouse, flechas y teclado)
  [].slice.call(document.querySelectorAll('[data-tq]')).forEach(function(tq){
    var tr=tq.querySelector('.tq-track'),n=tr.children.length,bars=[].slice.call(tq.querySelectorAll('.tq-bars i')),num=tq.querySelector('[data-tq-n]'),cur=0;
    function idx(){return Math.round(tr.scrollLeft/tr.clientWidth)}
    function go(i){i=(i+n)%n;tr.scrollTo({left:i*tr.clientWidth,behavior:RM?'auto':'smooth'})}
    function paint(){var i=Math.max(0,Math.min(n-1,idx()));if(i===cur&&num.textContent==String(i+1))return;cur=i;num.textContent=i+1;bars.forEach(function(b,k){b.classList.toggle('on',k<=i)});[].forEach.call(tr.children,function(s,k){s.setAttribute('aria-hidden',k===i?'false':'true')})}
    var raf=0;tr.addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(function(){raf=0;paint()})},{passive:true});
    tq.querySelector('[data-tq-prev]').addEventListener('click',function(){go(idx()-1)});
    tq.querySelector('[data-tq-next]').addEventListener('click',function(){go(idx()+1)});
    tr.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){e.preventDefault();go(idx()-1)}if(e.key==='ArrowRight'){e.preventDefault();go(idx()+1)}});
    // arrastre con mouse (en táctil el desplazamiento es nativo)
    var down=false,x0=0,s0=0,moved=false;
    tr.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=false;x0=e.clientX;s0=tr.scrollLeft;tr.classList.add('drag')});
    addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-x0;if(Math.abs(dx)>4)moved=true;tr.scrollLeft=s0-dx});
    addEventListener('pointerup',function(){if(!down)return;down=false;var d=tr.scrollLeft-s0,i=Math.round(s0/tr.clientWidth);if(d>tr.clientWidth*.15)i++;else if(d<-tr.clientWidth*.15)i--;go(Math.max(0,Math.min(n-1,i)));setTimeout(function(){tr.classList.remove('drag')},RM?0:600)});
    tr.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
    addEventListener('resize',function(){tr.scrollLeft=cur*tr.clientWidth});
    paint();
  });

  // formulario breve: arma el mensaje con lo elegido y abre WhatsApp con el estudio
  var brief=document.getElementById('brief');
  if(brief){
    var msg=brief.querySelector('textarea'),nameIn=brief.querySelector('[name=nombre]'),err=document.getElementById('brief-err');
    try{var pre=new URLSearchParams(location.search).get('necesito');if(pre)[].slice.call(brief.querySelectorAll('[name=necesito]')).forEach(function(x){if(x.value===pre)x.checked=true})}catch(e){}
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

    // portada: la última palabra del título cambia letra por letra (las letras salen por arriba y entran desde abajo)
    var sw=document.querySelector('[data-swap]');
    if(sw&&!RM){
      var vis=sw.querySelector('.swap-vis'),words=sw.getAttribute('data-swap').split('|'),wi=0;
      var paintW=function(w,cls){vis.innerHTML='';w.split('').forEach(function(c,n){var s=document.createElement('span');s.className='ch '+(cls||'');s.textContent=c;s.style.animationDelay=(n*.035)+'s';vis.appendChild(s)})};
      var measure=function(w){var m=document.createElement('span');m.style.cssText='position:absolute;visibility:hidden;white-space:pre';m.textContent=w;sw.appendChild(m);var x=m.getBoundingClientRect().width;m.remove();return x};
      paintW(words[0]);vis.style.width=measure(words[0])+'px';
      setInterval(function(){
        if(document.hidden)return;
        [].forEach.call(vis.children,function(c){c.classList.add('out')});
        var next=words[wi=(wi+1)%words.length];
        setTimeout(function(){vis.style.width=measure(next)+'px';paintW(next,'in')},450+vis.children.length*35);
      },2800);
      addEventListener('resize',function(){vis.style.width=measure(vis.textContent)+'px'});
      // la tipografía llega después: se vuelve a medir para que la palabra no quede cortada
      if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){vis.style.width=measure(vis.textContent)+'px'});
    }

    // portada: los mockups pasan como un GIF (cortes secos); se pausa con el botón, fuera de pantalla o con movimiento reducido
    var reel=document.querySelector('[data-reel]');
    if(reel){
      var fr=[].slice.call(reel.querySelectorAll('img')),pb=reel.querySelector('[data-reel-pause]'),k=0,paused=RM,reelOn=true;
      var show=function(n){fr[k].classList.remove('on');k=(n+fr.length)%fr.length;fr[k].classList.add('on')};
      if(pb){if(RM){pb.textContent='Reproducir';pb.setAttribute('aria-pressed','true')}
        pb.addEventListener('click',function(e){e.stopPropagation();paused=!paused;pb.textContent=paused?'Reproducir':'Pausar';pb.setAttribute('aria-pressed',paused?'true':'false')})}
      if('IntersectionObserver' in window)new IntersectionObserver(function(es){reelOn=es[0].isIntersecting}).observe(reel);
      setInterval(function(){if(!paused&&reelOn&&!document.hidden&&(!document.getElementById('player')||document.getElementById('player').hidden))show(k+1)},750);
    }

    // reel: el círculo "Ver reel" sigue al cursor dentro del video; al tocarlo se abre a pantalla completa con sonido
    var frame=document.querySelector('[data-player]'),player=document.getElementById('player');
    if(frame&&player){
      var orbP=frame.querySelector('[data-play]'),pv=player.querySelector('video'),closeB=player.querySelector('[data-close]'),prev=frame.querySelector('video');
      if(RM&&prev){prev.removeAttribute('autoplay');prev.pause()}
      var fine=window.matchMedia('(hover:hover) and (pointer:fine)').matches;
      if(fine){
        frame.classList.add('idle');
        frame.addEventListener('pointermove',function(e){var r=frame.getBoundingClientRect();frame.classList.remove('idle');orbP.style.setProperty('--ox',(e.clientX-r.left)+'px');orbP.style.setProperty('--oy',(e.clientY-r.top)+'px')});
        frame.addEventListener('pointerleave',function(){frame.classList.add('idle');orbP.style.removeProperty('--ox');orbP.style.removeProperty('--oy')});
      }
      var lastF=null;
      var openP=function(){lastF=document.activeElement;player.hidden=false;void player.offsetWidth;player.classList.add('open');root.classList.add('player-open');behind.forEach(function(el){el.setAttribute('inert','')});if(prev)prev.pause();pv.currentTime=0;var pr=pv.play();if(pr&&pr.catch)pr.catch(function(){});closeB.focus()};
      var closeP=function(){pv.pause();player.classList.remove('open');root.classList.remove('player-open');behind.forEach(function(el){el.removeAttribute('inert')});setTimeout(function(){player.hidden=true},RM?0:350);if(prev&&!RM){var q=prev.play();if(q&&q.catch)q.catch(function(){})}if(lastF)lastF.focus()};
      frame.addEventListener('click',openP);
      closeB.addEventListener('click',closeP);
      pv.addEventListener('ended',closeP);
      document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!player.hidden)closeP()});
      player.addEventListener('keydown',function(e){if(e.key!=='Tab')return;var f=[pv,closeB];var a=f.indexOf(document.activeElement);if(e.shiftKey&&a<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&a===f.length-1){e.preventDefault();f[0].focus()}});
      if('IntersectionObserver' in window&&prev)new IntersectionObserver(function(es){if(RM||!player.hidden)return;if(es[0].isIntersecting){var q=prev.play();if(q&&q.catch)q.catch(function(){})}else prev.pause()}).observe(frame);
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

// el botón de WhatsApp se esconde sobre el inicio y sobre el cierre, donde ya hay botones
(function(){
  var orb=document.getElementById('waOrb');if(!orb||!('IntersectionObserver' in window))return;
  var zones=[].slice.call(document.querySelectorAll('.hero,.cta,#brief'));if(!zones.length)return;
  var on=new Set();
  var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?on.add(e.target):on.delete(e.target)});document.documentElement.classList.toggle('wa-hide',on.size>0)},{threshold:.25});
  zones.forEach(function(z){io.observe(z)});
})();

// el óvalo de la marca: con movimiento reducido el texto queda quieto
(function(){
  if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  [].forEach.call(document.querySelectorAll('svg.seal'),function(s){if(s.pauseAnimations)s.pauseAnimations()});
})();
