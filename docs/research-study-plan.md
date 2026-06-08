# Research Study Plan

## Working Title

**From Fact-Checking to Participatory Accountability: Evaluating Adaptive Context Requests in Social Media Feeds**

## Contribution

This work investigates whether a lightweight, participatory accountability mechanism helps audiences make better-calibrated credibility judgments without imposing excessive cognitive load or creator burden.

The interface does not determine whether a claim is true or false. Instead, it lets audiences request context and makes creator responsiveness, evidence sharing, and unresolved requests visible after a social threshold is reached.

The intended HCI contribution is:

1. A design model for accountability that remains unobtrusive until context is socially requested.
2. Empirical evidence about how visible accountability behavior affects credibility judgments and sharing decisions.
3. Evidence about the trade-off between audience benefit, perceived fairness, and creator burden.

## Research Questions

**RQ1.** Does adaptive accountability improve the calibration of credibility judgments compared with a conventional social media feed?

**RQ2.** Does adaptive accountability reduce willingness to share unsupported claims while preserving willingness to share well-supported claims?

**RQ3.** How does the interface affect perceived fairness, cognitive load, trust judgment, and willingness to use?

**RQ4.** Which accountability signals influence judgment most: community requests, creator response, source submission, or unresolved status?

**RQ5.** How do creators experience context requests in terms of burden, legitimacy, pressure, and opportunity to clarify?

## Key Construct

“Better credibility judgment” should not mean lower credibility ratings overall. It should mean:

- Better discrimination between well-supported and unsupported claims
- Better calibration between confidence and correctness
- Greater sensitivity to source quality and creator response
- More appropriate sharing decisions
- Less reliance on superficial engagement cues

The prototype itself remains non-verdict-based. Ground truth is used only by researchers when selecting and coding experimental stimuli.

## Community Notes Dataset Role

The prototype includes aggregate metrics from a Community Notes public-data snapshot covering 2021-01-23 through 2026-06-05. The data is used to motivate and contextualize design questions, not to provide ground-truth labels for study stimuli.

The current snapshot contains:

- 2,763,904 authored notes
- 2,952,168 status-history records
- 517,036 note-request eligibility signal records
- 2,575,922 status records still marked as needing more ratings
- A 6.5-hour median to first non-pending status among records with a recorded transition
- 29,006,350 note ratings from the supplied ratings export
- 1,443,786 contributor enrollment records

These descriptive results motivate evaluation of:

- Whether users understand unresolved status
- Whether context arrives early enough to affect judgment and sharing
- Whether source and evidence attachments improve response usefulness
- Whether adaptive thresholds reduce noise without creating excessive delay
- Whether clarity, relevant sources, claim-specific responses, and important context predict perceived usefulness in this prototype
- Whether participants understand contributor eligibility as a process state rather than a reputation signal

Authored note reason flags can overlap, and status helpfulness does not determine whether the underlying post is true. Confirmatory study stimuli therefore require separate researcher verification.

## Study 1: Audience Experiment

### Design

A preregistered, randomized between-subjects online experiment:

| Condition | Interface |
| --- | --- |
| Control | Conventional social feed without accountability controls |
| Request-only | Feed with `Request Context`, but no public accountability history |
| Adaptive accountability | Full prototype with threshold status, timeline, creator responses, evidence, and history |

The request-only condition helps isolate the effect of initiating participation from the effect of seeing accumulated accountability behavior.

### Participants

- Adults who use social media at least weekly
- Recruit a demographically varied sample
- Exclude participants who fail preregistered attention or comprehension checks
- Determine the confirmatory sample with an a priori power analysis
- Use a small pilot only to estimate variance, completion time, and manipulation strength

A reasonable pilot target is 20-30 participants. The final sample size should be justified by the smallest effect of interest rather than chosen from a generic convention.

### Stimuli

Create a balanced feed containing:

- Personal and casual posts
- Clearly framed opinions
- Supported public claims
- Unsupported or weakly supported claims
- Rumors with different confirmation states
- Health, political, finance, entertainment, and AI claims

For claims included in accuracy analyses, establish the evidential status before data collection using traceable public records or expert-reviewed source packets. Avoid active breaking news whose status could change during the study.

Counterbalance:

- Claim topic
- Claim evidential status
- Creator identity
- Engagement counts
- Post order
- Presence and quality of creator response

Use fictional creators and neutral visual styling to reduce prior-attitude and celebrity effects.

### Task

Participants browse a feed under one assigned condition. For selected claim posts, they:

1. Rate perceived credibility.
2. Indicate confidence in that judgment.
3. Decide whether they would share, save, ignore, or seek more information.
4. Optionally inspect or request context where the interface permits it.
5. Answer brief post-task questions about fairness, effort, and usefulness.

Avoid requiring participants to open context. Voluntary interaction is an important behavioral outcome.

### Primary Outcomes

**Credibility discrimination**

Difference in credibility ratings between well-supported and unsupported claims.

**Calibration**

Association between participant confidence and judgment correctness. Analyze calibration error or a preregistered probabilistic scoring measure where appropriate.

**Sharing discernment**

Difference in sharing intention between well-supported and unsupported claims.

The desired effect is increased discernment, not a blanket reduction in sharing.

### Secondary Outcomes

- Perceived credibility
- Trust judgment
- Context-opening rate
- Context-request rate
- Decision time
- Source-link opening rate
- Perceived fairness
- Cognitive load
- Interface comprehension
- Willingness to use
- Perceived social pressure
- Recall of accountability status

### Example Hypotheses

**H1.** Participants in the adaptive-accountability condition will show greater credibility discrimination than participants in the control condition.

**H2.** Participants in the adaptive-accountability condition will show greater sharing discernment than participants in the control condition.

**H3.** High-quality creator responses with relevant evidence will increase credibility ratings more than responses without evidence.

**H4.** Unresolved context requests will increase information-seeking and reduce sharing intention for unsupported claims, without equivalent effects on personal posts.

**H5.** Adaptive accountability will increase perceived fairness relative to direct warning-label designs, while producing a modest increase in cognitive load relative to the control.

H5 requires a warning-label comparison condition or a separate follow-up study if it is retained.

### Manipulation Checks

Participants should be able to identify:

- What `Request Context` does
- Whether a threshold was reached
- Whether the creator was invited to respond
- Whether a response or source was provided
- That the interface did not declare the claim true or false

### Analysis Plan

Use mixed-effects models because each participant evaluates multiple posts.

Suggested models:

- Credibility rating: linear mixed-effects model
- Share choice: logistic mixed-effects model
- Context opening: logistic mixed-effects model
- Decision time: log-transformed mixed-effects model or robust alternative

Include random intercepts for participant and post. Consider random slopes for evidential status where supported by the data.

Core fixed effects:

- Experimental condition
- Evidential status
- Condition × evidential status
- Response quality
- Claim category

Report:

- Effect sizes and confidence intervals
- Model assumptions and exclusions
- Confirmatory and exploratory analyses separately
- Null results without reframing them as proof of equivalence

Preregister the primary outcome, exclusion criteria, transformations, contrasts, and stopping rule.

## Study 2: Creator Experience

### Design

A mixed-methods scenario study or moderated usability study with people who post publicly online.

Participants receive simulated context requests for several post types and use the creator dashboard to respond, decline, or provide evidence.

### Measures

- Perceived legitimacy of requests
- Perceived fairness
- Response burden
- Emotional pressure
- Willingness to respond
- Appropriateness of the threshold
- Comfort sharing evidence
- Perceived risk of harassment or coordinated misuse
- Value of request summaries
- Preference for response labels

### Qualitative Questions

- When does a context request feel constructive?
- When does it feel accusatory or coercive?
- What information helps a creator decide whether to respond?
- Should creators be able to explain why they are not responding?
- What protections are needed for personal, legal, or safety-sensitive claims?
- How should coordinated request campaigns be handled?

Use thematic analysis with a documented coding process and report disagreements or reflexive decisions transparently.

## Instrumentation Needed

Before data collection, add consent-aware event logging for:

- Condition assignment
- Post impression and dwell time
- Context-button impression
- Context request opened, submitted, or abandoned
- Context drawer opened
- Timeline viewed
- Source link opened
- Creator response viewed
- Credibility and confidence ratings
- Sharing decision
- Moderator or misuse-report interaction

Do not log free-text responses without explicit consent and a retention policy. Use pseudonymous study IDs rather than platform identities.

## Recommended Scales

Use validated scales where they fit, but keep the survey short enough to avoid fatigue. Candidate constructs include:

- Single-item or multi-item credibility judgments
- Confidence ratings
- Sharing intention
- NASA-TLX subset or another justified cognitive-load measure
- Procedural fairness
- Perceived autonomy
- System usability
- Intention to use

Any adapted scale should be documented, piloted, and evaluated for reliability in the study sample.

## Ethics and Risk Controls

- Obtain institutional ethics or IRB review before recruitment
- Clearly disclose that all posts and identities are simulated
- Avoid distressing health or political stimuli unless necessary and justified
- Debrief participants about the study purpose and experimental content
- Do not expose participants to active misinformation without correction during debriefing
- Provide withdrawal and data-deletion procedures
- Minimize collection of political affiliation and other sensitive attributes
- Predefine protections against coordinated context-request misuse

## Validity Threats

- Participants may behave differently in a study than on a real platform
- Fictional posts may reduce emotional and identity investment
- Repeated credibility questions may increase scrutiny across all conditions
- Threshold visibility may be confused with majority opinion
- Creator responsiveness may be interpreted as credibility despite the disclaimer
- Topic familiarity and political identity may dominate interface effects
- A single threshold may not generalize across claim types or communities

Mitigations include counterbalancing, comprehension checks, measuring topic familiarity, separating behavioral and self-report outcomes, and testing multiple threshold explanations.

## Success Criteria

Evidence for the design should require more than higher usability ratings. A persuasive result would show:

1. Better credibility and sharing discrimination in the adaptive condition.
2. No evidence that participants interpret request counts as truth votes.
3. Acceptable cognitive-load costs.
4. Creator perceptions of reasonable fairness and manageable burden.
5. Qualitative evidence that the mechanism supports clarification rather than punishment.

## Publication Path

Potential paper structure:

1. Problem: fact-checking and warning labels often impose verdicts after content is published.
2. Design space: accountability as a participatory, thresholded process.
3. Prototype: adaptive context requests and behavioral history.
4. Study 1: audience judgment and sharing experiment.
5. Study 2: creator burden and fairness.
6. Findings: benefits, trade-offs, and misuse risks.
7. Design implications for non-verdict social media interventions.

The strongest claim should remain bounded: the interface may improve judgment calibration and information-seeking under studied conditions. It should not be presented as a system that determines credibility or prevents misinformation.
