import { Easing } from "remotion";

// Design tokens extracted in reference-style-system/STYLE_BIBLE.md.
// MEASURED values cite reference-analysis/color/COLOR_TEXTURE.md; ESTIMATE values are labelled.

export const color = {
  // Backgrounds
  paper: "#F6F5EA", // flat digital paper (V3 f2877) MEASURED
  paperWarm: "#E5DDC6", // warm cream (V2 f270) MEASURED
  paperCollage: "#EBE1D8", // V1 collage paper, centre of #F2E8DF→#DED4CE vignette MEASURED range
  dark: "#12100D", // V1 dark interstitial MEASURED
  // Ink
  ink: "#201E18", // V3 title/body ink MEASURED
  inkSoft: "#393733", // V4 headline ink MEASURED
  textOnDark: "#E3E3E3", // V3 credits MEASURED
  // Accents
  highlight: "#F0E136", // highlighter (V3 f3740) MEASURED
  highlightPure: "#F6EA00", // title box / tape (V1 f1260) MEASURED
  gold: "#EAB718", // disc accent (V2) MEASURED
  red: "#FC3828", // data red (V3) MEASURED
  redDeep: "#8B1C1B", // bullets / hand circles (V2, V1) MEASURED
  blue: "#50B7FE", // data blue (V3) MEASURED — fills only, fails as text (2.0:1)
  green: "#62C583", // chart green (V3) MEASURED
  pink: "#FF85C1", // chart pink (V3) MEASURED
  purple: "#BA75BB", // chart purple (V3) MEASURED
  grid: "#CDCCC2", // grid-paper hairline (V3) MEASURED
  greyMap: "#99989B", // inactive map/region grey (V3) MEASURED
  // Newspaper
  agedPaper: "#C4BDB2", // V4 crumpled-paper ground, centre MEASURED
  newsprint: "#E7E0CF", // clipping stock ESTIMATE (lighter than V4 ground so the clipping separates)
  newsInk: "#3A3835", // V4 headline ink MEASURED
  dateTag: "#7D3130", // V4 date-tag maroon MEASURED
  brush: "#F8E10F", // dry-brush yellow; more saturated than #F0E136 so it survives multiply on newsprint
  brushOchre: "#E2B33A", // V4 ochre stroke ≈ multiply of #FBCC59 ESTIMATE, brightened
} as const;

export const shadow = {
  cardLarge: "10px 12px 27px 2px rgba(0,0,0,.62)", // ESTIMATE fit, V5 f0
  cardSmall: "4px 5px 10px 2px rgba(0,0,0,.5)", // ESTIMATE fit, V3 f12012
} as const;

// Easing library. All curves are ESTIMATES fitted to tracked motion (see MOTION_RECIPES.md).
// No reference move showed spring overshoot, so none of these overshoot.
export const ease = {
  pop: Easing.bezier(0.16, 0.7, 0.7, 1), // ease-out fitted to V2 disc .55/.80/.95 (RMS 0.005): pops, highlight blocks
  expo: Easing.bezier(0.16, 1, 0.3, 1), // expo-out: tape slide (V5 D2), TV pop (V1 D16)
  grow: Easing.bezier(0.25, 1, 0.5, 1), // quart-out: bars (V3 D8)
  punch: Easing.bezier(0.2, 0.8, 0.3, 1), // cubic/quart-out: punch-in, whip pan (V3 D2, V6 D7)
  push: Easing.bezier(0.7, 0, 0.4, 1), // in-out cubic: camera push to detail (V3 D11)
  tilt: Easing.bezier(0.45, 0, 0.55, 1), // in-out sine: soft push (V6 D3)
  pan: Easing.bezier(0.55, 0, 0.1, 1), // short ease-in, long tail: lateral pan (V3 D10)
  accel: Easing.bezier(0.55, 0, 1, 0.45), // ease-in: push into a cut (V6 D10, V1 D22)
  wipe: Easing.bezier(0.37, 0, 0.63, 1), // sine in-out: highlighter per line (V3 D7)
} as const;

// Graphics animate "on twos": 12 drawings/s on a 24 fps timeline (V3 D0, V6 D1, V1 ~12 fps).
export const STEP = 2;
export const stepped = (frame: number, step: number = STEP) =>
  Math.floor(frame / step) * step;

export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;
