// node assets/core/selfcheck.mjs — asserts the core math matches the measured references.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  EASE_POINTS, ease, onTwos, stepTime, stepFrame, tween, tweenScale,
  seeded, tornClipPath, boilSeed,
} from "./editorial-core.js";

const near = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg}: ${a} vs ${b}`);

// tokens.json and core agree on ease control points
const tokens = JSON.parse(readFileSync(new URL("../tokens.json", import.meta.url)));
for (const [k, v] of Object.entries(EASE_POINTS)) assert.deepEqual(tokens.ease[k], v, `ease ${k}`);

// endpoints, monotonic, no overshoot
for (const [k, f] of Object.entries(ease)) {
  assert.equal(f(0), 0, k); assert.equal(f(1), 1, k);
  let prev = 0;
  for (let p = 0; p <= 1; p += 0.01) {
    const v = f(p);
    assert.ok(v >= prev - 1e-6, `${k} monotonic`);
    assert.ok(v <= 1 + 1e-9, `${k} overshoot`);
    prev = v;
  }
}
// Measured anchors: V3 bars (grow) ~50% at 6/30 and ~90% at 14/30; V3 node push 0.50 at 53%; V2 disc (pop) .55/.81
near(ease.grow(6 / 30), 0.5, 0.12, "grow 50%");
near(ease.grow(14 / 30), 0.9, 0.06, "grow 90%");
near(ease.push(0.53), 0.5, 0.08, "push mid");
near(ease.pop(0.25), 0.55, 0.05, "pop q1");
near(ease.pop(0.5), 0.81, 0.05, "pop q2");
// V5 tape (expo): ~85% of travel in the first ~1 s of a 3.9 s move
near(ease.expo(1 / 3.9), 0.85, 0.08, "expo first second");

// stepping: 12 drawings/s
near(stepTime(0.09), 1 / 12, 1e-12, "stepTime");
assert.equal(stepFrame(5), 4);
const t2 = onTwos((p) => p, 1); // 1 s tween → 12 steps + final value
assert.equal(new Set(Array.from({ length: 241 }, (_, i) => t2(i / 240))).size, 13);
// tween / log zoom
assert.equal(tween(0.5, 0, 1, 0, 100), 50);
near(tweenScale(0.5, 0, 1, 1, 4), 2, 1e-9, "log zoom");
// determinism
assert.equal(seeded("a"), seeded("a"));
assert.notEqual(seeded("a"), seeded("b"));
assert.equal(tornClipPath(100, 50, "x"), tornClipPath(100, 50, "x"));
assert.deepEqual([0, 1, 2, 3, 4, 5].map((k) => boilSeed(k / 12)), [1, 1, 2, 1, 1, 2]);
console.log("editorial-core selfcheck: all assertions passed");
