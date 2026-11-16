// Plays the sentences of one request as they arrive. Each one starts on the sample where the one before it
// ends, so there is no gap between them. `context` is an AudioContext; changed() is called whenever `playing`
// may have changed.
function livePlayer(context, changed = () => {}) {
  // A sentence with nothing before it to follow starts this many seconds from now, not at once: the browser then
  // has it in hand before its first sample is due. Asked to start at once, it can start a few milliseconds late
  // (measured in Firefox: up to 21 ms), and the next sentence would begin before it has ended.
  const LEAD = 0.05;
  const sources = new Set();
  let open = false;     // more sentences of this request may still come
  let muted = false;    // the listener stopped this request: its later sentences stay silent
  let refused = false;  // the browser said no when asked to start the sound
  let queued = 0;       // sentences of this request handed to the browser
  let next = 0;         // the context time at which the next sentence starts

  function silence() {
    for (const source of sources) {
      source.onended = null;
      try { source.stop(); } catch (error) { /* an old browser, and the sentence had already ended */ }
    }
    sources.clear();
  }

  return {
    get playing() { return !muted && (open || sources.size > 0); },

    // A new request. Call it from a click or a key press: browsers let a page start sound only there.
    begin() {
      silence();
      open = true; muted = false; refused = false; queued = 0; next = 0;
      if (context.state !== "running") Promise.resolve(context.resume()).catch(() => { refused = true; });
      changed();
    },

    // Queue one sentence. It starts when the one before it ends, or right away when that moment has passed.
    add(samples, rate) {
      if (muted || !samples.length) return;
      const buffer = context.createBuffer(1, samples.length, rate);
      buffer.getChannelData(0).set(samples);
      const source = context.createBufferSource();
      source.buffer = buffer;
      source.connect(context.destination);
      source.onended = () => { sources.delete(source); changed(); };
      const when = Math.max(next, context.currentTime + LEAD);
      source.start(when);
      next = when + samples.length / rate;
      sources.add(source);
      queued += 1;
    },

    // No more sentences will come; the queued ones play to the end. False when there is nothing to hear (no
    // sentence came, or the browser refused the sound): the caller then plays the whole clip itself. A context
    // that is only slow to start is not a refusal: a short text can be done before the sound is running, and
    // its sentences play as soon as it is.
    end() {
      open = false;
      const played = muted || (queued > 0 && !(refused && context.state !== "running"));
      if (!played) silence();
      changed();
      return played;
    },

    stop() {
      muted = true; open = false;
      silence();
      changed();
    },
  };
}
