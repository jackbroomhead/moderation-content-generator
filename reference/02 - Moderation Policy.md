# Moderation Policy — Approved v1

## Core actions

### Approve

Approve when the content is permitted and does not create a credible policy or safety concern.

Examples include:

- ordinary personal or community posts;
- criticism and strong opinions;
- mutual playful banter and mild teasing;
- recognisable satire or parody;
- non-credible hyperbole;
- low-risk inaccuracies with no meaningful likely harm;
- unpleasant speech that does not cross a policy threshold.

### Remove

Remove when there is a clear policy violation and enough evidence to act without specialist, emergency or account-level review.

Examples include:

- obvious scams, phishing and credential theft;
- one-off targeted insults or bullying;
- ordinary spam;
- direct hateful abuse or slurs;
- prohibited consensual adult explicit content;
- clear encouragement or celebration of violence without a credible immediate threat;
- glorification or promotion of self-harm or dangerous eating-disorder behaviour where the poster is not personally in an apparent crisis;
- clearly harmful false advice where specialist verification is not needed.

### Escalate

Escalate where the post involves serious real-world risk, crisis intervention, sensitive information, sustained behaviour, substantial public harm or uncertainty requiring specialist investigation.

Examples include:

- credible threats, planned attacks or immediate danger;
- a person who appears to be in a self-harm or medical crisis;
- exposed sensitive personal information;
- sustained harassment, stalking or coordinated brigading;
- plausible or complicated fraud requiring investigation;
- unverified or coordinated claims with substantial public-harm potential;
- graphic violence or gore during the current early/main moderation design;
- non-consensual intimate imagery, nudify targeting, sextortion or similar serious abuse.

## Unsure versus Needs Review

### Unsure

`Unsure` is a future gameplay deferral, not a moderation outcome and not part of the JSON schema.

- awards no pay or completed score;
- returns the post to the queue later;
- does not alter the post's real answer;
- should have a limit so players cannot defer indefinitely.

### Needs Review

`Needs Review` is an escalation-reason UI choice.

- appears only after the player chooses Escalate;
- is accepted only when `allowNeedsReviewEscalation` is `true`;
- completes the post rather than returning it to the queue;
- should award less than identifying the specific parent reason;
- must never replace the post's specific `correctEscalationReason` in JSON.

Do not accept Needs Review for clear emergencies such as explicit planned violence, clear exposed private data or an obvious self-harm crisis.

## Fraud and scams

- Obvious phishing, fake giveaways, credential theft and straightforward scams: **Remove**.
- Plausible, complicated or high-risk suspected fraud that needs investigation: **Escalate / FraudScam**.

## Privacy and sensitive information

Sensitive personal information is escalated even when shared with good intentions.

Examples:

- home addresses or live private locations;
- medical records or health information;
- driving licences, passports and identity documents;
- bank details or private financial information;
- leaked private account data;
- non-consensual intimate information.

Default answer: **Escalate / PrivacySensitiveInfo**.

## Harassment, abuse and stalking

- Mutual banter or one-off mild teasing: **Approve**.
- Direct targeted insults or bullying: **Remove**.
- Repeated, sustained or escalating targeting: **Escalate / HarassmentAbuse**.
- Coordinated brigading or multiple related accounts: **Escalate / HarassmentAbuse**.
- Repeated unwanted monitoring, contact or following: **Escalate / HarassmentAbuse**.

Use a stronger parent reason when present:

- stalking that exposes private location or routines: `PrivacySensitiveInfo` may be primary;
- stalking with a credible confrontation or harm threat: `ThreatViolence` is primary.

## Misinformation, disinformation and mal-information

Definitions used by the game:

- **Misinformation:** false or inaccurate information shared without an intention to cause harm.
- **Disinformation:** false or manipulated information deliberately created or distributed to deceive, cause harm or secure political, personal or financial gain.
- **Mal-information:** true information deliberately shared to cause harm.

Actions:

- opinion, recognisable satire, parody and harmless low-stakes myths: **Approve**;
- clearly harmful false information where the violation is obvious: **Remove**;
- unverified, complex, coordinated or potentially high-impact civic, medical, financial or public-safety claims: **Escalate / MisinformationPublicHarm**.

Mal-information is routed according to the actual harm: privacy, harassment or threat may take priority.

## Self-harm and personal crisis

- Content glorifying, encouraging or promoting self-harm, dangerous fasting or eating-disorder behaviour: **Remove**.
- Content suggesting the poster may personally be in crisis, medically endangered or at risk of harming themselves: **Escalate / SelfHarmCrisis**.
- When both promotion and personal danger are present, personal safety takes priority: **Escalate / SelfHarmCrisis**.

## Threats, violence and graphic violence

- Obvious jokes, metaphors or non-credible frustration: **Approve**.
- General celebration, encouragement or glorification of violence without a credible immediate target: **Remove**.
- Credible threats, planned attacks, identifiable targets, specific time/location or immediate danger: **Escalate / ThreatViolence**.
- Graphic violence or graphic gore: **Escalate / ThreatViolence** under the current schema and parent menu.

A later specialist workflow may require both removing public visibility and escalating the incident. Until implemented, JSON remains `Escalate / ThreatViolence` with suitable tags.

## Hate and extremism

Early/main game routing uses the existing parent categories:

- discussion, reporting or criticism of controversial beliefs: **Approve**;
- direct slurs, hateful abuse or dehumanising content: **Remove**;
- targeted or coordinated hate campaigns: **Escalate / HarassmentAbuse**;
- violent extremist threats, recruitment tied to violence or incitement: **Escalate / ThreatViolence**;
- coordinated false propaganda with substantial public harm: **Escalate / MisinformationPublicHarm**;
- ambiguous coded signals may allow Needs Review when the context genuinely does not support a confident parent reason.

Later specialist branches may distinguish Hate Abuse from Extremism / Terror, but those are not current top-level JSON reasons.

## Sexual content and non-consensual imagery

- Consensual adult explicit content prohibited by platform policy: **Remove**.
- Non-consensual intimate imagery, sexual blackmail, sextortion and targeted nudify abuse: **Escalate**.

Choose the dominant existing parent reason:

- exposure of intimate/private material: `PrivacySensitiveInfo`;
- sustained targeting or coercive abuse: `HarassmentAbuse`;
- financial sextortion or scam mechanics: `FraudScam`;
- a credible threat of physical harm: `ThreatViolence`.

Synthetic involvement should be captured in tags and later specialist branching, not by inventing a new current parent reason.

## Spam and platform manipulation

- ordinary spam, repeated irrelevant promotion and basic bot posting: **Remove**.
- coordinated manipulation is routed by purpose:
  - false influence campaign: `MisinformationPublicHarm`;
  - brigading: `HarassmentAbuse`;
  - fraud network: `FraudScam`;
  - credible violent network activity: `ThreatViolence`.

A later Platform Manipulation branch may be introduced after metadata and coordination mechanics unlock.

## Synthetic media

Synthetic media describes how content was created or altered; its parent reason depends on the harm.

- harmless, clearly disclosed AI art or parody: **Approve**;
- deceptive low-level manipulation with a clear ordinary violation: **Remove**;
- manipulated media capable of causing substantial public harm: **Escalate / MisinformationPublicHarm**;
- fake endorsements used for uncertain fraud: **Escalate / FraudScam**;
- non-consensual synthetic intimate imagery: usually `PrivacySensitiveInfo` or `HarassmentAbuse`.

Early cases are treated under Misinformation / Public Harm. Later days may branch to a specialist Synthetic Media option. The player must receive contextual evidence; they must never be expected to identify a deepfake from visual imperfections alone.

## Excluded content

Never create child sexualisation, grooming, exploitation or abuse scenarios. This material is outside the intended tone and scope of the Steam game.

## Escalation priority

When more than one reason is plausible, select the parent reason representing the most immediate or serious dominant harm:

1. immediate physical danger or credible threat → `ThreatViolence`
2. personal self-harm crisis → `SelfHarmCrisis`
3. exposed sensitive/private information → `PrivacySensitiveInfo`
4. sustained harassment, stalking or coercive abuse → `HarassmentAbuse`
5. coordinated or high-impact falsehood/public harm → `MisinformationPublicHarm`
6. uncertain or complicated fraud → `FraudScam`

Other defensible parent reasons may be listed in `acceptableEscalationReasons`.


## Task 4e label hardening update

The current generated filler pool treats some high-risk classes as escalation
once reasons are available:

- Simple spam remains Remove, but credential, payment, security-code, deposit,
  off-platform payment, fake support, fake charity payment, identity document or
  sensitive verification extraction is Escalate / FraudScam from Day 3 onward.
- Dangerous challenge and physical-safety content is not ThreatViolence unless
  a person or group is threatening violence. Use Escalate /
  MisinformationPublicHarm, and Day 10+ PublicSafetyEmergency when applicable.
- Harmful medical misinformation that discourages care or promotes false cures
  is Escalate / MisinformationPublicHarm, with Day 10+ HealthMedical when available.
- Civic, public-safety and financial misinformation with real-world harm
  potential is Escalate / MisinformationPublicHarm, with Day 10+ specialist
  routing where applicable.
- ThreatViolence requires actual threat, incitement, praise, planning or intent
  of violence; public-safety rumours and civic frustration are not enough.
