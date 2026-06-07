import {
  AbsoluteFill,
  Audio,
  CalculateMetadataFunction,
  OffthreadVideo,
  Sequence,
  staticFile,
} from "remotion";
import { SceneImage } from "./components/SceneImage";
import { CaptionOverlay } from "./components/CaptionOverlay";
import { FilmGrain } from "./components/FilmGrain";
import { TransitionEffect } from "./components/TransitionEffect";
import { SceneData, ViralBrollProps, WordTimestamp } from "./types";

const FPS = 30;

const SceneVisual: React.FC<{
  scene: SceneData;
  imagePath: string;
  durationFrames: number;
}> = ({ scene, imagePath, durationFrames }) => {
  if (!scene.video_src) {
    return <SceneImage src={imagePath} kenBurns={scene.ken_burns} />;
  }

  const videoFrames = Math.min(
    durationFrames,
    Math.round((scene.video_duration ?? scene.duration) * FPS),
  );
  const remainingFrames = Math.max(0, durationFrames - videoFrames);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Sequence from={0} durationInFrames={videoFrames}>
        <OffthreadVideo
          src={staticFile(scene.video_src)}
          volume={scene.video_volume ?? 0.18}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </Sequence>

      {remainingFrames > 0 && (
        <Sequence from={videoFrames} durationInFrames={remainingFrames}>
          <SceneImage src={imagePath} kenBurns={scene.ken_burns} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

export const calculateViralBrollMetadata: CalculateMetadataFunction<ViralBrollProps> = async ({
  props,
}) => {
  const totalSeconds = (props.scenes || []).reduce(
    (sum: number, s: SceneData) => sum + s.duration,
    0,
  );

  return {
    durationInFrames: Math.max(1, Math.ceil(totalSeconds * FPS)),
    fps: FPS,
    width: 1920,
    height: 1080,
  };
};

export const ViralBrollVideo: React.FC<ViralBrollProps> = ({
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
              <SceneVisual
                scene={scene}
                imagePath={imagePath}
                durationFrames={durationFrames}
              />
              <TransitionEffect type={scene.transition} />
            </Sequence>
          );
        })}
      </FilmGrain>

      <Audio src={staticFile("narration.mp3")} />

      {words && words.length > 0 && <CaptionOverlay words={words} />}
    </AbsoluteFill>
  );
};
