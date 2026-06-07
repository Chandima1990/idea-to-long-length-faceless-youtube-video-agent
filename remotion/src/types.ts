export interface KenBurnsConfig {
  startX: number;
  endX: number;
  startY: number;
  endY: number;
  startScale: number;
  endScale: number;
}

export type TransitionType = "dissolve" | "white_flash" | "fade_black";

export type ShotType = "wide" | "medium" | "close_up" | "detail" | "aerial" | "establishing";

export interface SceneData {
  scene_number: number;
  narration_text: string;
  duration: number;
  image_prompt: string;
  video_src?: string;
  video_duration?: number;
  video_volume?: number;
  shot_type: ShotType;
  ken_burns: string;
  transition: TransitionType;
}

export interface FilmPreset {
  filter: string;
  grain: number;
  vignette: number;
}

export interface WordTimestamp {
  word: string;
  startMs: number;
  endMs: number;
}

export interface CaptionConfig {
  words: WordTimestamp[];
  wordsPerPage?: number;
  fontSize?: number;
  color?: string;
  highlightColor?: string;
  backgroundColor?: string;
}

export interface ViralBrollInputProps {
  outputDir: string;
  filmPreset: string;
}

export interface ViralBrollProps {
  outputDir: string;
  filmPreset: string;
  scenes: SceneData[];
  words: WordTimestamp[];
}
