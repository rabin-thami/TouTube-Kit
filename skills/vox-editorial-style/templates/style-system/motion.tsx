import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { clamp, color, ease, stepped } from "./tokens";

// Typewriter by characters, stepped on twos. V3 lower third ≈ 1 char/frame, V1 titles ≈ 2 frames/char.
export const TypeOn: React.FC<{
  text: string;
  start: number;
  framesPerChar?: number;
  style?: React.CSSProperties;
}> = ({ text, start, framesPerChar = 1, style }) => {
  const f = stepped(useCurrentFrame());
  const n = Math.max(0, Math.floor((f - start) / framesPerChar));
  return <span style={style}>{text.slice(0, n)}</span>;
};

// Flat highlighter block that wipes in L→R behind its children (V1 D4/D7, V3 D7).
// Multiply keeps ink and paper grain visible through the yellow (V4).
export const Highlight: React.FC<{
  start: number;
  duration?: number;
  fill?: string;
  children: React.ReactNode;
}> = ({ start, duration = 12, fill = color.highlight, children }) => {
  const f = stepped(useCurrentFrame());
  const p = interpolate(f, [start, start + duration], [0, 1], {
    ...clamp,
    easing: ease.pop,
  });
  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      <span
        style={{
          position: "absolute",
          left: "-0.12em",
          top: "0.06em",
          bottom: "-0.02em",
          width: `calc((100% + 0.24em) * ${p})`,
          background: fill,
          mixBlendMode: "multiply",
        }}
      />
      <span style={{ position: "relative" }}>{children}</span>
    </span>
  );
};

// Scale pop with expo-out and no overshoot (V2 circle 24 f, V2 bullet 18 f, V1 TV 10 f).
export const PopIn: React.FC<{
  start: number;
  duration?: number;
  from?: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ start, duration = 18, from = 0, style, children }) => {
  const f = stepped(useCurrentFrame());
  return (
    <div
      style={{
        ...style,
        opacity: f < start ? 0 : 1,
        scale: interpolate(f, [start, start + duration], [from, 1], {
          ...clamp,
          easing: ease.pop,
        }),
      }}
    >
      {children}
    </div>
  );
};

// Hand-drawn double-loop ellipse that draws on (V6 D8 12 f, V1 D9 6–10 f, V3 D14).
export const MarkerEllipse: React.FC<{
  start: number;
  duration?: number;
  width: number;
  height: number;
  stroke?: string;
  strokeWidth?: number;
  style?: React.CSSProperties;
}> = ({
  start,
  duration = 12,
  width,
  height,
  stroke = color.redDeep,
  strokeWidth = 5,
  style,
}) => {
  const f = stepped(useCurrentFrame());
  const p = interpolate(f, [start, start + duration], [0, 1], {
    ...clamp,
    easing: ease.tilt,
  });
  const w = width;
  const h = height;
  // Two slightly offset, slightly open loops read as hand-drawn rather than vector-perfect.
  const d = `M ${w * 0.62} ${h * 0.06}
    C ${w * 1.02} ${h * 0.1}, ${w * 1.04} ${h * 0.92}, ${w * 0.5} ${h * 0.95}
    C ${w * -0.04} ${h * 0.97}, ${w * -0.02} ${h * 0.04}, ${w * 0.55} ${h * 0.03}
    C ${w * 0.98} ${h * 0.02}, ${w * 1.01} ${h * 0.7}, ${w * 0.7} ${h * 0.86}`;
  return (
    <svg width={w} height={h} style={{ overflow: "visible", ...style }}>
      <path
        d={d}
        fill="none"
        stroke={stroke}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        pathLength={1}
        strokeDasharray={1}
        strokeDashoffset={1 - p}
      />
    </svg>
  );
};
