import React from "react";
import { AbsoluteFill, Img, Audio, Sequence, useVideoConfig, interpolate, useCurrentFrame } from "remotion";

export type ViralShortProps = {
  audioUrl: string;
  audioDurationS: number;
  slides: Array<{
    url: string;
    startS: number;
    endS: number;
    motion?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right" | "static";
  }>;
  captionsSrt: string;
  brand: {
    primaryColor: string;
    secondaryColor: string;
    logoUrl?: string;
    handle?: string;
  };
};

export const defaultProps: ViralShortProps = {
  audioUrl: "",
  audioDurationS: 45,
  slides: [],
  captionsSrt: "",
  brand: {
    primaryColor: "#8FDF65",
    secondaryColor: "#000000",
    handle: "@brand",
  },
};

const Slide: React.FC<{
  url: string;
  startS: number;
  endS: number;
  motion?: ViralShortProps["slides"][number]["motion"];
}> = ({ url, startS, endS, motion = "zoom-in" }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const fromFrame = startS * fps;
  const durationFrames = (endS - startS) * fps;
  const localFrame = frame - fromFrame;

  // Subtle Ken Burns effect
  const scale = motion === "zoom-in"
    ? interpolate(localFrame, [0, durationFrames], [1.0, 1.08])
    : motion === "zoom-out"
    ? interpolate(localFrame, [0, durationFrames], [1.08, 1.0])
    : 1;

  // Cross-fade in/out
  const opacity = interpolate(
    localFrame,
    [0, fps * 0.3, durationFrames - fps * 0.3, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", opacity }}>
      <Img
        src={url}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />
    </AbsoluteFill>
  );
};

// Stub básico — captions virão word-by-word do SRT em iteração futura.
// Por enquanto: parse simples e mostra a frase atual.
const Captions: React.FC<{ srt: string; primaryColor: string }> = ({ srt, primaryColor }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const currentS = frame / fps;

  // Parse SRT inline
  const blocks = srt.split(/\n\n+/).filter(Boolean);
  const cues = blocks.map((b) => {
    const lines = b.split("\n");
    if (lines.length < 3) return null;
    const time = lines[1];
    const m = time.match(/(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})/);
    if (!m) return null;
    const startS = +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000;
    const endS = +m[5] * 3600 + +m[6] * 60 + +m[7] + +m[8] / 1000;
    return { startS, endS, text: lines.slice(2).join(" ") };
  }).filter(Boolean) as { startS: number; endS: number; text: string }[];

  const active = cues.find((c) => currentS >= c.startS && currentS < c.endS);
  if (!active) return null;

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 220 }}>
      <div
        style={{
          background: "rgba(0,0,0,0.65)",
          color: "#fff",
          padding: "16px 24px",
          borderRadius: 12,
          fontFamily: "Inter, sans-serif",
          fontWeight: 800,
          fontSize: 56,
          lineHeight: 1.2,
          maxWidth: "85%",
          textAlign: "center",
          textShadow: "0 2px 8px rgba(0,0,0,0.8)",
        }}
      >
        {active.text}
      </div>
    </AbsoluteFill>
  );
};

const BrandOverlay: React.FC<{ brand: ViralShortProps["brand"] }> = ({ brand }) => {
  if (!brand.handle) return null;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 60,
          background: "rgba(0,0,0,0.55)",
          padding: "8px 16px",
          borderRadius: 999,
          color: "#fff",
          fontSize: 28,
          fontFamily: "Inter, sans-serif",
          fontWeight: 600,
        }}
      >
        {brand.handle}
      </div>
    </AbsoluteFill>
  );
};

export const ViralShort: React.FC<ViralShortProps> = ({
  audioUrl,
  audioDurationS,
  slides,
  captionsSrt,
  brand,
}) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: brand.secondaryColor }}>
      {slides.map((s, i) => (
        <Sequence key={i} from={Math.floor(s.startS * fps)} durationInFrames={Math.ceil((s.endS - s.startS) * fps)}>
          <Slide url={s.url} startS={s.startS} endS={s.endS} motion={s.motion} />
        </Sequence>
      ))}
      <Captions srt={captionsSrt} primaryColor={brand.primaryColor} />
      <BrandOverlay brand={brand} />
      {audioUrl ? <Audio src={audioUrl} /> : null}
    </AbsoluteFill>
  );
};
