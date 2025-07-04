function setup() {
    createCanvas(800, 800);
    background(0, 128, 0); // Green background
    textAlign(CENTER, CENTER);
    textSize(16);
    noLoop();
  }
  
  function draw() {
    // Circles
    stroke(255); // White outline
    noFill();
    ellipse(400, 400, 700, 700); // Outer circle: 5 fingers = 700px diameter
    ellipse(400, 400, 640, 640); // Inner circle: 700 - 2*30 = 640px
  
    // Shemhamphorasch: 72 letters in the band
    const letters = "htoexorabaslayqciystalgaaonosvlarycekspfyomeneauarelatedatononaoylepotma".split('');
    for (let i = 0; i < 72; i++) {
      let angle = i * 5; // 360 / 72 = 5 degrees
      let rad = 335; // Midpoint of band: (350 + 320) / 2
      let x = 400 + rad * cos(radians(angle));
      let y = 400 + rad * sin(radians(angle));
      push();
      translate(x, y);
      rotate(radians(angle));
      text(letters[i], 0, 0);
      pop();
    }
  
    // Small cross at apex (top of band)
    stroke(255);
    line(400, 50, 400, 70); // Vertical
    line(390, 60, 410, 60); // Horizontal
  
    // Pentagram
    const pentagramAngles = [90, 162, 234, 306, 18];
    let pentPoints = [];
    for (let angle of pentagramAngles) {
      let x = 400 + 320 * cos(radians(angle));
      let y = 400 + 320 * sin(radians(angle));
      pentPoints.push({x, y});
    }
    stroke(255, 0, 0); // Red
    line(pentPoints[0].x, pentPoints[0].y, pentPoints[2].x, pentPoints[2].y);
    line(pentPoints[2].x, pentPoints[2].y, pentPoints[4].x, pentPoints[4].y);
    line(pentPoints[4].x, pentPoints[4].y, pentPoints[1].x, pentPoints[1].y);
    line(pentPoints[1].x, pentPoints[1].y, pentPoints[3].x, pentPoints[3].y);
    line(pentPoints[3].x, pentPoints[3].y, pentPoints[0].x, pentPoints[0].y);
  
    // Tau at center
    textSize(40);
    fill(255);
    text("T", 400, 400);
    textSize(16);
    noFill();
  
    // Names around Tau
    const names = ["E", "L", "E", "L", "Y"];
    const pairs = ["lx", "al", "a", "c", "to"];
    for (let i = 0; i < 5; i++) {
      let angle = 90 + i * 72;
      let x1 = 400 + 60 * cos(radians(angle));
      let y1 = 400 + 60 * sin(radians(angle));
      text(names[i], x1, y1);
      let x2 = 400 + 80 * cos(radians(angle));
      let y2 = 400 + 80 * sin(radians(angle));
      text(pairs[i], x2, y2);
    }
  
    // Heptagons
    const radii = [120, 100, 80];
    const colors = [[0, 0, 255], [255, 255, 0], [255, 255, 0]]; // Blue, Yellow, Yellow
    const angels = ["Zadkiel", "Samael", "Zfadkiel", "Raphael", "Anael", "Michael", "Gabriel"];
    for (let r = 0; r < 3; r++) {
      let points = [];
      for (let k = 0; k < 7; k++) {
        let angle = k * (360 / 7);
        let x = 400 + radii[r] * cos(radians(angle));
        let y = 400 + radii[r] * sin(radians(angle));
        points.push({x, y});
      }
      stroke(colors[r][0], colors[r][1], colors[r][2]);
      beginShape();
      for (let p of points) vertex(p.x, p.y);
      endShape(CLOSE);
  
      // Labels for first heptagon
      if (r === 0) {
        for (let i = 0; i < 7; i++) {
          let p1 = points[i];
          let p2 = points[(i + 1) % 7];
          let mx = (p1.x + p2.x) / 2;
          let my = (p1.y + p2.y) / 2;
          let angle = atan2(p2.y - p1.y, p2.x - p1.x);
          push();
          translate(mx, my);
          rotate(angle);
          text(angels[i], 0, 0);
          pop();
        }
      }
  
      // Black circles and crosses for third heptagon
      if (r === 2) {
        fill(0);
        noStroke();
        for (let p of points) ellipse(p.x, p.y, 10, 10);
        stroke(0);
        for (let p of points) {
          line(p.x - 5, p.y, p.x + 5, p.y);
          line(p.x, p.y - 5, p.x, p.y + 5);
        }
      }
    }
  }