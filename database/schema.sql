CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE user_role AS ENUM ('audience', 'creator', 'moderator', 'research_observer');
CREATE TYPE claim_classification AS ENUM (
  'personal',
  'opinion',
  'public_claim',
  'high_impact_claim',
  'rumor_news',
  'health_claim',
  'finance_claim',
  'political_claim',
  'ai_claim'
);
CREATE TYPE context_request_type AS ENUM ('source', 'clarification', 'evidence', 'classification');
CREATE TYPE response_label AS ENUM (
  'personal_experience',
  'opinion',
  'rumor_speculation',
  'confirmed_with_source',
  'official_document'
);

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  display_name TEXT NOT NULL,
  handle TEXT NOT NULL UNIQUE,
  role user_role NOT NULL DEFAULT 'audience',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  creator_id UUID NOT NULL REFERENCES users(id),
  body TEXT NOT NULL,
  category TEXT,
  classification claim_classification NOT NULL,
  accountability_enabled BOOLEAN NOT NULL DEFAULT false,
  context_threshold INTEGER NOT NULL DEFAULT 5 CHECK (context_threshold > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE context_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  requester_id UUID NOT NULL REFERENCES users(id),
  request_type context_request_type NOT NULL,
  question TEXT NOT NULL CHECK (char_length(question) BETWEEN 1 AND 500),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (post_id, requester_id)
);

CREATE TABLE creator_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL UNIQUE REFERENCES posts(id) ON DELETE CASCADE,
  creator_id UUID NOT NULL REFERENCES users(id),
  explanation TEXT NOT NULL,
  source_url TEXT,
  evidence_note TEXT,
  label response_label,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE misuse_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  reporter_id UUID REFERENCES users(id),
  note TEXT,
  reviewed_at TIMESTAMPTZ,
  reviewed_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE observer_reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  observer_id UUID NOT NULL REFERENCES users(id),
  note TEXT,
  reviewed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (post_id, observer_id)
);

CREATE INDEX context_requests_post_id_idx ON context_requests(post_id);
CREATE INDEX posts_creator_id_idx ON posts(creator_id);
CREATE INDEX misuse_reports_unreviewed_idx ON misuse_reports(created_at) WHERE reviewed_at IS NULL;

CREATE VIEW public_accountability_status AS
SELECT
  p.id AS post_id,
  COUNT(cr.id)::INTEGER AS request_count,
  COUNT(cr.id) >= p.context_threshold AS threshold_reached,
  cres.id IS NOT NULL AS creator_responded,
  cres.created_at AS responded_at
FROM posts p
LEFT JOIN context_requests cr ON cr.post_id = p.id
LEFT JOIN creator_responses cres ON cres.post_id = p.id
GROUP BY p.id, p.context_threshold, cres.id, cres.created_at;

COMMENT ON VIEW public_accountability_status IS
  'Behavioral accountability only. This view must not be interpreted as a truth, trust, or credibility score.';
