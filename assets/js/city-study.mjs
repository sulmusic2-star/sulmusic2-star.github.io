import * as THREE from '../vendor/three.module.min.js';

// A bounded portfolio study of a public municipal snapshot. It is not a product map.
export function heightValue(attributes) {
  const v=attributes.ELEVATION_GROUND_LEVEL;
  return Number.isFinite(v)&&v>0?v:null;
}
export function projectXY(point,bounds,scale=200) {
  return [(point[0]-(bounds[0]+bounds[2])/2)/scale,(point[1]-(bounds[1]+bounds[3])/2)/scale];
}
export function signedArea(ring) {
  return ring.reduce((a,p,i)=>{const q=ring[(i+1)%ring.length];return a+p[0]*q[1]-q[0]*p[1];},0)/2;
}

async function mount(host) {
 const canvas=host.querySelector('canvas'),status=host.querySelector('[data-city-status]');
 const modes=[...host.querySelectorAll('[data-city-mode]')],select=host.querySelector('select');
 let renderer,raf=0,disposed=false,mode='volume',yaw=-.28,drag=null,motion=null,active=null;
 const reduce=matchMedia('(prefers-reduced-motion: reduce)');
 function fallback(message){canvas.hidden=true;host.dataset.state='fallback';status.textContent=message;modes.forEach(x=>x.disabled=true);host.querySelector('[data-city-reset]').disabled=true;}
 try {
  const response=await fetch('/assets/data/boston-buildings.json');if(!response.ok)throw new Error('data');
  const data=await response.json();
  host.querySelector('[data-city-count]').textContent=data.features.length;
  const features=data.features.filter(f=>f.geometry?.rings?.length);
  select.replaceChildren(...features.map(f=>new Option('Building '+f.attributes.OBJECTID,f.attributes.OBJECTID)));
  const initial=features.slice().sort((a,b)=>(heightValue(b.attributes)||0)-(heightValue(a.attributes)||0))[0];
  function showRecord(feature) {
    const a=feature.attributes,h=heightValue(a);select.value=String(a.OBJECTID);
    host.querySelector('[data-object-id]').textContent=a.OBJECTID;
    host.querySelector('[data-object-height]').textContent=h===null?'Not supplied':h.toFixed(1)+' ft';
    host.querySelector('[data-object-type]').textContent=a.IEL_TYPE||'Not supplied';
    const u=new URL(data.sourceUrl+'/query');u.search=new URLSearchParams({where:'OBJECTID='+a.OBJECTID,outFields:'OBJECTID,ELEVATION_GROUND_LEVEL,IEL_TYPE',returnGeometry:'true',f:'pjson'});
    host.querySelector('[data-object-source]').href=u.href;
    host.dataset.selected=String(a.OBJECTID);
  }
  showRecord(initial);
  select.disabled=false;
  // Source rows remain usable even if WebGL is unavailable.
  select.addEventListener('change',()=>{const f=features.find(f=>String(f.attributes.OBJECTID)===select.value);if(f){showRecord(f);highlight(f.attributes.OBJECTID);}});
  let highlight=()=>{};
  renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'low-power',preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.18;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  const scene=new THREE.Scene(),camera=new THREE.OrthographicCamera(-10,10,8,-8,.1,100),rig=new THREE.Group();scene.add(rig);
  scene.add(new THREE.HemisphereLight(0xf1f7ff,0x536281,2.4));
  const sun=new THREE.DirectionalLight(0xffffff,3.8);sun.position.set(-8,18,9);sun.castShadow=true;
  sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-12,right:12,top:12,bottom:-12,near:1,far:50});sun.shadow.bias=-.0003;sun.shadow.normalBias=.025;scene.add(sun);
  const rim=new THREE.DirectionalLight(0x729dff,2.8);rim.position.set(12,6,-9);scene.add(rim);
  const base=new THREE.Mesh(new THREE.BoxGeometry((data.bounds[2]-data.bounds[0])/200+.16,.16,(data.bounds[3]-data.bounds[1])/200+.16),new THREE.MeshStandardMaterial({color:0x9eabc4,roughness:.55,metalness:.2}));base.position.y=-.12;base.receiveShadow=true;rig.add(base);
  const top=new THREE.Mesh(new THREE.PlaneGeometry(base.geometry.parameters.width,base.geometry.parameters.depth),new THREE.MeshStandardMaterial({color:0xc8d2e2,roughness:.9}));top.rotation.x=-Math.PI/2;top.position.y=-.03;top.receiveShadow=true;rig.add(top);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.ShadowMaterial({opacity:.19}));ground.rotation.x=-Math.PI/2;ground.position.y=-.22;scene.add(ground);
  const meshes=[],edgeGroups=[];
  const wall=new THREE.MeshStandardMaterial({color:0xa9bbd7,roughness:.56,metalness:.16});
  const roof=new THREE.MeshStandardMaterial({color:0xf2f4fa,roughness:.7,metalness:.06});
  const selectedWall=new THREE.MeshStandardMaterial({color:0x1546dd,roughness:.38,metalness:.25});
  const selectedRoof=new THREE.MeshStandardMaterial({color:0x5385ff,roughness:.3,metalness:.16});
  const edgeMat=new THREE.LineBasicMaterial({color:0x7189b4,transparent:true,opacity:.35});
  for(const feature of features) {
   const rings=feature.geometry.rings.filter(r=>r.length>=4),outers=rings.filter(r=>signedArea(r)<0),holes=rings.filter(r=>signedArea(r)>0);
   for(const outer of (outers.length?outers:rings)) {
    const points=outer.map(p=>new THREE.Vector2(...projectXY(p,data.bounds)));
    const shape=new THREE.Shape(points);
    // ArcGIS exterior rings are clockwise. Associate holes by point inclusion.
    const inside=(point,ring)=>{let hit=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[i],b=ring[j];if((a[1]>point[1])!==(b[1]>point[1])&&point[0]<(b[0]-a[0])*(point[1]-a[1])/(b[1]-a[1])+a[0])hit=!hit;}return hit;};
    for(const hole of holes)if(inside(hole[0],outer))shape.holes.push(new THREE.Path(hole.map(p=>new THREE.Vector2(...projectXY(p,data.bounds)))));
    const height=heightValue(feature.attributes),geo=new THREE.ExtrudeGeometry(shape,{depth:height===null?.012:height/200,bevelEnabled:false,steps:1});geo.rotateX(-Math.PI/2);
    const mesh=new THREE.Mesh(geo,[roof,wall]);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.feature=feature;rig.add(mesh);meshes.push(mesh);
    const edges=new THREE.LineSegments(new THREE.EdgesGeometry(geo,25),edgeMat);rig.add(edges);edgeGroups.push(edges);
   }
  }
  let volume=1,viewRatio=1,viewSpan=7.7;const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();
  function draw(){raf=0;if(disposed)return;if(motion){const t=reduce.matches?1:Math.min(1,(performance.now()-motion.start)/650),e=1-Math.pow(1-t,4);volume=motion.from+(motion.to-motion.from)*e;if(t===1)motion=null;else schedule();}
   meshes.forEach(m=>m.scale.y=Math.max(.004,volume));edgeGroups.forEach(m=>m.scale.y=Math.max(.004,volume));rig.rotation.y=yaw;
   const plan=1-volume,target=new THREE.Vector3(0,.2,0);let span=viewSpan;
   if(mode==='inspect'&&active!==null){rig.updateMatrixWorld(true);const bounds=new THREE.Box3();for(const m of meshes)if(m.userData.feature.attributes.OBJECTID===active)bounds.union(new THREE.Box3().setFromObject(m));if(!bounds.isEmpty()){bounds.getCenter(target);const size=bounds.getSize(new THREE.Vector3());span=Math.max(.65,size.length()*.72)/Math.min(1,viewRatio);}}
   camera.left=-span*viewRatio;camera.right=span*viewRatio;camera.top=span;camera.bottom=-span;camera.updateProjectionMatrix();
   camera.position.copy(target).add(new THREE.Vector3(12*(1-plan),15+plan*10,16*(1-plan)+.001));camera.lookAt(target);renderer.render(scene,camera);
  }
  function schedule(){if(!raf&&!disposed)raf=requestAnimationFrame(draw);}
  highlight=id=>{active=id;meshes.forEach(m=>m.material=m.userData.feature.attributes.OBJECTID===id?[selectedRoof,selectedWall]:[roof,wall]);schedule();};
  function setMode(value){mode=value;host.dataset.mode=mode;modes.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.cityMode===mode)));motion={from:volume,to:mode==='plan'?0:1,start:performance.now()};status.textContent=mode==='inspect'?'Close view of the selected building. Choose another record or reset the view.':mode==='plan'?'Plan view. Select a building to inspect its municipal record.':'Drag to rotate. Select a building to inspect its municipal record.';schedule();}
  modes.forEach(b=>{b.disabled=false;b.addEventListener('click',()=>setMode(b.dataset.cityMode));});
  host.querySelector('[data-city-reset]').disabled=false;host.querySelector('[data-city-reset]').addEventListener('click',()=>{yaw=-.28;setMode('volume');showRecord(initial);highlight(initial.attributes.OBJECTID);});
  function resize(){const box=canvas.getBoundingClientRect(),w=Math.max(1,box.width),h=Math.max(1,box.height);renderer.setSize(w,h,false);viewRatio=w/h;viewSpan=w<620?Math.max(8.8,11/viewRatio):7.7;schedule();}
  const observer=new ResizeObserver(resize);observer.observe(canvas);
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,yaw,moved:false};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;const delta=e.clientX-drag.x;if(Math.abs(delta)+Math.abs(e.clientY-drag.y)>5)drag.moved=true;if(mode!=='plan'){yaw=drag.yaw+delta*.005;schedule();}});
  canvas.addEventListener('pointerup',e=>{if(!drag)return;if(!drag.moved){const rect=canvas.getBoundingClientRect();pointer.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes,false)[0];if(hit){const f=hit.object.userData.feature;showRecord(f);highlight(f.attributes.OBJECTID);}}drag=null;if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);});
  canvas.addEventListener('pointercancel',()=>drag=null);
  canvas.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();yaw+=(e.key==='ArrowLeft'?-.12:.12);schedule();}else if(e.key==='Home'){e.preventDefault();yaw=-.28;schedule();}});
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();disposed=true;cancelAnimationFrame(raf);fallback('3D view unavailable. The source selector and project links remain available.');});
  window.addEventListener('pagehide',()=>{cancelAnimationFrame(raf);raf=0;});window.addEventListener('pageshow',()=>schedule());
  reduce.addEventListener('change',()=>schedule());
  host.dataset.state='ready';canvas.hidden=false;highlight(initial.attributes.OBJECTID);resize();
  status.textContent='Drag to rotate. Select a building to inspect its municipal record.';
 } catch(error) { fallback('The interactive view could not load. Read the study data or explore the product below.'); }
}
const host=typeof document!=='undefined'?document.querySelector('[data-city-study]'):null;if(host)mount(host);
