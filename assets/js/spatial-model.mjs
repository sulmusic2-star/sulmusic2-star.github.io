// A synthetic, planar boundary example. Units are illustrative meters.
// These coordinates are not a government dataset or an actual property.
export const boundary = [[-25,-120],[28,-120],[42,-80],[30,-35],[48,15],[36,65],[50,120],[-18,120],[-33,75],[-24,20],[-42,-45]];
export function segmentDistance(p,a,b) {
  const dx=b[0]-a[0],dy=b[1]-a[1],d=dx*dx+dy*dy;
  const t=d?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/d)):0;
  return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);
}
export function contains(p, ring=boundary) {
  let inside=false;
  for(let i=0,j=ring.length-1;i<ring.length;j=i++) {
    const a=ring[i],b=ring[j];
    if((a[1]>p[1])!==(b[1]>p[1]) && p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]) inside=!inside;
  }
  return inside;
}
export function classifyPoint(x,z,radius) {
  if(![x,z,radius].every(Number.isFinite)||radius<0) throw new TypeError('Use finite coordinates and a nonnegative radius.');
  const p=[x,z], distance=Math.min(...boundary.map((a,i)=>segmentDistance(p,a,boundary[(i+1)%boundary.length])));
  const nominal=contains(p), uncertain=distance<=radius+1e-9;
  return {state:uncertain?'review':nominal?'inside':'outside', nominal, distance, radius};
}
export function terrainHeight(x,z) {
  const valley=12*Math.sin(z/61)+3*Math.cos(z/23);
  return 4 + 11*(1-Math.exp(-Math.pow((x-valley)/47,2))) + 4*Math.sin(x/59)*Math.cos(z/72) + 2*Math.sin(z/28+x/42);
}
