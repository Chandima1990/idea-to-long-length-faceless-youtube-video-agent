import { AbsoluteFill, Audio, CalculateMetadataFunction, Sequence, staticFile } from "remotion";
import { SceneImage } from "./components/SceneImage";
import { CaptionOverlay } from "./components/CaptionOverlay";
import { FilmGrain } from "./components/FilmGrain";
import { TransitionEffect } from "./components/TransitionEffect";
import { SceneData, ViralBrollProps, WordTimestamp } from "./types";

const FPS = 30;

export const calculateShortsMetadata: CalculateMetadataFunction<ViralBrollProps> = async ({
  props,
}) => {
  const totalSeconds = (props.scenes || []).reduce(
    (sum: number, s: SceneData) => sum + s.duration,
    0,
  );

  return {
    durationInFrames: Math.max(1, Math.ceil(totalSeconds * FPS)),
    fps: FPS,
    width: 1080,
    height: 1920,
  };
};

export const ShortsVideo: React.FC<ViralBrollProps> = ({
  outputDir,
  filmPreset,
  scenes,
  words,
}) => {
  if (!scenes || scenes.length === 0) {
    return <AbsoluteFill style={{ backgroundColor: "#000" }} />;
  }

  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <FilmGrain preset={filmPreset}>
        {scenes.map((scene, i) => {
          const durationFrames = Math.round(scene.duration * FPS);
          const fromFrame = currentFrame;
          currentFrame += durationFrames;

          const imagePath = staticFile(
            `images/scene_${String(i + 1).padStart(3, "0")}.png`,
          );

          return (
            <Sequence key={i} from={fromFrame} durationInFrames={durationFrames}>
              <SceneImage src={imagePath} kenBurns={scene.ken_burns} />
              <TransitionEffect type={scene.transition} />
            </Sequence>
          );
        })}
      </FilmGrain>

      <Audio src={staticFile("narration.mp3")} />

      {words && words.length > 0 && (
        <CaptionOverlay
          words={words}
          wordsPerPage={4}
          fontSize={72}
        />
      )}
    </AbsoluteFill>
  );
};
