import React from "react";
import {
  AbsoluteFill,
  Composition,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { clamp, color, ease, shadow, stepped } from "./tokens";
import { marker, sans, serif } from "./fonts";
import { Grain, GridPatch, PaperTexture, Vignette } from "./texture";
import { Highlight, MarkerEllipse, PopIn, TypeOn } from "./motion";
import { zoomThrough } from "./zoomThrough";

// Calibration piece for reference-style-system/. All copy and data are placeholders.
const FPS = 24;
const TITLE = 150;
const CHART = 150;
const COLLAGE = 120;
const ZOOM_THROUGH = 52; // 24 f ease-in + 28 f ease-out, measured in V6

// --- Scene 1: flat-paper title card (V3 D2 slow push + punch-in, word-synced type-on, V1 D4 highlight)
const TitleCard: React.FC = () => {
  const f = stepped(useCurrentFrame());
  // [word, reveal frame, line break after]. Reveal frames stand in for VO word timings.
  const words: [string, number, boolean][] = [
    ["EVERY", 6, false],
    ["MAP", 14, true],
    ["STARTS", 24, false],
    ["AS", 32, false],
    ["A", 36, true],
  ];
  return (
    <AbsoluteFill style={{ background: color.paper }}>
      <GridPatch corner="tr" />
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          // Linear creep 0.13%/f → ×1.30 punch over 16 f (ease-out) → creep 0.1%/f
          scale:
            (1 + 0.0013 * Math.min(f, 60)) *
            interpolate(f, [60, 76], [1, 1.3], {
              ...clamp,
              easing: ease.punch,
            }) *
            (1 + 0.001 * Math.max(0, f - 76)),
        }}
      >
        <div
          style={{
            border: `10px solid ${color.ink}`,
            padding: "48px 56px",
            width: 1000,
            boxSizing: "border-box",
            textAlign: "center",
            fontFamily: serif,
            fontWeight: 900,
            fontSize: 118, // cap ≈ 80 px before the ×1.3 punch → ≈ 104 px after (V3: 93 px cap after punch)
            lineHeight: 0.98, // V3 line pitch ≈ 1.19 × cap ≈ 0.95–1.0 × font size
            color: color.ink,
            letterSpacing: "-0.01em",
          }}
        >
          {words.map(([w, at, br]) => (
            <React.Fragment key={w}>
              <span style={{ opacity: f >= at ? 1 : 0 }}>{w} </span>
              {br ? <br /> : null}
            </React.Fragment>
          ))}
          <span style={{ opacity: f >= 56 ? 1 : 0 }}>
            <Highlight start={60} duration={12} fill={color.highlightPure}>
              GUESS
            </Highlight>
          </span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// --- Scene 2: data chart (V3 D8 bars: quart-out 30 f, 8 f stagger; D7 highlighter; marker circle)
const bars = [
  { label: "Category one", value: 0.92, fill: color.red },
  { label: "Category two", value: 0.64, fill: color.blue },
  { label: "Category three", value: 0.41, fill: color.green },
  { label: "Category four", value: 0.27, fill: color.purple },
  { label: "Other", value: 0.08, fill: color.pink },
];
const BAR_START = 40; // after the zoom-through has landed
const BAR_MAX = 900;

const ChartCard: React.FC = () => {
  const f = stepped(useCurrentFrame());
  return (
    <AbsoluteFill style={{ background: color.paper, color: color.ink }}>
      <GridPatch corner="bl" />
      <div
        style={{
          position: "absolute",
          top: 92,
          width: "100%",
          textAlign: "center",
          fontFamily: serif,
          fontWeight: 600,
          fontSize: 52, // cap ≈ 35 px (V3 chart titles)
        }}
      >
        Share of something, by category
      </div>
      <div
        style={{
          position: "absolute",
          top: 168,
          width: "100%",
          textAlign: "center",
          fontFamily: sans,
          fontSize: 24,
          color: color.inkSoft,
        }}
      >
        <TypeOn
          text="Placeholder data — calibration only"
          start={56}
          framesPerChar={1}
        />
      </div>
      {bars.map((b, i) => {
        const start = BAR_START + i * 8;
        const w = interpolate(f, [start, start + 30], [0, b.value * BAR_MAX], {
          ...clamp,
          easing: ease.grow,
        });
        const y = 300 + i * 132;
        return (
          <React.Fragment key={b.label}>
            <div
              style={{
                position: "absolute",
                right: 1920 - 480,
                top: y + 18,
                fontFamily: sans,
                fontWeight: 500,
                fontSize: 34,
                textAlign: "right",
              }}
            >
              {i === 4 ? (
                <Highlight start={110} duration={16}>
                  {b.label}
                </Highlight>
              ) : (
                b.label
              )}
            </div>
            <div
              style={{
                position: "absolute",
                left: 520,
                top: y,
                height: 84,
                width: w,
                background: b.fill,
              }}
            />
            <div
              style={{
                position: "absolute",
                left: 540 + w,
                top: y + 18,
                fontFamily: sans,
                fontWeight: 700,
                fontSize: 36,
                opacity: f >= start + 20 ? 1 : 0,
              }}
            >
              {Math.round(b.value * 100)}%
            </div>
          </React.Fragment>
        );
      })}
      <MarkerEllipse
        start={124}
        width={260}
        height={150}
        style={{ position: "absolute", left: 470, top: 822 }}
      />
      <div
        style={{
          position: "absolute",
          left: 760,
          top: 880,
          fontFamily: marker,
          fontSize: 34,
          color: color.redDeep,
          rotate: "-3deg",
          opacity: f >= 136 ? 1 : 0,
        }}
      >
        the small one matters
      </div>
    </AbsoluteFill>
  );
};

// --- Scene 3: analog collage (V6 D3 push + D6 linear pull, V5 tape expo-out, V1 vignette/grain, shadows)
const Collage: React.FC = () => {
  const f = stepped(useCurrentFrame());
  const camera =
    interpolate(f, [8, 30], [1, 1.18], { ...clamp, easing: ease.tilt }) *
    (1 - 0.001 * Math.max(0, f - 30)); // linear pull ≈ 0.2%/2 f
  const tape = interpolate(f, [24, 54], [0, 1], { ...clamp, easing: ease.expo });
  const underline = interpolate(f, [40, 48], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: color.dark }}>
      <AbsoluteFill style={{ scale: camera, transformOrigin: "50% 40%" }}>
        <AbsoluteFill style={{ background: color.paperCollage }} />
        <PaperTexture />
        <div
          style={{
            position: "absolute",
            top: 120,
            width: "100%",
            textAlign: "center",
            fontFamily: serif,
            fontWeight: 700,
            fontSize: 88,
            color: color.inkSoft,
            // Chromatic fringe ≈ 2 px (V1 captions, V6 tape)
            textShadow:
              "-2px 0 rgba(220,40,40,.35), 2px 0 rgba(40,160,220,.35)",
          }}
        >
          Training the eye
          <svg
            width={520}
            height={24}
            style={{ display: "block", margin: "4px auto 0" }}
          >
            <path
              d="M6 14 C 140 6, 320 18, 514 9"
              stroke={color.ink}
              strokeWidth={6}
              fill="none"
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - underline}
            />
          </svg>
        </div>
        {/* Placeholder "archival photo": neutral B&W with a faint warm lift, white border */}
        <div
          style={{
            position: "absolute",
            left: 560,
            top: 330,
            width: 800,
            height: 520,
            rotate: "-2deg",
            border: "16px solid #F4F1EA",
            boxShadow: shadow.cardLarge,
            background:
              "radial-gradient(circle at 35% 40%, #9a958c 0%, #5d5953 45%, #2c2a27 100%)",
            filter: "sepia(0.08)",
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "grid",
              placeItems: "center",
              fontFamily: sans,
              fontSize: 28,
              color: "#d8d4cc",
              letterSpacing: "0.2em",
            }}
          >
            PLACEHOLDER PHOTO
          </div>
        </div>
        <PopIn
          start={60}
          duration={18}
          style={{ position: "absolute", left: 1230, top: 300 }}
        >
          <MarkerEllipse
            start={60}
            width={210}
            height={150}
            stroke={color.redDeep}
          />
        </PopIn>
        <div
          style={{
            position: "absolute",
            left: 520,
            top: 790,
            padding: "10px 26px",
            background: color.highlightPure,
            fontFamily: marker,
            fontSize: 40,
            color: color.ink,
            boxShadow: shadow.cardSmall,
            opacity: f >= 24 ? 1 : 0,
            translate: `${(1 - tape) * 420}px ${(1 - tape) * 260}px`,
            rotate: `${-4 + (1 - tape) * 3}deg`,
          }}
        >
          SAMPLE · 19XX
        </div>
      </AbsoluteFill>
      <Vignette strength={0.12} />
      <Grain amount={0.2} />
      {/* End: linear fade to black, 29 f (V2 D11) */}
      <AbsoluteFill
        style={{
          background: "#000",
          opacity: interpolate(
            useCurrentFrame(),
            [COLLAGE - 29, COLLAGE],
            [0, 1],
            clamp,
          ),
        }}
      />
    </AbsoluteFill>
  );
};

export const StyleCalibrationVideo: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence name="Title card" durationInFrames={TITLE}>
      <TitleCard />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition
      presentation={zoomThrough(ZOOM_THROUGH)}
      timing={linearTiming({ durationInFrames: ZOOM_THROUGH })}
    />
    <TransitionSeries.Sequence name="Chart" durationInFrames={CHART}>
      <ChartCard />
    </TransitionSeries.Sequence>
    <TransitionSeries.Sequence name="Collage" durationInFrames={COLLAGE}>
      <Collage />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);

export const StyleCalibration: React.FC = () => (
  <Composition
    id="StyleCalibration"
    component={StyleCalibrationVideo}
    durationInFrames={TITLE + CHART + COLLAGE - ZOOM_THROUGH}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
