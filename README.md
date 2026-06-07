# Adaptive Accountability Interface for Social Media Claims

A full-stack research prototype exploring how social platforms can make requests for context, creator responses, evidence submission, and accountability history visible without deciding whether a claim is true or false.

The interface is dark, mobile-first, and presented in a centered phone-like frame on desktop. All identities, claims, interactions, and source links are mock data.

## Features

- Realistic social feed with personal posts, opinions, public claims, rumors, and high-impact claims
- Adaptive `Request context` control shown only for eligible claim categories
- Five-request public visibility threshold and per-user duplicate prevention
- Creator response center with source, evidence, and descriptive response labels
- Public context drawer with community request summary and explicit non-verdict disclaimer
- Behavior-based accountability history without truth, trust, or credibility scores
- Misuse reporting and a moderator/research observer queue
- Non-functional AI classification suggestion panel with prohibited verdict labels
- Browser `localStorage` persistence plus a mock Express API
- PostgreSQL schema for a future persistent implementation

## Project Structure

```text
.
├── src/
│   ├── App.vue
│   ├── components/
│   │   ├── AccountabilityHistory.vue
│   │   ├── AboutResearch.vue
│   │   ├── ContextDrawer.vue
│   │   ├── CreatorDashboard.vue
│   │   ├── ModeratorQueue.vue
│   │   ├── PostCard.vue
│   │   └── RequestContextModal.vue
│   ├── data/mockPosts.js
│   ├── services/storage.js
│   ├── main.js
│   └── style.css
├── server/
│   ├── index.js
│   └── mock-data.json
├── database/schema.sql
└── README.md
```

## Setup

Requires Node.js 18 or newer.

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Run the mock backend in another terminal:

```bash
npm run server
```

Or run both:

```bash
npm run dev:all
```

The frontend is available at `http://localhost:5173`; the API runs at `http://localhost:3001`. The current UI deliberately uses `localStorage` so the study flow works without the backend. Vite proxies `/api` to the Express server for future integration.

Build for production:

```bash
npm run build
```

## Research Purpose

**Research question:** How can adaptive accountability mechanisms help audiences assess social media credibility while minimizing disruption to normal user behavior?

Suggested evaluation measures include perceived credibility, trust judgment, sharing intention, perceived fairness, cognitive load, creator burden, and willingness to use.

The central design principle is that accountability remains invisible by default and becomes visible only when socially necessary. Personal and casual posts receive no accountability controls. Eligible claim types can receive private context requests; status becomes public only after the configured threshold.

## API Summary

- `GET /api/health`
- `GET /api/posts`
- `POST /api/posts/:postId/requests`
- `POST /api/posts/:postId/response`
- `POST /api/posts/:postId/reports`
- `PATCH /api/posts/:postId/review`

The API writes demo state to the ignored `server/data.json` file.

## Limitations

- No real authentication or authorization
- Fixed demo user and simulated roles
- Rule-based eligibility stored in mock data
- No functional AI classification
- No source validation or fact-checking
- No production moderation, privacy, rate limiting, or accessibility audit
- Accountability metrics are illustrative and not suitable for ranking people

## Future Work

- Connect the Vue state layer to the Express API and PostgreSQL
- Add consent-aware research event instrumentation
- Test alternative thresholds and private notification strategies
- Add authenticated role permissions and rate limiting
- Conduct accessibility, usability, and creator-burden studies
- Explore transparent, appealable classification assistance without truth verdicts
