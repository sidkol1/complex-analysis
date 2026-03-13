---
title: Complex Differentiation
date: 2026-03-12
---

When I ask people to explain what it might mean to take the derivative of a function $g:\mathbb{C}\rightarrow\mathbb{C}$, they sometimes muse about slopes of planes in four-dimensional-space. This mistake happens because they are overly commited to one of many possible conceptions of a *derivative*.

Indeed, there are many ways to mentally model the idea of a derivative. According to one such model, the derivative of a function $f: \mathbb{R}\rightarrow\mathbb{R}$ at a point $x_0$ is the slope of the tangent line of $f$ at $x_0$. 

Displayed below is the derivative of $x^2$ at a point $x_0$, denoted by a yellow dot. The derivative is given by the slope of the red line tangent to $f$ at $x_0$. 

![Tangent line animation](assets/tangent-line.gif)


This notion of a derivative makes many unnecessary assumptions about $f$. For one, it assumes $f$ has a *graph*, and that a point on this graph can be associated with its *tangent* line. Both of these assumptions fail to generalize to higher dimensions and to complex numbers. 

For this reason, I prefer the equivalent *limit* definition of a derivative. On this view, the derivative of $f$ at $x_0$ is the average rate of change of $f$ between $x_0$ and points close to $x_0$. (If this seems unfamiliar, recall that the average rate of change in $f$ between $x_0$ and $x$ is $\frac{f(x) - f(x_0)}{x - x_0})$. 

In other words, the choice of a point $x_0$ induces a single-variable difference function $R_{x_0}(x) := \frac{f(x) - f(x_0)}{x - x_0}$. (When the choice of $x_0$ and $x$ are clear from context, we will refer to this quantity with the notation $\frac{\Delta{f}}{\Delta{x}}$). The quantity $f'(x_0)$ is the value assumeed by this difference function throughout small neighborhoods of $x_0$. 

How can we visualize the limit definition? One way is to imagine the real line with a point $x_0$ fixed. Now for each number $x \neq x_0$, we can calculate the average rate of change in $f$ between $x$ and $x_0$. The derivative is the limit of this rate as $x \rightarrow x_0$ (the "rate-of-change-function" has a hole at $x = x_0$, which does not pose an issue for finding its *limit*). If $f(x) = x^2$ and we want to calculate $f'(1)$, this looks like the following:

![Average rate of change](assets/avg-rate-of-change.gif)

Try it yourself by dragging the red dot corresponding to $x$:

<div class="interactive-real-line" style="position:relative; margin:1.5em 0;">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.4em;">
    <div style="font-size:0.9em;">
      <span id="rl-x0-input-label" style="color:#e8c840;"></span>
      <input id="rl-x0-input" type="number" step="any" value="1" style="width:3.5em; font-family:Georgia,serif; font-size:0.95em; border:1px solid #ccc; border-radius:3px; padding:2px 4px; margin-left:2px;">
    </div>
    <div id="rl-readout" style="font-size:1.1em; min-height:1.6em;"></div>
  </div>
  <div style="position:relative;">
    <svg id="rl-svg" width="100%" viewBox="0 0 600 80" style="display:block; user-select:none;">
      <line x1="40" y1="40" x2="560" y2="40" stroke="#222" stroke-width="1.5" id="rl-axis"/>
      <polygon points="560,40 553,36 553,44" fill="#222" id="rl-arrow"/>
      <g id="rl-ticks"></g>
      <circle cx="0" cy="40" r="6" fill="#e8c840" id="rl-x0-dot"/>
      <circle cx="0" cy="40" r="7" fill="#e05050" id="rl-x-dot" style="cursor:grab;"/>
    </svg>
    <div id="rl-x0-lbl" style="position:absolute; pointer-events:none;"></div>
    <div id="rl-x-lbl" style="position:absolute; pointer-events:none;"></div>
  </div>
  <div style="text-align:center; font-size:0.8em; color:#999; margin-top:0.3em;">scroll to zoom</div>
  <script>
  (function() {
    var svg = document.getElementById('rl-svg');
    var readout = document.getElementById('rl-readout');
    var xDot = document.getElementById('rl-x-dot');
    var x0Dot = document.getElementById('rl-x0-dot');
    var x0Lbl = document.getElementById('rl-x0-lbl');
    var xLbl = document.getElementById('rl-x-lbl');
    var ticksG = document.getElementById('rl-ticks');
    var x0Input = document.getElementById('rl-x0-input');
    var x0InputLabel = document.getElementById('rl-x0-input-label');
    var pxLeft = 40, pxRight = 550;
    var x0 = 1, xVal = 3;
    var xMin = -2, xMax = 4;

    x0InputLabel.innerHTML = katex.renderToString('x_0 =', { throwOnError: false });

    function toSvgX(v) { return pxLeft + (v - xMin) / (xMax - xMin) * (pxRight - pxLeft); }
    function fromSvgX(px) { return xMin + (px - pxLeft) / (pxRight - pxLeft) * (xMax - xMin); }

    function svgToPage(svgX, svgY) {
      var rect = svg.getBoundingClientRect();
      var vb = svg.viewBox.baseVal;
      return {
        x: rect.left + (svgX - vb.x) / vb.width * rect.width,
        y: rect.top + (svgY - vb.y) / vb.height * rect.height
      };
    }

    function drawTicks() {
      ticksG.innerHTML = '';
      var range = xMax - xMin;
      var step = range <= 2 ? 0.25 : range <= 5 ? 0.5 : range <= 12 ? 1 : 2;
      var start = Math.ceil(xMin / step) * step;
      for (var t = start; t <= xMax; t += step) {
        var px = toSvgX(t);
        var tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        tick.setAttribute('x1', px); tick.setAttribute('x2', px);
        tick.setAttribute('y1', 35); tick.setAttribute('y2', 45);
        tick.setAttribute('stroke', '#222'); tick.setAttribute('stroke-width', '1');
        ticksG.appendChild(tick);
        var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', px); label.setAttribute('y', 28);
        label.setAttribute('text-anchor', 'middle'); label.setAttribute('font-size', '12');
        label.setAttribute('fill', '#666'); label.setAttribute('font-family', 'Georgia, serif');
        label.textContent = parseFloat(t.toFixed(4));
        ticksG.appendChild(label);
      }
    }

    function update() {
      xDot.setAttribute('cx', toSvgX(xVal));
      x0Dot.setAttribute('cx', toSvgX(x0));
      readout.innerHTML = katex.renderToString(
        '\\frac{\\Delta f}{\\Delta x} = ' + (xVal + x0).toFixed(2),
        { throwOnError: false }
      );
      var wrapper = svg.parentElement;
      var p0 = svgToPage(toSvgX(x0), 55);
      var pX = svgToPage(toSvgX(xVal), 55);
      var wrapRect = wrapper.getBoundingClientRect();
      x0Lbl.innerHTML = katex.renderToString('x_0', { throwOnError: false });
      x0Lbl.style.left = (p0.x - wrapRect.left - 8) + 'px';
      x0Lbl.style.top = (p0.y - wrapRect.top) + 'px';
      x0Lbl.style.color = '#e8c840';
      x0Lbl.style.fontSize = '0.85em';
      xLbl.innerHTML = katex.renderToString('x', { throwOnError: false });
      xLbl.style.left = (pX.x - wrapRect.left - 5) + 'px';
      xLbl.style.top = (pX.y - wrapRect.top) + 'px';
      xLbl.style.color = '#e05050';
      xLbl.style.fontSize = '0.85em';
    }

    x0Input.addEventListener('input', function() {
      var v = parseFloat(x0Input.value);
      if (!isNaN(v)) {
        x0 = v; xVal = x0 + 2;
        var mid = (x0 + xVal) / 2;
        var half = Math.max(Math.abs(xVal - x0), 2) * 1.5;
        xMin = mid - half; xMax = mid + half;
        drawTicks(); update();
      }
    });

    var dragging = false;
    function startDrag(e) { dragging = true; xDot.style.cursor = 'grabbing'; e.preventDefault(); }
    function endDrag() { dragging = false; xDot.style.cursor = 'grab'; }
    function onMove(e) {
      if (!dragging) return;
      var pt = svg.createSVGPoint();
      pt.x = e.touches ? e.touches[0].clientX : e.clientX;
      pt.y = e.touches ? e.touches[0].clientY : e.clientY;
      var svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
      xVal = fromSvgX(svgP.x);
      var eps = (xMax - xMin) * 0.005;
      if (Math.abs(xVal - x0) < eps) xVal = x0 + eps;
      update();
    }
    xDot.addEventListener('mousedown', startDrag);
    xDot.addEventListener('touchstart', startDrag, { passive: false });
    window.addEventListener('mousemove', onMove);
    window.addEventListener('touchmove', onMove, { passive: false });
    window.addEventListener('mouseup', endDrag);
    window.addEventListener('touchend', endDrag);

    svg.addEventListener('wheel', function(e) {
      e.preventDefault();
      var pt = svg.createSVGPoint();
      pt.x = e.clientX; pt.y = e.clientY;
      var svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
      var center = fromSvgX(svgP.x);
      var factor = e.deltaY > 0 ? 1.15 : 1 / 1.15;
      xMin = center + (xMin - center) * factor;
      xMax = center + (xMax - center) * factor;
      drawTicks();
      update();
    }, { passive: false });

    drawTicks();
    update();
  })();
  </script>
</div>

Since $\frac{\Delta{f}}{\Delta{x}} \rightarrow 2$ as $x \rightarrow 1$, we conclude that $f'(1) = 2$. If we want to calculate the derivative of $f$ at a different point, we have to move the yellow dot $x_0$ and repeat this process. The point of calculating $\lim_{x \rightarrow x_0}\frac{f(x) - f(x_0)}{x - x_0}$ is, of course, to approximate $f(x)$ for $x$ close to $x_0$. And this is the notion of derivatives that is easy to generalize to complex numbers. 

Suppose that $g: \mathbb{C} \rightarrow \mathbb{C}$. We would expect the derivative of $g$ at a point $z_0$ to be the averate rate of change in $g$ between $z_0$ and points close to $z_0$ (or more specifically, the limit of this rate of change). Defining the average rate of change in $\mathbb{C}$ amounts to just swapping some variables for other ones in the definition for $\mathbb{R}$. Between $z_0$ and $z$, the average rate of change in $g$ is $\frac{g(z) - g(z_0)}{z - z_0}$. 

The above guess is correct. Let's consider $g(z) = z^2$ and its derivative at $z_0 = 1 + i$. We'll calculate the average rate of change between $z_0$ and $z$ for various choices of $z$, and observe what happens when $z$ gets close to $z_0$. 

![Complex average rate of change](assets/complex-avg-rate.gif)

Try it yourself by dragging the red dot corresponding to $z$ around the complex plane:

<div class="interactive-complex-plane" style="position:relative; margin:1.5em 0;">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.4em; flex-wrap:wrap; gap:0.4em;">
    <div style="font-size:0.9em; display:flex; align-items:center; gap:4px;">
      <span id="cp-z0-input-label" style="color:#e8c840;"></span>
      <input id="cp-z0-re-input" type="number" step="any" value="1" style="width:3.5em; font-family:Georgia,serif; font-size:0.95em; border:1px solid #ccc; border-radius:3px; padding:2px 4px;">
      <span style="color:#888;">+</span>
      <input id="cp-z0-im-input" type="number" step="any" value="1" style="width:3.5em; font-family:Georgia,serif; font-size:0.95em; border:1px solid #ccc; border-radius:3px; padding:2px 4px;">
      <span style="color:#888; font-style:italic;">i</span>
    </div>
    <div id="cp-readout" style="font-size:1.1em; min-height:1.6em;"></div>
  </div>
  <div style="position:relative;">
    <svg id="cp-svg" width="100%" viewBox="0 0 500 500" style="display:block; user-select:none;">
      <g id="cp-axes"></g>
      <g id="cp-ticks"></g>
      <circle cx="0" cy="0" r="6" fill="#e8c840" id="cp-z0-dot"/>
      <circle cx="0" cy="0" r="7" fill="#e05050" id="cp-z-dot" style="cursor:grab;"/>
    </svg>
    <div id="cp-z0-lbl" style="position:absolute; pointer-events:none;"></div>
    <div id="cp-z-lbl" style="position:absolute; pointer-events:none;"></div>
  </div>
  <div style="text-align:center; font-size:0.8em; color:#999; margin-top:0.3em;">scroll to zoom</div>
  <script>
  (function() {
    var svg = document.getElementById('cp-svg');
    var readout = document.getElementById('cp-readout');
    var zDot = document.getElementById('cp-z-dot');
    var z0Dot = document.getElementById('cp-z0-dot');
    var z0Lbl = document.getElementById('cp-z0-lbl');
    var zLbl = document.getElementById('cp-z-lbl');
    var ticksG = document.getElementById('cp-ticks');
    var axesG = document.getElementById('cp-axes');
    var z0ReInput = document.getElementById('cp-z0-re-input');
    var z0ImInput = document.getElementById('cp-z0-im-input');
    var z0InputLabel = document.getElementById('cp-z0-input-label');
    var pxMin = 30, pxMax = 470;
    var z0Re = 1, z0Im = 1, zRe = 3, zIm = 0;
    var vXMin = -3, vXMax = 4, vYMin = -3, vYMax = 4;

    z0InputLabel.innerHTML = katex.renderToString('z_0 =', { throwOnError: false });

    function toSvgX(v) { return pxMin + (v - vXMin) / (vXMax - vXMin) * (pxMax - pxMin); }
    function toSvgY(v) { return pxMax - (v - vYMin) / (vYMax - vYMin) * (pxMax - pxMin); }
    function fromSvgX(px) { return vXMin + (px - pxMin) / (pxMax - pxMin) * (vXMax - vXMin); }
    function fromSvgY(py) { return vYMin + (pxMax - py) / (pxMax - pxMin) * (vYMax - vYMin); }

    function svgToPage(sx, sy) {
      var rect = svg.getBoundingClientRect();
      var vb = svg.viewBox.baseVal;
      return {
        x: rect.left + (sx - vb.x) / vb.width * rect.width,
        y: rect.top + (sy - vb.y) / vb.height * rect.height
      };
    }

    function drawAxes() {
      axesG.innerHTML = '';
      var ox = toSvgX(0), oy = toSvgY(0);
      var clamp = function(v) { return Math.max(pxMin, Math.min(pxMax, v)); };
      function ln(x1,y1,x2,y2) {
        var l = document.createElementNS('http://www.w3.org/2000/svg','line');
        l.setAttribute('x1',x1); l.setAttribute('y1',y1);
        l.setAttribute('x2',x2); l.setAttribute('y2',y2);
        l.setAttribute('stroke','#222'); l.setAttribute('stroke-width','1.2');
        axesG.appendChild(l);
      }
      if (oy >= pxMin && oy <= pxMax) { ln(pxMin, oy, pxMax, oy); }
      if (ox >= pxMin && ox <= pxMax) { ln(ox, pxMax, ox, pxMin); }
      var t = document.createElementNS('http://www.w3.org/2000/svg','text');
      t.setAttribute('x', pxMax + 8); t.setAttribute('y', clamp(oy) + 4);
      t.setAttribute('font-size','13'); t.setAttribute('fill','#666');
      t.setAttribute('font-family','Georgia, serif'); t.textContent = 'Re';
      axesG.appendChild(t);
      t = document.createElementNS('http://www.w3.org/2000/svg','text');
      t.setAttribute('x', clamp(ox) + 6); t.setAttribute('y', pxMin - 6);
      t.setAttribute('font-size','13'); t.setAttribute('fill','#666');
      t.setAttribute('font-family','Georgia, serif'); t.textContent = 'Im';
      axesG.appendChild(t);
    }

    function drawTicks() {
      ticksG.innerHTML = '';
      var rangeX = vXMax - vXMin;
      var step = rangeX <= 2 ? 0.25 : rangeX <= 5 ? 0.5 : rangeX <= 12 ? 1 : 2;
      var ox = toSvgX(0), oy = toSvgY(0);
      var start, t, px, py, tick, label;
      start = Math.ceil(vXMin / step) * step;
      for (t = start; t <= vXMax; t += step) {
        if (Math.abs(t) < step * 0.1) continue;
        px = toSvgX(t);
        tick = document.createElementNS('http://www.w3.org/2000/svg','line');
        tick.setAttribute('x1',px); tick.setAttribute('x2',px);
        tick.setAttribute('y1',oy-4); tick.setAttribute('y2',oy+4);
        tick.setAttribute('stroke','#222'); tick.setAttribute('stroke-width','1');
        ticksG.appendChild(tick);
        label = document.createElementNS('http://www.w3.org/2000/svg','text');
        label.setAttribute('x',px); label.setAttribute('y',oy+18);
        label.setAttribute('text-anchor','middle'); label.setAttribute('font-size','11');
        label.setAttribute('fill','#888'); label.setAttribute('font-family','Georgia, serif');
        label.textContent = parseFloat(t.toFixed(4));
        ticksG.appendChild(label);
      }
      start = Math.ceil(vYMin / step) * step;
      for (t = start; t <= vYMax; t += step) {
        if (Math.abs(t) < step * 0.1) continue;
        py = toSvgY(t);
        tick = document.createElementNS('http://www.w3.org/2000/svg','line');
        tick.setAttribute('x1',ox-4); tick.setAttribute('x2',ox+4);
        tick.setAttribute('y1',py); tick.setAttribute('y2',py);
        tick.setAttribute('stroke','#222'); tick.setAttribute('stroke-width','1');
        ticksG.appendChild(tick);
        label = document.createElementNS('http://www.w3.org/2000/svg','text');
        label.setAttribute('x',ox-10); label.setAttribute('y',py+4);
        label.setAttribute('text-anchor','end'); label.setAttribute('font-size','11');
        label.setAttribute('fill','#888'); label.setAttribute('font-family','Georgia, serif');
        label.textContent = parseFloat(t.toFixed(4));
        ticksG.appendChild(label);
      }
    }

    function update() {
      zDot.setAttribute('cx', toSvgX(zRe));
      zDot.setAttribute('cy', toSvgY(zIm));
      z0Dot.setAttribute('cx', toSvgX(z0Re));
      z0Dot.setAttribute('cy', toSvgY(z0Im));
      var re = zRe + z0Re, im = zIm + z0Im;
      var sign = im >= 0 ? '+' : '-';
      readout.innerHTML = katex.renderToString(
        '\\frac{\\Delta g}{\\Delta z} = ' + re.toFixed(2) + ' ' + sign + ' ' + Math.abs(im).toFixed(2) + 'i',
        { throwOnError: false }
      );
      var wrapper = svg.parentElement;
      var wrapRect = wrapper.getBoundingClientRect();
      var p0 = svgToPage(toSvgX(z0Re), toSvgY(z0Im));
      var pZ = svgToPage(toSvgX(zRe), toSvgY(zIm));
      z0Lbl.innerHTML = katex.renderToString('z_0', { throwOnError: false });
      z0Lbl.style.left = (p0.x - wrapRect.left + 8) + 'px';
      z0Lbl.style.top = (p0.y - wrapRect.top + 4) + 'px';
      z0Lbl.style.color = '#e8c840'; z0Lbl.style.fontSize = '0.85em';
      zLbl.innerHTML = katex.renderToString('z', { throwOnError: false });
      zLbl.style.left = (pZ.x - wrapRect.left + 8) + 'px';
      zLbl.style.top = (pZ.y - wrapRect.top + 4) + 'px';
      zLbl.style.color = '#e05050'; zLbl.style.fontSize = '0.85em';
    }

    function onZ0Input() {
      var re = parseFloat(z0ReInput.value), im = parseFloat(z0ImInput.value);
      if (!isNaN(re)) z0Re = re;
      if (!isNaN(im)) z0Im = im;
      zRe = z0Re + 2; zIm = z0Im - 1;
      var midX = (z0Re + zRe) / 2, midY = (z0Im + zIm) / 2;
      var span = Math.max(Math.abs(zRe - z0Re), Math.abs(zIm - z0Im), 2) * 1.5;
      vXMin = midX - span; vXMax = midX + span;
      vYMin = midY - span; vYMax = midY + span;
      drawAxes(); drawTicks(); update();
    }
    z0ReInput.addEventListener('input', onZ0Input);
    z0ImInput.addEventListener('input', onZ0Input);

    var dragging = false;
    function startDrag(e) { dragging = true; zDot.style.cursor = 'grabbing'; e.preventDefault(); }
    function endDrag() { dragging = false; zDot.style.cursor = 'grab'; }
    function onMove(e) {
      if (!dragging) return;
      var pt = svg.createSVGPoint();
      pt.x = e.touches ? e.touches[0].clientX : e.clientX;
      pt.y = e.touches ? e.touches[0].clientY : e.clientY;
      var svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
      zRe = fromSvgX(svgP.x);
      zIm = fromSvgY(svgP.y);
      var eps = (vXMax - vXMin) * 0.005;
      if (Math.abs(zRe - z0Re) < eps && Math.abs(zIm - z0Im) < eps) zRe = z0Re + eps;
      update();
    }
    zDot.addEventListener('mousedown', startDrag);
    zDot.addEventListener('touchstart', startDrag, { passive: false });
    window.addEventListener('mousemove', onMove);
    window.addEventListener('touchmove', onMove, { passive: false });
    window.addEventListener('mouseup', endDrag);
    window.addEventListener('touchend', endDrag);

    svg.addEventListener('wheel', function(e) {
      e.preventDefault();
      var pt = svg.createSVGPoint();
      pt.x = e.clientX; pt.y = e.clientY;
      var svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
      var cx = fromSvgX(svgP.x), cy = fromSvgY(svgP.y);
      var factor = e.deltaY > 0 ? 1.15 : 1 / 1.15;
      vXMin = cx + (vXMin - cx) * factor;
      vXMax = cx + (vXMax - cx) * factor;
      vYMin = cy + (vYMin - cy) * factor;
      vYMax = cy + (vYMax - cy) * factor;
      drawAxes(); drawTicks(); update();
    }, { passive: false });

    drawAxes(); drawTicks(); update();
  })();
  </script>
</div>

As we can see, $g'(z_0) = 2 + 2i = 2z_0$, as we would expect. Alternatively, we can visualize the average rate of change between $z_0$ and $z$ for all possible choices of $z$ at once. Below is a plot of the difference function induced by the choice of $z_0$. (Heatmaps are often used to visualize complex-valued functions, with hue denoting magnitude and brightness denoting modulus).

![Difference quotient heatmap](assets/diff-quotient-heatmap.png)

Crucially, in sufficiently small circles enclosing $z_0$, the average rate of change between $z_0$ and $z$ is approximately constant. This is what allows the limit $$\lim_{z \rightarrow z_0}\frac{f(z) - f(z_0)}{z - z_0}$$ to exist in the first place. That constraint will prove important later. 