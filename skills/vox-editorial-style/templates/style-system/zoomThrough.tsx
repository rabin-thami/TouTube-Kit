import React from "react";
import { AbsoluteFill, interpolate } from "remotion";
import type {
  TransitionPresentation,
  TransitionPresentationComponentProps,
} from "@remotion/transitions";
import { clamp, ease } from "./tokens";

// "Zoom-through" cut (V6 f436–492): outgoing shot accelerates in (×1.29 over 24 f, ease-in),
// hard cut, incoming shot decelerates from ×1.82 to ×1 (28 f, ease-out). No cross-fade.
type Props = {
  split: number;
  outScale: number;
  inScale: number;
  durationInFrames: number;
};

const ZoomThroughPresentation: React.FC<
  TransitionPresentationComponentProps<Props>
> = ({
  children,
  presentationDirection,
  presentationProgress,
  passedProps,
}) => {
  const { split, outScale, inScale, durationInFrames } = passedProps;
  // Quantise to twos so the camera move matches the on-twos graphics.
  const t =
    (Math.floor((presentationProgress * durationInFrames) / 2) * 2) /
    durationInFrames;
  if (presentationDirection === "exiting") {
    return (
      <AbsoluteFill
        style={{
          opacity: t < split ? 1 : 0,
          scale: interpolate(t, [0, split], [1, outScale], {
            ...clamp,
            easing: ease.accel,
          }),
        }}
      >
        {children}
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill
      style={{
        opacity: t < split ? 0 : 1,
        scale: interpolate(t, [split, 1], [inScale, 1], {
          ...clamp,
          easing: ease.punch,
        }),
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export const zoomThrough = (
  durationInFrames: number,
  opts: Partial<Omit<Props, "durationInFrames">> = {},
): TransitionPresentation<Props> => ({
  component: ZoomThroughPresentation,
  props: {
    split: 24 / 52,
    outScale: 1.29,
    inScale: 1.82,
    durationInFrames,
    ...opts,
  },
});
