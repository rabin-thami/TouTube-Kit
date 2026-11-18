import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { stepped } from "./tokens";

// Monochrome film grain that refreshes on twos (12 fps), like V1/V6.
// `amount` is overlay opacity; 0.10 ≈ 1.5 levels std (V1 subtle), 0.30 ≈ 4–5 levels (V6 strong). Calibrated in REMOTION_IMPLEMENTATION_GUIDE.md.
export const Grain: React.FC<{ amount?: number }> = ({ amount = 0.1 }) => {
  const seed = stepped(useCurrentFrame()) / 2;
  return (
    <AbsoluteFill
      style={{
        mixBlendMode: "overlay",
        opacity: amount,
        pointerEvents: "none",
      }}
    >
      <svg width="100%" height="100%">
        <filter id={`grain-${seed}`}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.85"
            numOctaves={1}
            seed={seed}
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

// Static paper mottling (temporal corr ≥ 0.92 in V4/V5: the paper never boils by itself).
export const PaperTexture: React.FC<{ amount?: number }> = ({
  amount = 0.18,
}) => (
  <AbsoluteFill
    style={{ mixBlendMode: "multiply", opacity: amount, pointerEvents: "none" }}
  >
    <svg width="100%" height="100%">
      <filter id="paper-mottle">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.012 0.02"
          numOctaves={4}
          seed={7}
        />
        <feColorMatrix
          type="matrix"
          values="0 0 0 0 0.55  0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 -1.4 1.1"
        />
      </filter>
      <rect width="100%" height="100%" filter="url(#paper-mottle)" />
    </svg>
  </AbsoluteFill>
);

// Radial vignette. strength = corner luma drop (V1/V4 measured 8–15%, V5 5–8%, V3 0).
export const Vignette: React.FC<{ strength?: number }> = ({
  strength = 0.12,
}) => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      mixBlendMode: "multiply",
      background: `radial-gradient(ellipse 75% 75% at 50% 45%, rgba(0,0,0,0) 40%, rgba(40,30,20,${strength * 1.6}) 100%)`,
    }}
  />
);

// Local graph-paper patch fading out from one corner (V3: 48 px pitch, #CDCCC2 hairlines).
export const GridPatch: React.FC<{
  corner?: "tl" | "tr" | "bl" | "br";
  pitch?: number;
}> = ({ corner = "tr", pitch = 48 }) => {
  const pos = { tl: "0% 0%", tr: "100% 0%", bl: "0% 100%", br: "100% 100%" }[
    corner
  ];
  return (
    <AbsoluteFill
      style={{
        backgroundImage: `linear-gradient(#CDCCC2 1px, transparent 1px), linear-gradient(90deg, #CDCCC2 1px, transparent 1px)`,
        backgroundSize: `${pitch}px ${pitch}px`,
        maskImage: `radial-gradient(circle at ${pos}, black 0%, transparent 38%)`,
        opacity: 0.7,
      }}
    />
  );
};
