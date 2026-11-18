import React, { useId } from "react";
import { interpolate, random, useCurrentFrame } from "remotion";
import { clamp, color, ease, stepped } from "./tokens";

// Newspaper + dry-brush toolkit (V4 "Highlight" title/headline card, V1 newspaper burst f2275–2361).

const useSvgId = (prefix: string) =>
  prefix + useId().replace(/[^a-zA-Z0-9]/g, "");

// A-A-B texture boil: variant B is shown one drawing in three (V4: 3.3 Hz at 10 fps).
export const boilSeed = (frame: number, base = 1) =>
  base + [0, 0, 1][Math.floor(frame / 2) % 3];

// ---------------------------------------------------------------------------
// Dry-brush highlighter stroke. Drawn in a 1000×100 box stretched to its parent, so it
// fits any word. Horizontal bristle gaps + wobbly ragged edges; the reveal edge is ragged too.
// Defaults follow V4 swipe #2: accelerating (ease-in), short, hard stop.
export const BrushStroke: React.FC<{
  start: number;
  duration?: number;
  fill?: string;
  easing?: (t: number) => number;
  seed?: number;
  style?: React.CSSProperties;
}> = ({
  start,
  duration = 10,
  fill = color.brush,
  easing = ease.accel,
  seed = 3,
  style,
}) => {
  const frame = useCurrentFrame();
  const f = stepped(frame);
  const p = interpolate(f, [start, start + duration], [0, 1], {
    ...clamp,
    easing,
  });
  const id = useSvgId("brush");
  if (p <= 0) return null;
  // Slightly up-slanted body (V4 stroke rises left→right) with bulged ends.
  const d =
    "M 8 26 C 300 12, 700 6, 992 2 C 1000 30, 1000 60, 994 80 " +
    "C 700 86, 300 92, 4 98 C -2 74, -2 48, 8 26 Z";
  return (
    <svg
      viewBox="0 0 1000 100"
      preserveAspectRatio="none"
      style={{ overflow: "visible", mixBlendMode: "multiply", ...style }}
    >
      <defs>
        <filter id={id} x="-5%" y="-40%" width="110%" height="180%">
          {/* long horizontal streaks = bristle tracks; low values become dry gaps */}
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.0025 0.16"
            numOctaves={2}
            seed={seed}
            result="streaks"
          />
          <feColorMatrix
            in="streaks"
            type="matrix"
            values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  6 0 0 0 -1.75"
            result="bristles"
          />
          <feComposite
            in="SourceGraphic"
            in2="bristles"
            operator="in"
            result="dry"
          />
          {/* edge wobble; reseeded with the boil so held strokes stay alive */}
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.03 0.12"
            numOctaves={3}
            seed={boilSeed(frame, seed + 10)}
            result="wobble"
          />
          <feDisplacementMap
            in="dry"
            in2="wobble"
            scale={30}
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
        <clipPath id={`${id}c`}>
          <rect x={-60} y={-100} width={1120 * p} height={300} />
        </clipPath>
      </defs>
      <g filter={`url(#${id})`}>
        <g clipPath={`url(#${id}c)`}>
          <path d={d} fill={fill} />
        </g>
      </g>
    </svg>
  );
};

// Inline wrapper: brush stroke behind a word or phrase.
export const BrushHighlight: React.FC<{
  start: number;
  duration?: number;
  fill?: string;
  easing?: (t: number) => number;
  seed?: number;
  children: React.ReactNode;
}> = ({ children, ...brush }) => (
  <span style={{ position: "relative", display: "inline-block" }}>
    <BrushStroke
      {...brush}
      style={{
        position: "absolute",
        left: "-0.18em",
        top: "0.02em",
        width: "calc(100% + 0.4em)",
        height: "calc(100% + 0.04em)",
      }}
    />
    <span style={{ position: "relative" }}>{children}</span>
  </span>
);

// ---------------------------------------------------------------------------
// Letterpress ink: slight edge displacement + speckled ink holes, boiling A-A-B.
// `reveal` 0→1 inks the text in from eroded fragments (V4 title/headline ink-in, 4 drawings).
export const Letterpress: React.FC<{
  reveal?: number;
  seed?: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ reveal = 1, seed = 1, style, children }) => {
  const frame = useCurrentFrame();
  const id = useSvgId("ink");
  const s = boilSeed(frame, seed);
  // Alpha offset: high = solid ink with rare holes; low = mostly eroded.
  const solid = 4.4 - (1 - reveal) * 4.2;
  return (
    <>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id={id}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.8"
            numOctaves={1}
            seed={s}
            result="n"
          />
          <feDisplacementMap
            in="SourceGraphic"
            in2="n"
            scale={2.4}
            xChannelSelector="R"
            yChannelSelector="G"
            result="rough"
          />
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.22"
            numOctaves={2}
            seed={s + 5}
            result="speck"
          />
          <feColorMatrix
            in="speck"
            type="matrix"
            values={`0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -5 ${solid}`}
            result="holes"
          />
          <feComposite in="rough" in2="holes" operator="in" />
        </filter>
      </svg>
      <div style={{ filter: `url(#${id})`, ...style }}>{children}</div>
    </>
  );
};

// ---------------------------------------------------------------------------
// Halftone: renders SVG children as a newspaper dot screen (dot size follows darkness).
// Screen = tiled radial gradient; ink where luminance + screen < 1 (threshold).
export const Halftone: React.FC<{
  width: number;
  height: number;
  cell?: number;
  ink?: string;
  children: React.ReactNode;
}> = ({ width: w, height: h, cell = 7, ink = color.newsInk, children }) => {
  const id = useSvgId("ht");
  const c = cell;
  const dot =
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' width='${c}' height='${c}'><defs><radialGradient id='g'><stop offset='0' stop-color='black'/><stop offset='1' stop-color='white'/></radialGradient></defs><rect width='${c}' height='${c}' fill='url(#g)'/></svg>`,
    );
  const rgb = [1, 3, 5].map((i) => parseInt(ink.slice(i, i + 2), 16) / 255);
  return (
    <svg
      width={w}
      height={h}
      style={{ mixBlendMode: "multiply", display: "block" }}
    >
      <defs>
        <filter
          id={id}
          x={0}
          y={0}
          width={w}
          height={h}
          filterUnits="userSpaceOnUse"
          colorInterpolationFilters="sRGB"
        >
          <feColorMatrix
            in="SourceGraphic"
            type="saturate"
            values="0"
            result="lum"
          />
          <feImage href={dot} x={0} y={0} width={c} height={c} result="cell" />
          <feTile in="cell" result="screen" />
          <feComposite
            in="lum"
            in2="screen"
            operator="arithmetic"
            k1={0}
            k2={1}
            k3={1}
            k4={-0.5}
            result="sum"
          />
          <feComponentTransfer in="sum" result="bw">
            <feFuncR type="discrete" tableValues="0 1" />
            <feFuncG type="discrete" tableValues="0 1" />
            <feFuncB type="discrete" tableValues="0 1" />
            <feFuncA type="linear" slope={0} intercept={1} />
          </feComponentTransfer>
          <feColorMatrix
            in="bw"
            type="matrix"
            values={`0 0 0 0 ${rgb[0]}  0 0 0 0 ${rgb[1]}  0 0 0 0 ${rgb[2]}  -1 0 0 0 1`}
          />
        </filter>
      </defs>
      <g filter={`url(#${id})`}>{children}</g>
    </svg>
  );
};

// ---------------------------------------------------------------------------
// Torn-edge newsprint clipping with drop shadow. Edges are deterministic (`random(seed)`).
export const tornClipPath = (
  w: number,
  h: number,
  seed: string,
  step = 16,
  amp = 7,
) => {
  const pts: string[] = [];
  const j = (i: number) => random(`${seed}-${i}`) * amp;
  let i = 0;
  for (let x = 0; x <= w; x += step) pts.push(`${x}px ${j(i++)}px`);
  for (let y = step; y <= h; y += step) pts.push(`${w - j(i++)}px ${y}px`);
  for (let x = w - step; x >= 0; x -= step) pts.push(`${x}px ${h - j(i++)}px`);
  for (let y = h - step; y > 0; y -= step) pts.push(`${j(i++)}px ${y}px`);
  return `polygon(${pts.join(",")})`;
};

export const NewsClipping: React.FC<{
  width: number;
  height: number;
  seed?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ width, height, seed = "clip", style, children }) => (
  // drop-shadow on the parent, because clip-path would cut a box-shadow
  <div style={{ filter: "drop-shadow(6px 8px 14px rgba(0,0,0,.4))", ...style }}>
    <div
      style={{
        width,
        height,
        background: color.newsprint,
        clipPath: tornClipPath(width, height, seed),
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* newsprint fibre: static, multiply */}
      <svg
        width="100%"
        height="100%"
        style={{
          position: "absolute",
          inset: 0,
          mixBlendMode: "multiply",
          opacity: 0.35,
        }}
      >
        <filter id={`fibre-${seed}`}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.6 0.05"
            numOctaves={2}
            seed={4}
          />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0.6  0 0 0 0 0.56  0 0 0 0 0.48  0 0 0 -1.2 1"
          />
        </filter>
        <rect width="100%" height="100%" filter={`url(#fibre-${seed})`} />
      </svg>
      {/* foxing: uneven yellowing toward the edges */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(ellipse 80% 70% at 45% 40%, rgba(0,0,0,0) 55%, rgba(150,110,40,.22) 100%)",
          mixBlendMode: "multiply",
        }}
      />
      <div style={{ position: "relative", height: "100%" }}>{children}</div>
    </div>
  </div>
);

// Placeholder body copy for clippings — original filler, not real reporting.
const FILLER = [
  "Officials said the survey would take several seasons to complete.",
  "Residents gathered at the hall to compare the new sheets with the old.",
  "Several streets appear under two different names on earlier editions.",
  "The committee declined to comment on the proposed boundary changes.",
  "Printers worked through the night to prepare the first run of copies.",
  "Surveyors noted that the river had moved since the last measurement.",
];
export const fillerText = (n: number, offset = 0) =>
  Array.from(
    { length: n },
    (_, i) => FILLER[(i + offset) % FILLER.length],
  ).join(" ");
