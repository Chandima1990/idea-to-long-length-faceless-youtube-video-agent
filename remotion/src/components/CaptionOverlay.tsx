import {
  AbsoluteFill,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { WordTimestamp } from "../types";

interface CaptionOverlayProps {
  words: WordTimestamp[];
  fontSize?: number;
  color?: string;
  strokeColor?: string;
  fontFamily?: string;
}

const cleanWord = (word: string) => word.trim();

const WordRenderer: React.FC<{
  word: string;
  fontSize: number;
  color: string;
  strokeColor: string;
  fontFamily: string;
}> = ({ word, fontSize, color, strokeColor, fontFamily }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 260, mass: 0.45 },
    durationInFrames: 6,
  });
  const scale = 0.9 + Math.min(pop, 1) * 0.1;

  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "56%",
          width: "92%",
          textAlign: "center",
          transform: `translate(-50%, -50%) scale(${scale})`,
          transformOrigin: "center center",
        }}
      >
        <span
          style={{
            color,
            fontFamily,
            fontSize,
            fontWeight: 900,
            lineHeight: 0.95,
            letterSpacing: 0,
            textTransform: "uppercase",
            WebkitTextStroke: `14px ${strokeColor}`,
            paintOrder: "stroke fill",
            textShadow: "0 10px 16px rgba(0,0,0,0.55)",
            overflowWrap: "break-word",
          }}
        >
          {word}
        </span>
      </div>
    </AbsoluteFill>
  );
};

export const CaptionOverlay: React.FC<CaptionOverlayProps> = ({
  words,
  fontSize = 118,
  color = "#FFFFFF",
  strokeColor = "#000000",
  fontFamily = "Arial Black, Impact, sans-serif",
}) => {
  const { fps } = useVideoConfig();
  const visibleWords = words
    .map((word) => ({ ...word, word: cleanWord(word.word) }))
    .filter((word) => word.word.length > 0);

  return (
    <AbsoluteFill>
      {visibleWords.map((word, i) => {
        const fromFrame = Math.round((word.startMs / 1000) * fps);
        const nextStartMs = visibleWords[i + 1]?.startMs ?? word.endMs + 180;
        const durationMs = Math.max(80, nextStartMs - word.startMs);
        const duration = Math.max(1, Math.round((durationMs / 1000) * fps));

        return (
          <Sequence key={`${word.startMs}-${i}`} from={fromFrame} durationInFrames={duration}>
            <WordRenderer
              word={word.word}
              fontSize={fontSize}
              color={color}
              strokeColor={strokeColor}
              fontFamily={fontFamily}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
