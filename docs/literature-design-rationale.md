# Literature-Grounded Design Rationale

This document records how prior research informs prototype features. “Inspired by” does not mean that a feature is already validated in this interface. Each feature remains a hypothesis to test.

## Design Matrix

| Prototype feature | Research connection | Design implication | Evaluation question |
| --- | --- | --- | --- |
| Audience-initiated context requests | Crowdsourced tiplines and community fact-checking show that audiences can help identify content needing review or context. | Let audiences initiate a structured request rather than waiting for platform detection. | Who requests context, for which claims, and with what false-positive burden? |
| Public threshold before status display | Community systems need aggregation and selection mechanisms; individual reports alone are noisy and can be partisan. | Keep isolated requests private and expose status only after independent participation. | Does the threshold reduce misuse without making the mechanism too slow? |
| Creator response and source attachments | Birdwatch notes linked to sources were rated as more helpful in early empirical work. | Make sources, documents, evidence notes, and response type visible as separate objects. | Do sources improve calibration, and does source quality matter more than source count? |
| Context timeline | Research on Community Notes warns that contextual interventions may arrive after viral engagement has already occurred. | Show when requests, notification, response, and public updates happen. | Do users understand timing, and does the timeline prevent assumptions that silence is a verdict? |
| Request-reason analytics | Studies of crowdsourced fact-checking distinguish missing context, factual errors, and unverified claims. | Capture why users requested context instead of reducing participation to one generic flag. | Which request types produce useful creator responses? |
| Control vs experimental judgment task | Accuracy-prompt research evaluates sharing discernment rather than only belief reduction. | Measure credibility, confidence, and sharing in a normal feed and accountability feed. | Does the interface improve discrimination rather than merely increasing skepticism? |
| Adaptive accountability levels | Accuracy prompts can affect news sharing without changing engagement with social posts, while additional visual styling can create unintended engagement effects. | Avoid accountability controls on personal posts and increase intervention strength only for higher-impact claims. | Does adaptation reduce cognitive load and spillover onto casual content? |
| Sensitive allegation safeguards | Research on abusive-content moderation highlights the importance and difficulty of interpreting intent. | Add enhanced warnings and human review for personal/legal allegations without declaring them false. | Can the system limit amplification and harassment while preserving avenues for legitimate clarification? |
| Behavioral accountability history | The prototype’s contribution is responsiveness and evidence behavior, not a global trust score. | Display resolved requests, response consistency, sources, and evidence counts. | Do users overgeneralize behavioral history into source credibility or truth judgments? |

## Key Sources

1. Pröllochs, N. (2021). *Community-Based Fact-Checking on Twitter's Birdwatch Platform.* The analysis reports that source-linked notes and more positive language were associated with higher helpfulness ratings, while polarization and opinion/speculation remained challenges. https://arxiv.org/abs/2104.07175

2. Wojcik, S., Hilgard, S., Judd, N., et al. (2022). *Birdwatch: Crowd Wisdom and Bridging Algorithms can Inform Understanding and Reduce the Spread of Misinformation.* A survey experiment and platform deployment examined annotations selected to bridge heterogeneous groups. https://arxiv.org/abs/2210.15723

3. Chuai, Y., Tian, H., Pröllochs, N., & Lenzini, G. (2023). *Did the Roll-Out of Community Notes Reduce Engagement With Misinformation on X/Twitter?* The field analysis found no significant reduction associated with rollout and identified intervention delay as a likely limitation. https://arxiv.org/abs/2307.07960

4. Saeed, M., Traub, N., Nicolas, M., Demartini, G., & Papotti, P. (2022). *Crowdsourced Fact-Checking at Twitter: How Does the Crowd Compare With Experts?* The study finds that crowd approaches can scale but do not produce consistent actionable results in every setting. https://arxiv.org/abs/2208.09214

5. Kazemi, A., Garimella, K., Shahi, G. K., Gaffney, D., & Hale, S. A. (2022). *Tiplines to uncover misinformation on encrypted platforms.* Audience submissions were useful for discovering widely circulated content, including content submitted before it appeared in large public groups. https://misinforeview.hks.harvard.edu/article/research-note-tiplines-to-uncover-misinformation-on-encrypted-platforms-a-case-study-of-the-2019-indian-general-election-on-whatsapp/

6. Bhardwaj, V., et al. (2023). *Examining accuracy-prompt efficacy in combination with using colored borders to differentiate news and social content online.* Accuracy prompts improved sharing quality, while added visual borders also produced unintended engagement shifts. https://misinforeview.hks.harvard.edu/article/examining-accuracy-prompt-efficacy-in-combination-with-using-colored-borders-to-differentiate-news-and-social-content-online/

7. Camargo, C. Q., et al. (2023). *What do we study when we study misinformation? A scoping review of experimental research (2016–2022).* The review identifies heavy reliance on belief outcomes and limited direct study of behavior change, motivating sharing and interaction measures here. https://misinforeview.hks.harvard.edu/article/what-do-we-study-when-we-study-misinformation-a-scoping-review-of-experimental-research-2016-2022/

## Claims to Avoid

- “Community Notes proves this design works.”
- “More sources mean a claim is more credible.”
- “High response consistency means a creator is trustworthy.”
- “A context request indicates that a claim is false.”
- “The adaptive classifier can identify misinformation.”

The publishable claim depends on the planned experiment: whether this particular interface improves judgment calibration and sharing discernment while maintaining acceptable fairness, cognitive load, and creator burden.
