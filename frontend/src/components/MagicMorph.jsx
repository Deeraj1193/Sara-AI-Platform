// src/components/MagicMorph.jsx
import { useEffect, useRef } from "react";

/**
 * MagicMorph
 * A WebGL fullscreen shader-driven liquid morph overlay.
 *
 * Props:
 *  - trigger (number) : increment to start a new morph
 *  - durationMs (number) optional : total animation duration (default 900)
 *  - onComplete() optional : callback when animation is done
 *
 * Notes:
 *  - pointerEvents: none, placed on top (z-index high)
 *  - uses raw WebGL (no libs)
 */

function MagicMorph({ trigger, durationMs = 900, onComplete }) {
  const canvasRef = useRef(null);
  const rafRef = useRef(null);
  const startRef = useRef(null);
  const glRef = useRef(null);
  const progRef = useRef(null);

  useEffect(() => {
    if (trigger == null) return;
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Setup GL
    const gl = canvas.getContext("webgl", { antialias: true, alpha: true });
    if (!gl) {
      console.warn("WebGL not available");
      onComplete && onComplete();
      return;
    }
    glRef.current = gl;

    // Vertex shader (simple quad)
    const VERT = `
      attribute vec2 a_position;
      varying vec2 v_uv;
      void main() {
        v_uv = a_position * 0.5 + 0.5;
        gl_Position = vec4(a_position, 0.0, 1.0);
      }
    `;

    // Fragment shader: procedural liquid noise + sweep + bloom-like highlight
    // Uses a few fbm layers for organic motion.
    const FRAG = `
      precision highp float;
      varying vec2 v_uv;
      uniform float u_time;
      uniform float u_progress; // 0..1 progress of morph
      uniform vec2 u_res;
      // 2D random / noise (iq)
      float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453123); }
      float noise(vec2 p){
        vec2 i = floor(p);
        vec2 f = fract(p);
        vec2 u = f*f*(3.0-2.0*f);
        return mix(mix(hash(i+vec2(0.0,0.0)), hash(i+vec2(1.0,0.0)), u.x),
                   mix(hash(i+vec2(0.0,1.0)), hash(i+vec2(1.0,1.0)), u.x),
                   u.y);
      }
      float fbm(vec2 p){
        float v=0.0; float a=0.5;
        for(int i=0;i<5;i++){
          v += a*noise(p);
          p *= 2.0;
          a *= 0.5;
        }
        return v;
      }

      // palette for soft pastel glow
      vec3 palette(float t) {
        vec3 a = vec3(0.96,0.85,0.92); // pink-white base
        vec3 b = vec3(0.88,0.56,0.86); // bright pink
        vec3 c = vec3(0.76,0.85,0.98); // baby blue highlight
        return mix(a, mix(b,c, smoothstep(0.35, 0.9, t)), 0.7);
      }

      void main(){
        vec2 uv = v_uv;
        // aspect correction for noise scale
        vec2 pos = (uv - 0.5) * vec2(u_res.x/u_res.y, 1.0);

        // base time
        float t = u_time * 0.6;

        // a moving fbm field
        float n = fbm(vec2(pos.x*1.2 + t*0.45, pos.y*1.0 - t*0.25));
        float n2 = fbm(vec2(pos.x*2.0 - t*0.8, pos.y*2.0 + t*0.6));

        // create a flow vector for distortion
        vec2 flow = vec2(n2 - 0.5, n - 0.5) * 0.35;

        // progress-driven amplitude: starts quickly then eases
        float amp = mix(0.0, 1.6, smoothstep(0.0, 0.85, u_progress));
        // use a softened envelope so effect peaks near u_progress ~0.45 then decays
        float env = exp(-((u_progress-0.45)*(u_progress-0.45))*8.0);

        // final distortion
        vec2 disp = flow * amp * env * 0.9;

        // sample uv with displacement (we don't sample textures; instead we draw shader effect)
        vec2 sampleUv = uv + disp * 0.06;

        // luminous sweep: moving band across the screen tied to progress
        float sweepPos = mix(-0.6, 1.6, u_progress);
        float sweep = smoothstep(sweepPos-0.18, sweepPos, uv.x) * (1.0 - smoothstep(sweepPos, sweepPos+0.18, uv.x));
        sweep *= 1.2;

        // color base from fbm
        float m = fbm(uv*3.0 + t*0.9);
        float accent = smoothstep(0.2, 0.8, m);

        // layering the colors
        vec3 col = palette(m * 0.9 + 0.05) * (0.6 + 0.6*accent);
        // add sweep highlight
        col += vec3(1.0,0.88,1.0) * sweep * 0.8 * (0.6 + 0.4*env);

        // add soft vignetting and subtle rim
        float vign = 1.0 - smoothstep(0.0, 0.9, length((uv-0.5)*vec2(u_res.x/u_res.y,1.0)));
        col *= 0.95 + 0.35 * vign;

        // final mix with subtle glassiness driven by progress
        float glass = smoothstep(0.05, 0.6, u_progress);
        // glass overlay adds contrast and brightness
        col = mix(col * 0.95, col + vec3(0.12,0.08,0.12) * (0.6+env), glass*0.9);

        // apply soft gamma
        col = pow(col, vec3(0.92));

        // final alpha fade: stronger near mid-progress
        float alpha = smoothstep(0.02, 0.95, env * (0.5 + 0.9*u_progress));

        gl_FragColor = vec4(col, alpha);
      }
    `;

    // compile helper
    function compileShader(src, type) {
      const shader = gl.createShader(type);
      gl.shaderSource(shader, src);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Shader compile error:", gl.getShaderInfoLog(shader), src);
        gl.deleteShader(shader);
        return null;
      }
      return shader;
    }

    // build program
    const vs = compileShader(VERT, gl.VERTEX_SHADER);
    const fs = compileShader(FRAG, gl.FRAGMENT_SHADER);
    if (!vs || !fs) {
      onComplete && onComplete();
      return;
    }

    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.error("Program link error:", gl.getProgramInfoLog(prog));
      onComplete && onComplete();
      return;
    }
    progRef.current = prog;
    gl.useProgram(prog);

    // create vertex buffer for a full-screen quad
    const posLoc = gl.getAttribLocation(prog, "a_position");
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    const quad = new Float32Array([
      -1, -1,
      1, -1,
      -1, 1,
      -1, 1,
      1, -1,
      1, 1
    ]);
    gl.bufferData(gl.ARRAY_BUFFER, quad, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

    // uniforms
    const uTimeLoc = gl.getUniformLocation(prog, "u_time");
    const uProgLoc = gl.getUniformLocation(prog, "u_progress");
    const uResLoc = gl.getUniformLocation(prog, "u_res");

    // resize canvas to device pixel ratio
    function resize() {
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const width = Math.floor(canvas.clientWidth * dpr);
      const height = Math.floor(canvas.clientHeight * dpr);
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, width, height);
      }
      // pass resolution in normalized coords
      gl.uniform2f(uResLoc, canvas.width / dpr, canvas.height / dpr);
    }
    resize();
    window.addEventListener("resize", resize);

    // animation loop
    startRef.current = performance.now();
    let stopped = false;

    function frame(now) {
      if (stopped) return;
      const elapsed = now - startRef.current;
      const progT = Math.min(1, elapsed / durationMs);

      // update uniforms
      gl.uniform1f(uTimeLoc, elapsed * 0.001);
      gl.uniform1f(uProgLoc, progT);

      // clear and draw
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 6);

      if (progT >= 1) {
        // finish, wait a tiny bit so final frame is visible then cleanup
        setTimeout(() => {
          stopped = true;
          // cleanup GL resources
          try {
            gl.deleteProgram(prog);
            gl.deleteShader(vs);
            gl.deleteShader(fs);
            gl.deleteBuffer(buffer);
          } catch (e) {}
          window.removeEventListener("resize", resize);
          onComplete && onComplete();
        }, 60);
        return;
      }

      rafRef.current = requestAnimationFrame(frame);
    }

    rafRef.current = requestAnimationFrame(frame);

    // cleanup on unmount or when re-trigger
    return () => {
      stopped = true;
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      try {
        gl.deleteProgram(prog);
        gl.deleteShader(vs);
        gl.deleteShader(fs);
      } catch (e) {}
      window.removeEventListener("resize", resize);
    };
  }, [trigger, durationMs, onComplete]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        inset: 0,
        width: "100vw",
        height: "100vh",
        pointerEvents: "none",
        zIndex: 99999,
        mixBlendMode: "screen", /* add luminous blending, you can change to 'normal' if too bright */
      }}
    />
  );
}

export default MagicMorph;
