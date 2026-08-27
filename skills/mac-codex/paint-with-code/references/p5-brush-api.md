# Verified p5.brush Surface

The starter vendors the standalone browser build of `p5.brush` 2.2.1 and its MIT license. Keep the `vendor/` directory when copying the starter. Prefer this compact surface instead of pasting the full API into a generation prompt.

Official source and current documentation: <https://github.com/acamposuribe/p5.brush>

## Lifecycle

```js
const canvas = brush.createCanvas(width, height, {
  parent: "#art",
  id: "paint-with-code-canvas",
});

brush.seed(20260825);
brush.noiseSeed(20260825);
brush.clear("#f4f0e6");

// Drawing calls...

brush.render();
canvas.dataset.paintReady = "true";
window.__PAINT_WITH_CODE_READY__ = {
  canvasId: canvas.id,
  width,
  height,
};
```

The standalone build requires WebGL2. `brush.render()` is mandatory after drawing calls. Automation should wait for `canvas[data-paint-ready="true"]`; the window marker is a convenience for ordinary page scripts.

## Default Drawing Allowlist

| Purpose | Calls |
| --- | --- |
| State | `brush.push()`, `brush.pop()` |
| Transform | `brush.translate()`, `brush.rotate()`, `brush.scale()` |
| Brush | `brush.scaleBrushes()`, `brush.set()`, `brush.strokeWeight()`, `brush.noStroke()` |
| Interior | `brush.fill()`, `brush.fillTexture()`, `brush.noFill()` |
| Geometry | `brush.line()`, `brush.circle()`, `brush.rect()`, `brush.polygon()` |
| Organic paths | `brush.beginShape()`, `brush.vertex()`, `brush.endShape()` |

Only add flow fields, custom brushes, hatching, mass, clipping, or image tips when the composition needs them and the pinned version's documentation confirms the signature.

## Coordinate Model

The brush geometry is centered on the canvas. For a `1600 x 900` canvas, useful coordinates generally span `x = -800..800` and `y = -450..450`. Keep a margin so textured strokes are not clipped.

## Editing Pattern

Keep artistic choices declarative:

```js
const ART = {
  width: 1600,
  height: 900,
  seed: 20260825,
  palette: {
    paper: "#f4f0e6",
    ink: "#243036",
    accent: "#c45d45",
  },
  layout: {
    subjectX: -180,
    subjectY: 20,
  },
};
```

Split the drawing into named functions such as `paintBackground()`, `paintSubject()`, and `paintAccents()`. A revision should normally change configuration or one layer function, not replace the whole sketch.

## Browser Verification

After the ready marker appears:

1. Confirm the canvas backing dimensions match the request.
2. Sample canvas pixels or inspect an image histogram to reject blank/near-uniform output.
3. Inspect a screenshot at the final aspect ratio.
4. Check the browser console for WebGL, API, and cross-origin errors.
5. Export the canvas itself so page chrome is not included in the PNG.
