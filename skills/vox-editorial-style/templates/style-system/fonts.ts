import { loadFont as loadSerif } from "@remotion/google-fonts/SourceSerif4";
import { loadFont as loadSans } from "@remotion/google-fonts/Inter";
import { loadFont as loadMarker } from "@remotion/google-fonts/PermanentMarker";
import { loadFont as loadBlackletter } from "@remotion/google-fonts/UnifrakturMaguntia";
import { loadFont as loadCondensed } from "@remotion/google-fonts/Oswald";

// Free stand-ins for the references' proprietary faces (ESTIMATE matches, see TYPOGRAPHY_AND_LAYOUT.md).
export const serif = loadSerif("normal", {
  weights: ["400", "600", "700", "900"],
  subsets: ["latin"],
}).fontFamily;
loadSerif("italic", { weights: ["400", "700"], subsets: ["latin"] });

export const sans = loadSans("normal", {
  weights: ["400", "500", "700"],
  subsets: ["latin"],
}).fontFamily;

export const marker = loadMarker("normal", {
  weights: ["400"],
  subsets: ["latin"],
}).fontFamily;

// Newspaper roles: blackletter masthead (V4 masthead) and condensed tabloid headline.
export const blackletter = loadBlackletter("normal", {
  weights: ["400"],
  subsets: ["latin"],
}).fontFamily;

export const condensed = loadCondensed("normal", {
  weights: ["600", "700"],
  subsets: ["latin"],
}).fontFamily;
