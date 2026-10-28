import * as THREE from '../vendor/three.module.min.js';
import {boundary,terrainHeight} from './spatial-model.mjs';
export function mountLandscape(host,{x=65,radius=10}={}) {
 const canvas=host.querySelector('canvas');
 const renderer=new THREE.WebGLRenderer({canvas,alpha:false,antialias:true,powerPreference:'low-power'});
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));
 renderer.setClearColor(0xdce0d6); renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.95;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 const scene=new THREE.Scene(); const camera=new THREE.OrthographicCamera(-190,190,150,-150,1,1600);
 const group=new THREE.Group();scene.add(group);
 const hemi=new THREE.HemisphereLight(0xffffff,0x718079,1.7);scene.add(hemi);
 const key=new THREE.DirectionalLight(0xfff5df,2.4);key.position.set(-130,260,130);key.castShadow=true;
 key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-230,right:230,top:230,bottom:-230,near:1,far:700}); key.shadow.normalBias=.7; key.shadow.bias=-.00015;key.shadow.radius=8;scene.add(key);
 const fill=new THREE.DirectionalLight(0xdbe4ff,.75);fill.position.set(150,90,-140);scene.add(fill);
 const ground=new THREE.Mesh(new THREE.PlaneGeometry(2200,2200),new THREE.MeshStandardMaterial({color:0xdce0d6,roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-18;ground.receiveShadow=true;scene.add(ground);
 const base=new THREE.Mesh(new THREE.BoxGeometry(240,12,240),new THREE.MeshStandardMaterial({color:0x68736d,roughness:.82}));base.position.y=-8;base.castShadow=true;base.receiveShadow=true;group.add(base);
 const geo=new THREE.PlaneGeometry(240,240,110,110);geo.rotateX(-Math.PI/2);
 const pos=geo.attributes.position; const colors=[];
 for(let i=0;i<pos.count;i++){let a=pos.getX(i),b=pos.getZ(i),h=terrainHeight(a,b);pos.setY(i,h);let c=new THREE.Color(0xc1bca6).lerp(new THREE.Color(0xe9e5d5),Math.min(1,(h-1)/23));colors.push(c.r,c.g,c.b);}
 geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geo.computeVertexNormals();
 const land=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.94,metalness:0}));land.castShadow=true;land.receiveShadow=true;group.add(land);
 // A watertight cut edge joins the terrain surface to its physical display base.
 for(const side of [0,1,2,3]){const pts=[];for(let i=0;i<=110;i++){let t=-120+i*240/110;pts.push(side===0?[t,-120]:side===1?[120,t]:side===2?[-t,120]:[-120,-t]);}const v=[];for(let i=0;i<pts.length-1;i++){let a=pts[i],b=pts[i+1];v.push(a[0],-2,a[1],b[0],-2,b[1],a[0],terrainHeight(...a),a[1],a[0],terrainHeight(...a),a[1],b[0],-2,b[1],b[0],terrainHeight(...b),b[1]);}let g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.computeVertexNormals();let m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xb4b39f,side:THREE.DoubleSide,roughness:1}));m.castShadow=true;group.add(m);}
 // Contours are calculated from this exact synthetic height field.
 const contourPositions=[]; const step=4;
 for(let level=4;level<23;level+=2)for(let a=-120;a<120;a+=step)for(let b=-120;b<120;b+=step){let c=[[a,b],[a+step,b],[a+step,b+step],[a,b+step]],hits=[];for(let i=0;i<4;i++){let p=c[i],q=c[(i+1)%4],u=terrainHeight(...p),v=terrainHeight(...q);if((u<level)!==(v<level)){let t=(level-u)/(v-u);hits.push([p[0]+t*(q[0]-p[0]),level+.12,p[1]+t*(q[1]-p[1])]);}}if(hits.length>=2)contourPositions.push(...hits[0],...hits[1]);}
 const cg=new THREE.BufferGeometry();cg.setAttribute('position',new THREE.Float32BufferAttribute(contourPositions,3));group.add(new THREE.LineSegments(cg,new THREE.LineBasicMaterial({color:0x817e66,transparent:true,opacity:.38})));
 const layer=new THREE.Group();group.add(layer);
 const shape=new THREE.Shape(boundary.map(p=>new THREE.Vector2(p[0],-p[1])));
 const floodGeo=new THREE.ExtrudeGeometry(shape,{depth:1.25,bevelEnabled:false});floodGeo.rotateX(-Math.PI/2);
 const flood=new THREE.Mesh(floodGeo,new THREE.MeshStandardMaterial({color:0x366a63,roughness:.42,metalness:.15,transparent:true,opacity:.76,side:THREE.DoubleSide}));flood.receiveShadow=true;layer.add(flood);
 const edge=new THREE.Line(new THREE.BufferGeometry().setFromPoints([...boundary,boundary[0]].map(p=>new THREE.Vector3(p[0],1.4,p[1]))),new THREE.LineBasicMaterial({color:0x204e43}));layer.add(edge);
 const marker=new THREE.Group();group.add(marker);
 const stem=new THREE.Mesh(new THREE.CylinderGeometry(.65,.65,21,12),new THREE.MeshStandardMaterial({color:0x87512e,roughness:.4,metalness:.5}));stem.position.y=10.5;marker.add(stem);
 const bead=new THREE.Mesh(new THREE.SphereGeometry(3.5,24,16),new THREE.MeshStandardMaterial({color:0xde8139,roughness:.3,metalness:.18}));bead.position.y=23;bead.castShadow=true;marker.add(bead);
 const ringGeometry=new THREE.BufferGeometry(); const ring=new THREE.LineLoop(ringGeometry,new THREE.LineBasicMaterial({color:0x9d5425}));marker.add(ring);
 const halo=new THREE.Mesh(new THREE.CircleGeometry(1,64),new THREE.MeshBasicMaterial({color:0xd08040,transparent:true,opacity:.12,depthWrite:false,side:THREE.DoubleSide}));halo.rotation.x=-Math.PI/2;halo.position.y=.25;marker.add(halo);
 let angle=.62,flat=false,exploded=false,disposed=false;const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;let pending=0;
 function render(){pending=0;if(disposed)return;const w=host.clientWidth,h=host.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);const ratio=w/h;const span=Math.max(155,185/ratio);camera.left=-span*ratio;camera.right=span*ratio;camera.top=span;camera.bottom=-span;camera.position.set(Math.sin(angle)*(flat?1:370),flat?470:290,Math.cos(angle)*(flat?1:370));camera.lookAt(0,9,0);camera.updateProjectionMatrix();layer.position.y=exploded?57:18;marker.position.set(x,layer.position.y+2,0);let rp=[];for(let i=0;i<80;i++){let a=i/80*Math.PI*2;rp.push(Math.cos(a)*radius,.3,Math.sin(a)*radius);}ringGeometry.setAttribute('position',new THREE.Float32BufferAttribute(rp,3));halo.scale.set(radius,radius,1);renderer.render(scene,camera);}
 function request(){if(!pending)pending=requestAnimationFrame(render);}
 let ro=new ResizeObserver(request);ro.observe(host);
 let down=null;canvas.addEventListener('pointerdown',e=>{if(e.pointerType==='touch')return;down={x:e.clientX,angle};canvas.setPointerCapture(e.pointerId)});canvas.addEventListener('pointermove',e=>{if(down){angle=down.angle+(e.clientX-down.x)*.007;request()}});canvas.addEventListener('pointerup',()=>down=null);canvas.addEventListener('pointercancel',()=>down=null);
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();host.dataset.webgl='lost';host.querySelector('.model-fallback').hidden=false;canvas.hidden=true;host.dispatchEvent(new CustomEvent('model-unavailable'));});
 render(); host.dataset.webgl='ready';host.querySelector('.model-fallback').hidden=true;canvas.hidden=false;
 return {update(next){if(next.x!==undefined)x=next.x;if(next.radius!==undefined)radius=next.radius;if(next.flat!==undefined)flat=next.flat;if(next.exploded!==undefined)exploded=next.exploded;if(next.rotate!==undefined)angle+=next.rotate;reduced?render():request()},dispose(){disposed=true;cancelAnimationFrame(pending);ro.disconnect();renderer.dispose();scene.traverse(o=>{o.geometry?.dispose();if(o.material){(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>m.dispose())}})}};
}
