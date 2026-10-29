import * as THREE from '../vendor/three.module.min.js';

// These are presentation objects, not a simulation of the production application.
export const views = {
  overview: {title:'Interface, sources and report.',copy:'Choose a view of the public interface or the fictional source-check and report examples.',href:'/case-studies/lasting-ground/',link:'Explore the project',image:'/assets/product/lasting-ground-search.png'},
  interface: {title:'Property Search',copy:'Actual public interface, captured 28 October 2026. Answers and source details require access.',href:'https://lastingground.com',link:'Open Property Search',image:'/assets/product/lasting-ground-search.png'},
  source: {title:'The source-check example',copy:'Fictional input: two validated lanes, one caution and one missing record. These are supplied states, not independently verified records.',href:'/assets/product/source-example.json',link:'View the input and output',image:'/assets/product/source-check-page-1.png'},
  report: {title:'The sample report',copy:'Two-page fictional example. Its outline is generated from the public validator and packet composer.',href:'/assets/product/source-check-example.pdf',link:'Open the two-page report',image:'/assets/product/source-check-page-2.png'}
};

export const poses = {
  overview: [[[0,3.05,1],[-.09,-.23,.025],1.12], [[-3.9,2.05,-.9],[-.12,.40,-.11],.9], [[3.9,2.2,-.8],[-.1,-.42,.10],.9]],
  interface: [[[0,2.8,1],[0,0,0],1.06], [[-4.4,1.8,-1.2],[-.12,.5,-.12],.7], [[4.5,1.8,-1.2],[-.1,-.5,.12],.7]],
  source: [[[-4.8,2.7,-2.5],[-.1,-.45,.1],.72], [[0,2.65,1.6],[0,0,0],1.28], [[4.7,1.9,-1.5],[-.1,-.55,.1],.7]],
  report: [[[-4.8,2.7,-2.5],[-.1,-.45,.1],.72], [[4.5,1.8,-1.4],[-.1,-.4,.1],.7], [[0,2.65,1.6],[0,0,0],1.22]]
};
export function ease(t){return 1-Math.pow(1-Math.max(0,Math.min(1,t)),4);}

function rounded(w,h,r){
 const x=-w/2,y=-h/2,s=new THREE.Shape();
 s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s;
}
function solid(w,h,d,r,mat){
 const geo=new THREE.ExtrudeGeometry(rounded(w,h,r),{depth:d,bevelEnabled:true,bevelSegments:5,steps:1,bevelSize:.025,bevelThickness:.025,curveSegments:12});geo.translate(0,0,-d/2);
 const mesh=new THREE.Mesh(geo,mat);mesh.castShadow=true;mesh.receiveShadow=true;return mesh;
}
function labelTexture(data){
 const canvas=document.createElement('canvas');canvas.width=900;canvas.height=1200;const c=canvas.getContext('2d');
 c.fillStyle='#e8eddf';c.fillRect(0,0,900,1200);c.fillStyle='#173d33';c.fillRect(0,0,900,19);
 c.fillStyle='#26392e';c.font='500 58px "Instrument Sans",sans-serif';c.fillText('Source check',65,130);
 c.font='27px "Instrument Sans",sans-serif';c.fillStyle='#53614f';c.fillText('Fictional public-code example',65,183);
 let y=300;
 for(const lane of data.cases.original.input.source_lanes){
  c.strokeStyle='#b9c4b0';c.lineWidth=2;c.beginPath();c.moveTo(65,y-50);c.lineTo(835,y-50);c.stroke();
  c.fillStyle='#26392e';c.font='500 32px "Instrument Sans",sans-serif';c.fillText(lane.label,65,y);
  c.font='26px "Instrument Sans",sans-serif';c.fillStyle=lane.status==='validated'?'#315a41':'#8e492c';c.fillText(lane.status[0].toUpperCase()+lane.status.slice(1),65,y+47);y+=157;
 }
 c.fillStyle='#173d33';c.fillRect(65,955,770,160);c.fillStyle='#f1f3e9';c.font='500 44px "Instrument Sans",sans-serif';c.fillText('2 warnings remain',95,1018);
 c.font='26px "Instrument Sans",sans-serif';c.fillText('Caution and missing records stay visible.',95,1071);
 const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;return texture;
}

export async function mountStudio(host){
 const canvas=host.querySelector('canvas'), fallback=host.querySelector('[data-studio-fallback]');
 const still=document.createElement('img');still.className='studio-still';still.alt='';still.setAttribute('aria-hidden','true');still.hidden=true;canvas.after(still);
 const buttons=[...host.querySelectorAll('[data-studio-view]')], title=host.querySelector('[data-studio-title]'), copy=host.querySelector('[data-studio-copy]'), link=host.querySelector('[data-studio-link]');
 let applyPose=()=>{};
 let mode='overview',renderer,disposed=false,visible=true,pending=0,motion=null,drag=null,yaw=0,tilt=0,resources=[];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const fallbackImage=fallback.querySelector('img');
 function updateText(key){const v=views[key];title.textContent=v.title;copy.textContent=v.copy;link.href=v.href;link.querySelector('span').textContent=v.link;if(key==='overview'&&location.pathname.startsWith('/case-studies/lasting-ground')){link.href='#product';link.querySelector('span').textContent='Read about the product';}fallbackImage.src=v.image;fallbackImage.alt=v.title+' '+v.copy;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.studioView===key)));host.dataset.view=key;}
 function degrade(reason){canvas.hidden=true;still.hidden=true;fallback.hidden=false;host.dataset.renderer='fallback';host.querySelector('[data-studio-hint]').textContent=reason;}
 buttons.forEach(b=>{b.disabled=false;b.addEventListener('click',()=>select(b.dataset.studioView));});
 function select(key){if(!views[key])return;mode=key;updateText(key);if(!renderer||disposed||host.dataset.renderer==='fallback')return;applyPose(key);}
 try {
  renderer=new THREE.WebGLRenderer({canvas,alpha:false,antialias:true,powerPreference:'low-power',preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
  renderer.shadowMap.enabled=false;renderer.shadowMap.type=THREE.VSMShadowMap;renderer.setClearColor(0xeeeee7,1);
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(32,1,.1,100),rig=new THREE.Group();scene.add(rig);
  const ambient=new THREE.HemisphereLight(0xfffdf4,0x718172,2.25);scene.add(ambient);
  const key=new THREE.DirectionalLight(0xfff4de,3.7);key.position.set(-6,10,7);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-10,right:10,top:10,bottom:-10,near:.5,far:30});key.shadow.normalBias=.035;key.shadow.bias=-.00025;key.shadow.radius=6;key.shadow.blurSamples=12;scene.add(key);
  const fill=new THREE.DirectionalLight(0xdce5ed,1.9);fill.position.set(8,4,-2);scene.add(fill);
  const rim=new THREE.DirectionalLight(0xffffff,2.1);rim.position.set(-3,3,-6);scene.add(rim);
  // Large luminous panels give the metal edges a controlled studio reflection.
  const envScene=new THREE.Scene();envScene.background=new THREE.Color(0xb4b9b1);
  for(const [p,s] of [[[0,7,0],[8,4]],[[7,3,2],[5,8]],[[-6,4,3],[4,9]]]){let plane=new THREE.Mesh(new THREE.PlaneGeometry(...s),new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide}));plane.position.set(...p);plane.lookAt(0,2,0);envScene.add(plane);}
  const pmrem=new THREE.PMREMGenerator(renderer);const env=pmrem.fromScene(envScene,.025);scene.environment=env.texture;resources.push(env);pmrem.dispose();envScene.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});
  // Broad, translucent contact shadows keep floating artifacts grounded without hard silhouettes.
  const shadowCanvas=document.createElement('canvas');shadowCanvas.width=shadowCanvas.height=256;
  const sc=shadowCanvas.getContext('2d'),gradient=sc.createRadialGradient(128,128,0,128,128,128);
  gradient.addColorStop(0,'rgba(32,47,37,.27)');gradient.addColorStop(.28,'rgba(32,47,37,.17)');gradient.addColorStop(.65,'rgba(32,47,37,.055)');gradient.addColorStop(1,'rgba(32,47,37,0)');sc.fillStyle=gradient;sc.fillRect(0,0,256,256);
  const shadowTexture=new THREE.CanvasTexture(shadowCanvas);resources.push(shadowTexture);
  const shadows=[];for(let i=0;i<3;i++){const m=new THREE.Mesh(new THREE.PlaneGeometry(i===0?8:4.5,4),new THREE.MeshBasicMaterial({map:shadowTexture,transparent:true,depthWrite:false,toneMapped:false}));m.rotation.x=-Math.PI/2;m.position.y=.005*i;scene.add(m);shadows.push(m);}
  const loader=new THREE.TextureLoader();const load=async url=>{const t=await loader.loadAsync(url);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());resources.push(t);return t;};
  const [screenTexture,page1,page2,data,mobileTexture]=await Promise.all([load('/assets/product/lasting-ground-search.png'),load('/assets/product/source-check-page-1.png'),load('/assets/product/source-check-page-2.png'),fetch('/assets/product/source-example.json').then(r=>{if(!r.ok)throw Error('Source example unavailable');return r.json();}),load('/assets/product/lasting-ground-search-mobile.png'),document.fonts.ready]);
  const sourceTexture=labelTexture(data);resources.push(sourceTexture);
  function face(w,h,tex,z){const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:tex,toneMapped:false}));m.position.z=z;return m;}
  const metal=new THREE.MeshPhysicalMaterial({color:0x717d73,metalness:.72,roughness:.4,clearcoat:.45,clearcoatRoughness:.3});
  const dark=new THREE.MeshStandardMaterial({color:0x15251f,metalness:.35,roughness:.55});
  const white=new THREE.MeshStandardMaterial({color:0xe8e7d8,roughness:.86});
  const screen=new THREE.Group();screen.add(solid(6.3,3.69,.18,.10,metal));screen.add(solid(6.21,3.60,.052,.075,dark));screen.children[1].position.z=.115;screen.add(face(6.07,3.415,screenTexture,.185));
  // Fine machined edge and rear ribs make thickness readable at oblique angles.
  for(let i=0;i<4;i++){let rib=new THREE.Mesh(new THREE.BoxGeometry(5.5,.015,.012),dark);rib.position.set(0,-1.50+i*.055,-.105);screen.add(rib);}
  const desktopScreen=new THREE.Group();while(screen.children.length)desktopScreen.add(screen.children[0]);screen.add(desktopScreen);
  const mobileScreen=new THREE.Group();mobileScreen.add(solid(2.54,5.43,.20,.18,metal));const mobileBezel=solid(2.47,5.36,.05,.14,dark);mobileBezel.position.z=.13;mobileScreen.add(mobileBezel);mobileScreen.add(face(2.36,5.106,mobileTexture,.19));screen.add(mobileScreen);
  const source=new THREE.Group();source.add(solid(2.55,3.4,.105,.045,metal));source.add(face(2.49,3.32,sourceTexture,.09));
  const report=new THREE.Group();
  for(let i=0;i<5;i++){let paper=solid(2.57,3.33,.013,.006,white);paper.position.set(-.016*i,.012*i,-.022*i);report.add(paper);}
  report.add(face(2.54,3.287,page1,.04));
  const rear=new THREE.Group();rear.add(solid(2.57,3.33,.015,.006,white));rear.add(face(2.54,3.287,page2,.035));rear.position.set(.32,.19,-.18);rear.rotation.z=-.08;report.add(rear);
  const groups=[screen,source,report];groups.forEach(g=>rig.add(g));
  function setPose(g,p){g.position.set(...p[0]);g.rotation.set(...p[1]);g.scale.setScalar(p[2]);}
  function resize(){const w=host.querySelector('[data-studio-stage]').clientWidth,h=host.querySelector('[data-studio-stage]').clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();desktopScreen.visible=w>=580;mobileScreen.visible=w<580;if(host.dataset.renderer!=='fallback')host.querySelector('[data-studio-hint]').textContent=w<580||reduced.matches||!matchMedia('(hover: hover) and (pointer: fine)').matches?'Select a view to inspect':'Drag to turn · select a view to inspect';}
  function cameraPose(){const narrow=canvas.clientWidth<580;const overview=mode==='overview';const span=narrow?(overview?18:11.8):(overview?13.2:11.9);camera.position.set(overview?2.4:0,overview?5.3:3.7,span);camera.lookAt(0,2.6,0);}
  function draw(){if(disposed||host.dataset.renderer==='fallback')return;cameraPose();rig.rotation.y=yaw;rig.rotation.x=tilt;groups.forEach((g,i)=>{shadows[i].position.x=g.position.x;shadows[i].position.z=g.position.z;shadows[i].scale.setScalar(g.scale.x);});renderer.render(scene,camera);if(!motion&&!drag){still.src=canvas.toDataURL('image/png');still.hidden=false;}}
  function frame(now){pending=0;if(disposed||!visible||document.hidden)return;if(motion){const t=Math.min(1,(now-motion.started)/650),e=ease(t);for(let i=0;i<groups.length;i++){const g=groups[i],a=motion.from[i],b=poses[mode][i];g.position.lerpVectors(a.p,new THREE.Vector3(...b[0]),e);g.quaternion.slerpQuaternions(a.q,new THREE.Quaternion().setFromEuler(new THREE.Euler(...b[1])),e);g.scale.setScalar(a.s+(b[2]-a.s)*e);}if(t===1){motion=null;host.dataset.motion='idle';}}draw();if(motion)request();}
  function request(){if(!pending&&!disposed&&visible&&!document.hidden)pending=requestAnimationFrame(frame);}
  applyPose=key=>{still.hidden=true;yaw=0;tilt=0;host.dataset.motion=reduced.matches?'idle':'moving';if(reduced.matches){groups.forEach((g,i)=>setPose(g,poses[key][i]));motion=null;request();}else{motion={started:performance.now(),from:groups.map(g=>({p:g.position.clone(),q:g.quaternion.clone(),s:g.scale.x}))};request();}}
  groups.forEach((g,i)=>setPose(g,poses[mode][i]));canvas.hidden=false;resize();draw();fallback.hidden=true;host.dataset.renderer='webgl';host.dataset.motion='idle';host.querySelector('[data-studio-hint]').textContent=(canvas.clientWidth<580||reduced.matches||!matchMedia('(hover: hover) and (pointer: fine)').matches)?'Select a view to inspect':'Drag to turn · select a view to inspect';
  const ro=new ResizeObserver(()=>{resize();draw();request();});ro.observe(host.querySelector('[data-studio-stage]'));
  const io=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible){request();}else{cancelAnimationFrame(pending);pending=0;}},{rootMargin:'80px'});io.observe(host);
  function onVisibility(){if(document.hidden){cancelAnimationFrame(pending);pending=0;}else request();}document.addEventListener('visibilitychange',onVisibility);
  function onReduced(){if(reduced.matches){motion=null;groups.forEach((g,i)=>setPose(g,poses[mode][i]));yaw=tilt=0;request();}}reduced.addEventListener('change',onReduced);
  canvas.addEventListener('pointerdown',e=>{if(e.pointerType==='touch'||reduced.matches)return;still.hidden=true;drag={x:e.clientX,y:e.clientY,yaw,tilt,moved:false};canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing';});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;if(Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>5)drag.moved=true;yaw=Math.max(-.5,Math.min(.5,drag.yaw+(e.clientX-drag.x)*.004));tilt=Math.max(-.14,Math.min(.14,drag.tilt+(e.clientY-drag.y)*.002));request();});
  function stop(e){if(drag&&!drag.moved&&e.type==='pointerup'){const rect=canvas.getBoundingClientRect(),ray=new THREE.Raycaster();ray.setFromCamera(new THREE.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);const hits=ray.intersectObjects(groups,true).filter(h=>{let o=h.object;while(o){if(!o.visible)return false;o=o.parent;}return true;});if(hits.length){let o=hits[0].object;while(o.parent!==rig)o=o.parent;select(['interface','source','report'][groups.indexOf(o)]);}}drag=null;canvas.style.cursor='grab';request();}canvas.addEventListener('pointerup',stop);canvas.addEventListener('pointercancel',stop);
  canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home'].includes(e.key))return;e.preventDefault();const keys=Object.keys(views),next=e.key==='Home'?'overview':keys[(keys.indexOf(mode)+(e.key==='ArrowRight'?1:3))%4];select(next);});
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(pending);pending=0;degrade('3D is unavailable here. The original artifacts remain available.');});
  window.addEventListener('pagehide',event=>{if(event.persisted){cancelAnimationFrame(pending);pending=0;return;}disposed=true;cancelAnimationFrame(pending);ro.disconnect();io.disconnect();document.removeEventListener('visibilitychange',onVisibility);reduced.removeEventListener('change',onReduced);scene.traverse(o=>{o.geometry?.dispose();if(o.material)(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>m.dispose());});resources.forEach(t=>t.dispose());renderer.dispose();});window.addEventListener('pageshow',event=>{if(event.persisted&&!disposed){resize();request();}});
 }catch{renderer?.dispose();renderer=null;degrade('3D is unavailable here. The original artifacts remain available.');}
}

for(const host of document.querySelectorAll('[data-product-studio]'))mountStudio(host);
