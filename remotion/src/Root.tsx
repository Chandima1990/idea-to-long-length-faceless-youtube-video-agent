import { Composition } from "remotion";
import { ViralBrollVideo, calculateViralBrollMetadata } from "./ViralBrollVideo";

export const RemotionRoot: React.FC = () => {
  return (
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
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={300}
    />
  );
};
