import React from "react";
import { Composition } from "remotion";
import { ViralShort, ViralShortProps, defaultProps } from "./compositions/ViralShort";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="ViralShort"
        component={ViralShort}
        durationInFrames={45 * 30}  // 45s at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultProps}
        calculateMetadata={({ props }) => {
          const durationS = props.audioDurationS ?? 45;
          return { durationInFrames: Math.ceil(durationS * 30) };
        }}
      />
    </>
  );
};
