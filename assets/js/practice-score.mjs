// Browser adaptation of the selected public scoring example, not the complete app.
// Source: https://github.com/sulmusic2-star/squadbrain-showcase/blob/main/examples/adaptive-practice.ts
export function scorePractice({misses=1,streak=0,hours=2,recent=false}={}) {
 if(![misses,streak,hours].every(Number.isFinite)||[misses,streak,hours].some(n=>n<0)) throw new TypeError('Practice history must be finite and nonnegative.');
 const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
 const interval=Math.pow(2,Math.min(streak,6))*(misses>0?.55:1);
 const ratio=hours/interval;let priority=clamp(ratio*55,0,95);const reasons=[];
 if(ratio>=1)reasons.push('Due for review');
 if(misses>0){priority+=clamp(misses*12,0,36);reasons.push('Miss history');}
 if(streak===0){priority+=10;reasons.push('Not yet stable');}
 if(recent){priority-=35;reasons.push('Recently shown');}
 return {priority:Math.round(clamp(priority,0,100)),reasons,interval};
}
