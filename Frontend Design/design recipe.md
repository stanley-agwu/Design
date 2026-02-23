# Design Recipe

### 1. Critical Rendering Path (CRP)

The sequence the browser follows to turn HTML/CSS/JS into pixels on screen:
HTML → DOM, CSS → CSSOM, DOM + CSSOM → Render Tree, Layout, Paint/Composite.

Why it matters: render-blocking CSS/JS delays first paint.

#### Example (render-blocking vs deferred JS)

```html
<!-- BAD: blocks parsing + rendering until downloaded & executed -->
<script src="/app.js"></script>

<!-- BETTER: doesn't block HTML parsing; runs after parse -->
<script defer src="/app.js"></script>

<!-- For analytics/non-critical scripts -->
<script async src="https://example.com/analytics.js"></script>
```

### 2. Core Web Vitals
Google’s key UX performance metrics (most common set):

1. LCP (Largest Contentful Paint): how fast the main content appears
2. INP (Interaction to Next Paint): responsiveness to user input
3. CLS (Cumulative Layout Shift): visual stability (no jumping)

#### Example: prevent CLS caused by images

```html
<!-- Reserve space to avoid layout shift -->
<img src="/hero.jpg" width="1200" height="600" alt="Hero" />
```

#### Example: reduce INP by avoiding long tasks

```ts
// Break up heavy work so the main thread can respond
function chunkedWork(items: number[]) {
  let i = 0;
  function runChunk() {
    const end = Math.min(i + 1000, items.length);
    for (; i < end; i++) doSomething(items[i]);
    if (i < items.length) requestAnimationFrame(runChunk);
  }
  requestAnimationFrame(runChunk);
}
```

### 3. HTTP Caching
Using cache headers so browsers/CDNs can reuse responses instead of re-downloading.

Common headers:
1. `Cache-Control: max-age=...`, `public`, `private`, `immutable`
2. `ETag` / `If-None-Match` (revalidation)
3. `Last-Modified` / `If-Modified-Since`

#### Example: cache fingerprinted assets “forever”
1. Bundle filename: `app.8f3a1c.js`
2. Header: `Cache-Control: public, max-age=31536000, immutable`

#### Example: revalidation for HTML
1. Header: `Cache-Control: no-cache`
2. Browser re-checks and may get `304 Not Modified`

### 4. Content Negotiation
Serving different representations of the same resource based on request headers like:

1. `Accept: application/json` vs `text/html`
2. `Accept-Language: en-GB` vs `en-US`
3. `Accept-Encoding: br, gzip`

#### Example: return JSON or HTML from the same endpoint

```ts
import express from "express";
const app = express();

app.get("/profile", (req, res) => {
  if (req.accepts("json")) {
    res.json({ name: "Resources", type: "Json" });
  } else {
    res.type("html").send("<h1>Resources</h1><p>Html</p>");
  }
});
```

### 5. Lazy Loading
Loading resources only when needed (on demand), improving initial load time.

#### Example: lazy-load a route/component (React)
Using Dynamic Import
```ts
import React, { Suspense } from "react";
const AdminPage = React.lazy(() => import("./AdminPage"));

export function App() {
  return (
    <Suspense fallback={<div>Loading…</div>}>
      <AdminPage />
    </Suspense>
  );
}
```

#### Example: lazy-load images

```html
<img src="/gallery/1.jpg" loading="lazy" alt="Gallery item" />
```

