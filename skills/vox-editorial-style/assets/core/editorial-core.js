// Editorial paper explainer — framework-neutral core (ES module, zero dependencies).
// Works in any JS renderer: Remotion, HyperFrames/GSAP, anime.js, Motion Canvas, plain canvas, Node.
// Everything is a pure function of time, so renders are deterministic.

// ---------- Easing ----------
// cubic-bezier(x1,y1,x2,y2) → (p in 0..1) => value. Same curve as CSS / Remotion Easing.bezier.
export function cubicBezier(x1, y1, x2, y2) {
  const cx = 3 * x1,
    bx = 3 * (x2 - x1) - cx,
    ax = 1 - cx - bx;
  const cy = 3 * y1,
    by = 3 * (y2 - y1) - cy,
    ay = 1 - cy - by;
  const sx = (t) => ((ax * t + bx) * t + cx) * t;
  const sy = (t) => ((ay * t + by) * t + cy) * t;
  const dx = (t) => (3 * ax * t + 2 * bx) * t + cx;
  const solve = (x) => {
    let t = x;
    for (let i = 0; i < 8; i++) {
      const e = sx(t) - x;
      if (Math.abs(e) < 1e-6) return t;
      const d = dx(t);
      if (Math.abs(d) < 1e-6) break;
      t -= e / d;
    }
    let lo = 0,
      hi = 1;
    t = x; // bisection fallback
    for (let i = 0; i < 40; i++) {
      const v = sx(t);
      if (Math.abs(v - x) < 1e-6) break;
      if (v < x) lo = t;
      else hi = t;
      t = (lo + hi) / 2;
    }
    return t;
  };
  return (p) => (p <= 0 ? 0 : p >= 1 ? 1 : sy(solve(p)));
}

// Fitted curves (ESTIMATE) — mirror assets/tokens.json "ease".
export const EASE_POINTS = {
  pop: [0.16, 0.7, 0.7, 1], // pops + highlight blocks (V2 disc fit)
  expo: [0.16, 1, 0.3, 1], // tape slide, TV pop (V5, V1)
  grow: [0.25, 1, 0.5, 1], // bars
  punch: [0.2, 0.8, 0.3, 1], // punch-in, whip pan, landing after a cut
  push: [0.7, 0, 0.4, 1], // camera push to detail
  tilt: [0.45, 0, 0.55, 1], // soft push, symmetric rises
  pan: [0.55, 0, 0.1, 1], // lateral pan, long tail
  accel: [0.55, 0, 1, 0.45], // moving INTO a cut, brush swipe
  wipe: [0.37, 0, 0.63, 1], // highlighter per line
  mapZoom: [0.55, 0, 0.15, 1],
};
export const ease = Object.fromEntries(
  Object.entries(EASE_POINTS).map(([k, v]) => [k, cubicBezier(...v)]),
);
export const linear = (p) => p;

// ---------- Stepped ("on twos") time ----------
// Quantise seconds to drawings (default 12/s). Use for every graphic animation.
export const stepTime = (sec, drawingsPerSecond = 12) =>
  Math.floor(sec * drawingsPerSecond + 1e-9) / drawingsPerSecond;
// Quantise frames: frame → nearest lower multiple of `step` (Remotion-style).
export const stepFrame = (frame, step = 2) => Math.floor(frame / step) * step;
// Wrap an ease so a tween of `durationSec` only changes 12x/s (GSAP/anime.js: pass as `ease`).
export const onTwos = (easeFn, durationSec, drawingsPerSecond = 12) => {
  const n = Math.max(1, Math.round(durationSec * drawingsPerSecond));
  return (p) => easeFn(Math.min(1, Math.floor(p * n + 1e-9) / n));
};

// ---------- Interpolation ----------
export const clamp01 = (v) => Math.max(0, Math.min(1, v));
// value at time t for a move from (t0,v0) to (t1,v1) with an ease; clamps outside the range.
export const tween = (t, t0, t1, v0, v1, easeFn = linear) =>
  v0 + (v1 - v0) * easeFn(clamp01((t - t0) / (t1 - t0)));
// Zooms ≥2x: interpolate in log space so perceived speed matches the references.
export const tweenScale = (t, t0, t1, s0, s1, easeFn = linear) =>
  Math.exp(tween(t, t0, t1, Math.log(s0), Math.log(s1), easeFn));

// ---------- Deterministic randomness ----------
export function seeded(key) {
  let h = 2166136261;
  for (const c of String(key)) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  h += 0x6d2b79f5;
  let t = h;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
// A-A-B texture boil: returns base or base+1, variant B one drawing in three.
export const boilSeed = (sec, base = 1, drawingsPerSecond = 12) =>
  base + [0, 0, 1][Math.floor(sec * drawingsPerSecond + 1e-9) % 3];

// ---------- Shapes ----------
// Torn-paper CSS clip-path polygon (deterministic).
export function tornClipPath(w, h, seed = "clip", step = 16, amp = 7) {
  const pts = [];
  let i = 0;
  const j = () => seeded(`${seed}-${i++}`) * amp;
  for (let x = 0; x <= w; x += step) pts.push(`${x}px ${j()}px`);
  for (let y = step; y <= h; y += step) pts.push(`${w - j()}px ${y}px`);
  for (let x = w - step; x >= 0; x -= step) pts.push(`${x}px ${h - j()}px`);
  for (let y = h - step; y > 0; y -= step) pts.push(`${j()}px ${y}px`);
  return `polygon(${pts.join(",")})`;
}

// Dry-brush stroke body in a 1000×100 viewBox (stretch with preserveAspectRatio="none").
export const BRUSH_PATH =
  "M 8 26 C 300 12, 700 6, 992 2 C 1000 30, 1000 60, 994 80 C 700 86, 300 92, 4 98 C -2 74, -2 48, 8 26 Z";

// Hand-drawn double-loop ellipse path for a w×h box (draw on with stroke-dashoffset, pathLength=1).
export const markerEllipsePath = (w, h) =>
  `M ${w * 0.62} ${h * 0.06} C ${w * 1.02} ${h * 0.1}, ${w * 1.04} ${h * 0.92}, ${w * 0.5} ${h * 0.95} ` +
  `C ${w * -0.04} ${h * 0.97}, ${w * -0.02} ${h * 0.04}, ${w * 0.55} ${h * 0.03} ` +
  `C ${w * 0.98} ${h * 0.02}, ${w * 1.01} ${h * 0.7}, ${w * 0.7} ${h * 0.86}`;

// ---------- SVG filter markup (insert inside <svg><defs>…</defs></svg>) ----------
// Dry-brush: horizontal bristle gaps + ragged displaced edges. Reveal by clipping a rect to width p.
export const brushFilter = (id, seed = 3, wobbleSeed = 13) => `
<filter id="${id}" x="-5%" y="-40%" width="110%" height="180%">
  <feTurbulence type="fractalNoise" baseFrequency="0.0025 0.16" numOctaves="2" seed="${seed}" result="streaks"/>
  <feColorMatrix in="streaks" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  6 0 0 0 -1.75" result="bristles"/>
  <feComposite in="SourceGraphic" in2="bristles" operator="in" result="dry"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.03 0.12" numOctaves="3" seed="${wobbleSeed}" result="wobble"/>
  <feDisplacementMap in="dry" in2="wobble" scale="30" xChannelSelector="R" yChannelSelector="G"/>
</filter>`;

// Letterpress ink: rough edges + speckle holes. reveal 0→1 inks text in from fragments.
export const letterpressFilter = (id, seed = 1, reveal = 1) => `
<filter id="${id}">
  <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="${seed}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4" xChannelSelector="R" yChannelSelector="G" result="rough"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.22" numOctaves="2" seed="${seed + 5}" result="speck"/>
  <feColorMatrix in="speck" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -5 ${4.4 - (1 - reveal) * 4.2}" result="holes"/>
  <feComposite in="rough" in2="holes" operator="in"/>
</filter>`;

// Halftone dot screen for SVG content of size w×h (dot size follows darkness). ink = "#RRGGBB".
export const halftoneFilter = (id, w, h, cell = 7, ink = "#3A3835") => {
  const dot =
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' width='${cell}' height='${cell}'><defs><radialGradient id='g'><stop offset='0' stop-color='black'/><stop offset='1' stop-color='white'/></radialGradient></defs><rect width='${cell}' height='${cell}' fill='url(#g)'/></svg>`,
    );
  const [r, g, b] = [1, 3, 5].map(
    (i) => parseInt(ink.slice(i, i + 2), 16) / 255,
  );
  return `
<filter id="${id}" x="0" y="0" width="${w}" height="${h}" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
  <feColorMatrix in="SourceGraphic" type="saturate" values="0" result="lum"/>
  <feImage href="${dot}" x="0" y="0" width="${cell}" height="${cell}" result="cell"/>
  <feTile in="cell" result="screen"/>
  <feComposite in="lum" in2="screen" operator="arithmetic" k1="0" k2="1" k3="1" k4="-0.5" result="sum"/>
  <feComponentTransfer in="sum" result="bw">
    <feFuncR type="discrete" tableValues="0 1"/><feFuncG type="discrete" tableValues="0 1"/>
    <feFuncB type="discrete" tableValues="0 1"/><feFuncA type="linear" slope="0" intercept="1"/>
  </feComponentTransfer>
  <feColorMatrix in="bw" type="matrix" values="0 0 0 0 ${r}  0 0 0 0 ${g}  0 0 0 0 ${b}  -1 0 0 0 1"/>
</filter>`;
};

// Grain tile as a CSS background (data URI). Animate background-position in big stepped jumps
// (12/s) for "fresh" grain without re-seeding — works in any DOM renderer. Opacity ≈ 0.15–0.3, overlay blend.
export const grainTileDataUri = (size = 512, seed = 1) =>
  "data:image/svg+xml;utf8," +
  encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='${size}' height='${size}'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='1' seed='${seed}' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>`,
  );
// Background offset for the grain tile at time `sec` (deterministic jump each drawing).
export const grainOffset = (sec, drawingsPerSecond = 12) => {
  const k = Math.floor(sec * drawingsPerSecond + 1e-9);
  return [
    Math.floor(seeded(`gx${k}`) * 512),
    Math.floor(seeded(`gy${k}`) * 512),
  ];
};

// Radial vignette CSS (strength = corner luma drop, 0.08–0.15 for collage).
export const vignetteCss = (strength = 0.12) =>
  `radial-gradient(ellipse 75% 75% at 50% 45%, rgba(0,0,0,0) 40%, rgba(40,30,20,${strength * 1.6}) 100%)`;
