# Escalation Reasons — Approved Parent Menu

The original escalation menu remains the permanent first-level menu.

| Player label | JSON code |
|---|---|
| Threat / Violence | `ThreatViolence` |
| Self-Harm / Crisis | `SelfHarmCrisis` |
| Harassment / Abuse | `HarassmentAbuse` |
| Fraud / Scam | `FraudScam` |
| Privacy / Sensitive Info | `PrivacySensitiveInfo` |
| Misinformation / Public Harm | `MisinformationPublicHarm` |
| Needs Review | controlled by `allowNeedsReviewEscalation` |

## `ThreatViolence`

Use for credible threats, planned attacks, targeted intimidation, immediate physical danger and, under the current simple system, graphic violence or gore requiring specialist handling.

Do not use for obvious metaphor, humour or non-credible frustration.

Possible later branches:

- credible personal threat;
- planned mass harm;
- incitement to violence;
- graphic violence;
- extremist violence.

## `SelfHarmCrisis`

Use when the poster may be personally in crisis, medically endangered or at risk of self-harm or suicide.

Promotion or glorification without personal crisis is removed rather than escalated.

Possible later branches:

- personal crisis;
- imminent danger;
- welfare intervention.

## `HarassmentAbuse`

Use for sustained harassment, stalking, repeated unwanted contact, coordinated brigading, account-level abuse or coercive targeted behaviour.

One-off ordinary targeted insults are removed.

Possible later branches:

- sustained harassment;
- stalking;
- coordinated brigading;
- hate abuse;
- coercive or sexual abuse.

## `FraudScam`

Use for plausible, complicated or high-risk suspected fraud that requires investigation.

Obvious phishing and straightforward scams are removed.

Possible later branches:

- investment fraud;
- credential theft;
- impersonation scam;
- ticket/marketplace fraud;
- suspicious activity requiring investigation.

## `PrivacySensitiveInfo`

Use for home addresses, live private locations, identification documents, medical records, bank information, private account data or non-consensual intimate information.

Possible later branches:

- doxxing or private location;
- medical information;
- identity documents;
- financial information;
- intimate/private information.

## `MisinformationPublicHarm`

Use for unverified, coordinated or complex claims with substantial possible civic, medical, financial or public-safety harm.

Possible later branches:

- public-health misinformation;
- civic or political manipulation;
- financial panic;
- coordinated disinformation;
- synthetic-media manipulation;
- platform influence operation.

## Needs Review

Needs Review is not a `correctEscalationReason` value.

It is accepted only when `allowNeedsReviewEscalation` is `true`. Every Escalate post must still contain one of the six specific JSON codes as its primary reason.

## Later specialist branching

Later difficulty should branch from a parent rather than replacing the first-level menu. Candidate subreasons such as `GraphicViolence`, `SyntheticMediaManipulation`, `HateAbuse`, `ExtremismTerror`, `SexualExploitation` and `PlatformManipulation` are design candidates only. They are not currently valid primary reason codes.


## Task 4e compatibility notes

- FraudScam now includes obvious credential/payment extraction once reasons are visible, not only ambiguous fraud.
- MisinformationPublicHarm includes dangerous challenges and public-safety misinformation under the current parent taxonomy.
- ThreatViolence should not be used for dangerous challenges, emergency rumours or non-violent infrastructure/public-safety claims unless there is actual threat or incitement.
- Day 10+ MisinformationPublicHarm should carry the appropriate specialist reason when the subtype is clear.
