(() => {
  const ART = {
    width: 1600,
    height: 900,
    seed: 20260825,
    palette: {
      paper: "#f4f0e6",
      ink: "#28343a",
      coral: "#c55f4b",
      teal: "#4d8582",
      yellow: "#d1a94a",
    },
  };

  function paintBackground() {
    brush.noStroke();
    brush.fill(ART.palette.teal, 52);
    brush.circle(-470, -170, 330, true);

    brush.fill(ART.palette.yellow, 42);
    brush.circle(460, 190, 420, true);
  }

  function paintSubject() {
    brush.noFill();
    brush.set("HB", ART.palette.ink, 2.2);
    brush.rect(-420, -170, 290, 220, "center");
    brush.rect(-40, -170, 290, 220, "center");

    for (let y = -250; y <= -90; y += 52) {
      brush.line(-315, y, -145, y + 18);
    }

    brush.set("rotring", ART.palette.coral, 2.5);
    brush.line(120, -170, 330, -170);
    brush.line(310, -188, 340, -170);
    brush.line(310, -152, 340, -170);
  }

  function paintAccents() {
    const positions = [
      [390, -250, 160],
      [470, -115, 215],
      [370, 35, 190],
    ];

    brush.noStroke();
    for (const [x, y, diameter] of positions) {
      brush.fill(ART.palette.teal, 78);
      brush.circle(x, y, diameter, true);
    }

    brush.noFill();
    brush.set("2B", ART.palette.ink, 1.2);
    brush.line(-590, 230, 570, 230);
    brush.line(-510, 285, 440, 285);
  }

  const canvas = brush.createCanvas(ART.width, ART.height, {
    parent: "#art",
    id: "paint-with-code-canvas",
  });

  brush.seed(ART.seed);
  brush.noiseSeed(ART.seed);
  brush.clear(ART.palette.paper);
  brush.scaleBrushes(3);

  paintBackground();
  paintSubject();
  paintAccents();
  brush.render();

  canvas.dataset.paintReady = "true";
  window.__PAINT_WITH_CODE_READY__ = {
    canvasId: canvas.id,
    width: ART.width,
    height: ART.height,
    seed: ART.seed,
  };
})();
