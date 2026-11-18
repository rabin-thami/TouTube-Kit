import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Sequence,
  Series,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { clamp, color, ease, stepped } from "./tokens";
import { blackletter, condensed, sans, serif } from "./fonts";
import { Grain, PaperTexture, Vignette } from "./texture";
import {
  BrushHighlight,
  Halftone,
  Letterpress,
  NewsClipping,
  fillerText,
} from "./newspaper";

// Newspaper effect demo. All mastheads, headlines and copy are invented placeholders.
const FPS = 24;
const FRONT = 150;
const BURST = [10, 8, 8, 6, 6, 6, 8, 44]; // V1 headline burst: 5–15 f @30 → 4–12 f @24, last one held
const TOTAL = FRONT + BURST.reduce((a, b) => a + b, 0);

// Placeholder "photo" drawn in SVG; Halftone turns it into a dot screen.
const PlaceholderPhoto: React.FC<{ w: number; h: number }> = ({ w, h }) => (
  <>
    <defs>
      <linearGradient id="photo-sky" x1={0} y1={0} x2={0} y2={1}>
        <stop offset={0} stopColor="#ffffff" />
        <stop offset={1} stopColor="#8f8f8f" />
      </linearGradient>
    </defs>
    <rect width={w} height={h} fill="url(#photo-sky)" />
    <circle cx={w * 0.72} cy={h * 0.28} r={h * 0.12} fill="#f4f4f4" />
    {[0.04, 0.16, 0.3, 0.46, 0.6, 0.78].map((x, i) => (
      <rect
        key={x}
        x={w * x}
        y={h * (0.35 + random(`b${i}`) * 0.25)}
        width={w * 0.14}
        height={h}
        fill={i % 2 ? "#4a4a4a" : "#6a6a6a"}
      />
    ))}
    <rect y={h * 0.82} width={w} height={h * 0.18} fill="#1e1e1e" />
  </>
);

// --- Scene 1: front page (V4 headline card: ink-in, tag snap, rule draw, brush swipe, snap zoom, pan up)
const FrontPage: React.FC = () => {
  const f = stepped(useCurrentFrame());
  return (
    <AbsoluteFill style={{ background: color.agedPaper }}>
      <PaperTexture amount={0.3} />
      <AbsoluteFill
        style={{
          transformOrigin: "50% 40%",
          // Snap zoom in 2 drawings as the brush lands, snap back before the pan (V4 f7–8, f31–32)
          scale:
            interpolate(f, [38, 42], [1, 1.22], {
              ...clamp,
              easing: ease.accel,
            }) *
            interpolate(f, [78, 82], [1, 1 / 1.22], {
              ...clamp,
              easing: ease.accel,
            }),
          // Pan up with ease-in and a hard stop (V4 f94–97: −207 px in 3 drawings)
          translate: `0px ${interpolate(f, [86, 94], [0, -330], { ...clamp, easing: ease.accel })}px`,
        }}
      >
        <NewsClipping
          width={1380}
          height={1330}
          seed="front"
          style={{ position: "absolute", left: 270, top: 70, rotate: "-1deg" }}
        >
          <div style={{ padding: "48px 70px", color: color.newsInk }}>
            <div
              style={{
                display: "inline-block",
                background: color.dateTag,
                color: "#F4EFE6",
                fontFamily: serif,
                fontSize: 28,
                padding: "8px 18px",
                opacity: f >= 14 ? 0.92 : 0,
                translate: `0px ${interpolate(f, [16, 20], [28, 0], clamp)}px`,
              }}
            >
              MARCH 3, 19XX
            </div>
            <Letterpress
              seed={2}
              style={{ textAlign: "center", marginTop: -10 }}
            >
              <div
                style={{
                  fontFamily: blackletter,
                  fontSize: 76,
                  lineHeight: 1.1,
                }}
              >
                The Daily Placeholder
              </div>
            </Letterpress>
            <div
              style={{
                height: 4,
                background: color.newsInk,
                marginTop: 8,
                scale: `${interpolate(f, [22, 30], [0, 1], clamp)} 1`,
              }}
            />
            <div
              style={{
                height: 1,
                background: color.newsInk,
                marginTop: 4,
                scale: `${interpolate(f, [24, 32], [0, 1], clamp)} 1`,
              }}
            />
            <Letterpress
              reveal={interpolate(f, [2, 10], [0, 1], clamp)}
              seed={5}
              style={{
                fontFamily: serif,
                fontWeight: 900,
                fontSize: 92,
                lineHeight: 1.02,
                textAlign: "center",
                marginTop: 34,
                letterSpacing: "-0.01em",
              }}
            >
              CITY ADOPTS ITS FIRST
              <br />
              <BrushHighlight start={40} duration={10} seed={7}>
                OFFICIAL STREET MAP
              </BrushHighlight>
            </Letterpress>
            <div
              style={{
                fontFamily: serif,
                fontStyle: "italic",
                fontSize: 26,
                textAlign: "center",
                marginTop: 18,
                opacity: f >= 30 ? 1 : 0,
              }}
            >
              By a staff correspondent
            </div>
            <div
              style={{
                height: 1,
                background: color.newsInk,
                margin: "22px 0 26px",
              }}
            />
            <Letterpress
              reveal={interpolate(f, [94, 102], [0, 1], clamp)}
              seed={9}
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr 1.15fr",
                gap: 34,
                fontFamily: serif,
                fontSize: 22,
                lineHeight: 1.38,
                textAlign: "justify",
                hyphens: "auto",
              }}
            >
              <div>{fillerText(6)}</div>
              <div>
                {fillerText(2, 3)}{" "}
                <BrushHighlight
                  start={112}
                  duration={8}
                  seed={11}
                  easing={(t) => t}
                >
                  The river had moved.
                </BrushHighlight>{" "}
                {fillerText(3, 1)}
              </div>
              <div>
                <Halftone width={440} height={330} cell={7}>
                  <PlaceholderPhoto w={440} h={330} />
                </Halftone>
                <div
                  style={{ fontStyle: "italic", fontSize: 18, marginTop: 8 }}
                >
                  Placeholder photo, halftone screen.
                </div>
              </div>
            </Letterpress>
          </div>
        </NewsClipping>
      </AbsoluteFill>
      <Vignette strength={0.13} />
      <Grain amount={0.15} />
    </AbsoluteFill>
  );
};

// --- Scene 2: headline burst (V1 f2275–2361): fast hard cuts, keyword brushed at the same screen spot
type Headline = {
  before: string;
  after: string;
  family: string;
  weight: number;
  italic?: boolean;
  size: number;
};
const HEADLINES: Headline[] = [
  {
    before: "NEW",
    after: "REDRAWS THE CITY",
    family: serif,
    weight: 900,
    size: 120,
  },
  {
    before: "WHO OWNS THE",
    after: "?",
    family: condensed,
    weight: 700,
    size: 150,
  },
  {
    before: "A",
    after: "NOBODY ASKED FOR",
    family: serif,
    weight: 700,
    italic: true,
    size: 116,
  },
  {
    before: "",
    after: "ERRORS COST MILLIONS",
    family: sans,
    weight: 700,
    size: 104,
  },
  {
    before: "THE",
    after: "WAR HEATS UP",
    family: condensed,
    weight: 600,
    size: 150,
  },
  {
    before: "COUNCIL VOTES ON",
    after: "",
    family: serif,
    weight: 900,
    size: 112,
  },
  {
    before: "",
    after: "MAKERS WIN APPEAL",
    family: condensed,
    weight: 700,
    size: 140,
  },
  {
    before: "THE",
    after: "THAT CHANGED IT ALL",
    family: serif,
    weight: 900,
    size: 116,
  },
];

const BurstClip: React.FC<{ h: Headline; i: number; held: boolean }> = ({
  h,
  i,
  held,
}) => {
  const r = (k: string) => random(`burst-${i}-${k}`) - 0.5;
  return (
    <AbsoluteFill style={{ background: color.agedPaper }}>
      <NewsClipping
        width={2200}
        height={1400}
        seed={`burst-${i}`}
        style={{
          position: "absolute",
          left: -140,
          top: -160,
          rotate: `${r("rot") * 4}deg`,
        }}
      >
        <Letterpress
          seed={20 + i}
          style={{ color: color.newsInk, fontFamily: serif }}
        >
          <div
            style={{
              columnCount: 6,
              columnGap: 40,
              fontSize: 21,
              lineHeight: 1.35,
              padding: "60px 160px",
              height: 330,
              opacity: 0.85,
              textAlign: "justify",
            }}
          >
            {fillerText(14, i)}
          </div>
          <div
            style={{
              display: "grid",
              // minmax(0,1fr) keeps both side columns equal even when text overflows,
              // so the keyword stays on the same screen spot in every clip
              gridTemplateColumns: "minmax(0,1fr) auto minmax(0,1fr)",
              alignItems: "baseline",
              columnGap: "0.25em",
              // keyword column sits on x = 960 of the frame (clip is offset −140 px)
              width: 1920 + 280 - 2 * 140,
              marginLeft: 140,
              padding: "0 0 0 0",
              fontFamily: h.family,
              fontWeight: h.weight,
              fontStyle: h.italic ? "italic" : "normal",
              fontSize: h.size,
              lineHeight: 1,
              marginTop: 40,
            }}
          >
            <span
              style={{
                display: "flex",
                justifyContent: "flex-end",
                whiteSpace: "nowrap",
              }}
            >
              {h.before}
            </span>
            <BrushHighlight start={held ? 8 : -20} duration={10} seed={30 + i}>
              MAP
            </BrushHighlight>
            <span style={{ textAlign: "left", whiteSpace: "nowrap" }}>
              {h.after}
            </span>
          </div>
          <div
            style={{
              columnCount: 6,
              columnGap: 40,
              fontSize: 21,
              lineHeight: 1.35,
              padding: "70px 160px",
              opacity: 0.85,
              textAlign: "justify",
            }}
          >
            {fillerText(18, i + 2)}
          </div>
        </Letterpress>
      </NewsClipping>
      <Vignette strength={0.3} />
      <Grain amount={0.2} />
    </AbsoluteFill>
  );
};

// --- SFX (original, synthesised by scripts/make-sfx.sh). Each cue lands on the visual event it belongs to;
// whooshes start with their move because they peak at the end, like the ease-in moves they follow.
type Cue = { at: number; sfx: string; volume: number; rate?: number };
const burstStarts = BURST.map(
  (_, i) => FRONT + BURST.slice(0, i).reduce((a, b) => a + b, 0),
);
const CUES: Cue[] = [
  { at: 0, sfx: "paper-rustle", volume: 0.5 }, // clipping lands, headline inks in
  { at: 20, sfx: "stamp-thunk", volume: 0.55 }, // date tag snaps into place
  { at: 38, sfx: "whoosh-snap", volume: 0.45 }, // snap zoom in (f38–42)
  { at: 40, sfx: "brush-swish", volume: 0.9 }, // brush swipe (f40–50, ease-in)
  { at: 78, sfx: "whoosh-snap", volume: 0.35, rate: 0.85 }, // snap zoom out
  { at: 86, sfx: "whoosh-pan", volume: 0.5 }, // pan up (f86–94)
  { at: 112, sfx: "brush-swish", volume: 0.5, rate: 1.25 }, // second, shorter brush (8 f)
  // Headline burst: one paper slap per hard cut, slightly varied so repeats don't sound identical
  ...burstStarts.map((at, i) => ({
    at,
    sfx: "paper-slap",
    volume: 0.55 + random(`slap-v${i}`) * 0.2,
    rate: 0.9 + random(`slap-r${i}`) * 0.25,
  })),
  {
    at: burstStarts[burstStarts.length - 1] + 8,
    sfx: "brush-swish",
    volume: 0.9,
  }, // held clip brush
];

const SfxTrack: React.FC = () => (
  <>
    {CUES.map((c, i) => (
      <Sequence key={i} from={c.at} name={`SFX ${c.sfx}`} layout="none">
        <Audio
          src={staticFile(`sfx/${c.sfx}.wav`)}
          volume={c.volume}
          playbackRate={c.rate ?? 1}
        />
      </Sequence>
    ))}
  </>
);

const Fade: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: "#000",
        opacity: interpolate(frame, [TOTAL - 20, TOTAL], [0, 1], clamp),
      }}
    />
  );
};

export const NewspaperDemoVideo: React.FC = () => (
  <AbsoluteFill>
    <Series>
      <Series.Sequence
        name="Front page"
        durationInFrames={FRONT}
        style={{
          scale: 1.087
        }}
      >
        <FrontPage />
      </Series.Sequence>
      {HEADLINES.map((h, i) => (
        <Series.Sequence
          key={i}
          name={`Headline ${i + 1}`}
          durationInFrames={BURST[i]}
        >
          <BurstClip h={h} i={i} held={i === HEADLINES.length - 1} />
        </Series.Sequence>
      ))}
    </Series>
    <Fade />
    <SfxTrack />
  </AbsoluteFill>
);

export const NewspaperDemo: React.FC = () => (
  <Composition
    id="NewspaperDemo"
    component={NewspaperDemoVideo}
    durationInFrames={TOTAL}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
