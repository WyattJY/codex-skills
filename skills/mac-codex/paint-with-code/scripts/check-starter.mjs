import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const indexPath = path.join(skillRoot, "assets", "starter", "index.html");
const sketchPath = path.join(skillRoot, "assets", "starter", "sketch.js");
const vendorPath = path.join(skillRoot, "assets", "starter", "vendor", "brush.js");
const licensePath = path.join(skillRoot, "assets", "starter", "vendor", "LICENSE.p5.brush.md");

const [html, sketch, vendor, license] = await Promise.all([
  readFile(indexPath, "utf8"),
  readFile(sketchPath, "utf8"),
  readFile(vendorPath, "utf8"),
  readFile(licensePath, "utf8"),
]);

const requirements = [
  [html.includes("./vendor/brush.js"), "load the vendored p5.brush build"],
  [!html.includes("cdn.jsdelivr.net"), "avoid runtime CDN dependency"],
  [html.includes("./sketch.js"), "load the editable sketch"],
  [vendor.length > 50000 && vendor.includes("createCanvas"), "include the standalone p5.brush build"],
  [license.includes("MIT License"), "include the p5.brush license"],
  [sketch.includes("brush.createCanvas"), "create a standalone brush canvas"],
  [sketch.includes("brush.seed("), "seed brush randomness"],
  [sketch.includes("brush.noiseSeed("), "seed brush noise"],
  [sketch.includes("brush.render()"), "flush the standalone render"],
  [sketch.includes("__PAINT_WITH_CODE_READY__"), "expose a render-ready marker"],
  [sketch.includes("dataset.paintReady"), "expose a DOM-visible ready marker"],
];

const failures = requirements.filter(([ok]) => !ok).map(([, message]) => message);
if (failures.length) {
  throw new Error(`Starter validation failed: ${failures.join(", ")}`);
}

console.log("paint-with-code starter validation passed");
