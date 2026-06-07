import { Composition } from "remotion";
import { ViralBrollVideo, calculateViralBrollMetadata } from "./ViralBrollVideo";
import { ShortsVideo, calculateShortsMetadata } from "./ShortsVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ViralBrollVideo"
        component={ViralBrollVideo}
        calculateMetadata={calculateViralBrollMetadata}
        defaultProps={{
          outputDir: "",
          filmPreset: "clean_modern",
          scenes: [],
          words: [],
        }}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={300}
      />
      <Composition
        id="ShortsVideo"
        component={ShortsVideo}
        calculateMetadata={calculateShortsMetadata}
        defaultProps={{
          outputDir: "",
          filmPreset: "vector_infographic",
          scenes: [],
          words: [],
        }}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={1800}
      />
    </>
  );
};
