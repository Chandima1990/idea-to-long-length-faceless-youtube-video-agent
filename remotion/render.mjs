import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const outputDir = process.argv[2];
const filmPreset = process.argv[3] || "clean_modern";
const outputFile = process.argv[4] || path.join(outputDir, "final.mp4");
const compositionId = process.argv[5] || "ViralBrollVideo";
const browserExecutable =
  process.env.REMOTION_BROWSER_EXECUTABLE ||
  (fs.existsSync("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    : fs.existsSync(path.join(__dirname, "node_modules", ".remotion", "chrome-headless-shell", "win64", "chrome-headless-shell-win64", "chrome-headless-shell.exe"))
      ? path.join(__dirname, "node_modules", ".remotion", "chrome-headless-shell", "win64", "chrome-headless-shell-win64", "chrome-headless-shell.exe")
      : null);

if (!outputDir) {
  console.error("Usage: node render.mjs <outputDir> [filmPreset] [outputFile]");
  process.exit(1);
}

const absOutputDir = path.resolve(outputDir);

const scenesRaw = JSON.parse(fs.readFileSync(path.join(absOutputDir, "scenes.json"), "utf8"));
const words = JSON.parse(fs.readFileSync(path.join(absOutputDir, "words.json"), "utf8"));

const inputProps = {
  outputDir: absOutputDir,
  filmPreset,
  scenes: scenesRaw.scenes,
  words,
};

const entry = path.join(__dirname, "src", "index.tsx");

async function main() {
  console.log(`Bundling Remotion project...`);
  const bundled = await bundle({ entryPoint: entry, publicDir: absOutputDir });

  console.log(`Selecting composition: ${compositionId}...`);
  const composition = await selectComposition({
    serveUrl: bundled,
    id: compositionId,
    inputProps,
    browserExecutable,
  });

  console.log(`Rendering ${composition.durationInFrames} frames at ${composition.fps}fps...`);
  console.log(`Output: ${outputFile}`);
  await renderMedia({
    composition,
    serveUrl: bundled,
    codec: "h264",
    outputLocation: outputFile,
    inputProps,
    browserExecutable,
    chromiumOptions: {
      enableMultiProcessOnLinux: false,
      args: ["--allow-file-access-from-files", "--disable-web-security"],
    },
  });

  console.log(`Done: ${outputFile}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
