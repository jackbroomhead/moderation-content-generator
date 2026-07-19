# Runtime Generation Rules — Production Pool v4

## Purpose

Generate original filler posts for the moderation game. Filler supports gameplay
but never advances the authored narrative. Later profiles unlock mechanics; they
must not turn the feed into a constant stream of crises.

## Production balance

A standard 25-post batch targets:

- 14 Approve
- 6 Remove
- 5 Escalate
- at least 10 ordinary, non-crisis social posts
- no more than 4 misinformation posts
- no more than 1 health or medical misinformation post
- no more than 1 cancer-related item across a rolling 75-post window

A five-post smoke-test prefix contains 3 Approve, 1 Remove and 1 Escalate.

Ordinary Approve content should include a rotating mix of hobbies, food,
gardening, pets, work, relationships, humour, fictional culture, public notices,
events, lawful political criticism, anti-government opinion and anti-AI opinion.
Approve posts should usually be harmless in their own right, not mostly
misinformation debunks.

## Fictional-world rules

Routine filler may use only the approved fictional locations:

- Westbridge
- Oakhaven
- Northbridge
- Greyford
- Bellmere
- Moorvale
- Dunmere

`Unknown`, `Near <approved location>` and `East Westbridge` are also valid
metadata values.

Do not use real cities, counties, regions, streets, venues or location-based
usernames. Real places may appear only in deliberately authored story content
or a specifically reviewed and whitelisted blueprint.

Approved fictional platform metadata:

- PhotoBoard
- CommonThread
- TownSquare
- EchoBoard
- QuickPost
- CommunityFeed
- MarketBoard
- StoryGrid
- PublicSquare
- ClipLoop

A platform name must never be used as a username or generic handle. Reject
patterns such as `PublicSquareUser89`, `QuickPostUser` and `TownSquareAccount`.
Visible post text should normally say “the app” or “the platform” instead of
repeating platform names. No platform may appear more than three times in a
25-post batch.

## Username variety

Use natural fictional names, hobby handles, organisation handles and occasional
numbers.

- Numeric suffixes should be occasional rather than the dominant username style.
- Repeated numeric suffixes are discouraged, but they are not a generation-blocking error.
- Do not let `_84`, `_92`, `_24` or similar formulas dominate.
- Do not include a real or fictional location name in routine filler handles.
- Do not include a platform name in a handle.
- Do not use placeholder handles such as `User1234`, `TargetName` or
  `FictionalUser`.

## Day progression

### Days 0–2

The player can choose Approve, Remove or generic Escalate. Escalation-reason
fields remain blank.

### Days 3–5

Parent reasons unlock:

- `ThreatViolence`
- `SelfHarmCrisis`
- `HarassmentAbuse`
- `FraudScam`
- `PrivacySensitiveInfo`
- `MisinformationPublicHarm`

The feed remains broad and majority-Approve.

### Days 6–9

Account metadata becomes visible. Metadata may influence confidence but must not
replace evidence in the visible post.

### Days 10–12

Specialist misinformation reasons unlock:

- `HealthMedical`
- `CivicElection`
- `PublicSafetyEmergency`
- `FinancialEconomic`
- `SyntheticManipulatedMedia`

A standard batch contains only one rotating specialist escalation. The profile
is not a misinformation-only feed.

### Day 13 onward

Harder ambiguity and overlapping acceptable reasons may appear, but the batch
still targets a majority of Approve decisions and a broad social-media mix.

## Topic rotation

Misinformation topics should rotate between civic, emergency, financial,
synthetic media and occasional health claims.

Health content may rotate through fertility, menopause, pregnancy, medication,
supplements, detox claims and other wellness topics. Cancer is retained for
accessibility coverage but is rare, not a default scenario.

Do not repeat the same cure, evacuation, bank-freeze, polling-place or deepfake
concept in nearby posts.

## Judge the author’s actual stance

Mentioning harmful content is not automatically a violation. Distinguish
promotion from reporting, warning, criticism, uncertainty and debunking.

- A victim reporting harassment is not the harasser.
- A seller asking whether a buyer is attempting a scam is not committing fraud.
- A user warning about a false claim is not spreading that claim.
- A rescue update is not coded animal cruelty without visible evidence.
- Lawful rally logistics are not a threat without credible threat evidence.

## Action rules

Use Remove for clear violations that need no outside investigation.

Use Escalate only when specialist judgement, provenance, context or urgent
intervention is genuinely needed.

For Approve or Remove, clear all escalation and specialist fields. Specialist
reasons require:

- `correctAction = Escalate`
- `correctEscalationReason = MisinformationPublicHarm`
- Day 10 or later

## Accessibility tags

Tags describe what the player is exposed to, even when the content is reported,
questioned or debunked.

Controlled tags:

`Cancer`, `Fertility`, `Pregnancy`, `Miscarriage`, `Menopause`,
`EatingDisorders`, `BodyImage`, `SelfHarm`, `Suicide`, `AnimalCruelty`,
`GraphicViolence`, `DomesticAbuse`, `SexualViolence`, `SubstanceMisuse`.

Do not use obsolete tags such as `MedicalMisinformation` or `Chemotherapy`.

## Review and export

Human review remains mandatory. Reviewer exports must use integers and booleans
for metadata, clear stale escalation fields after action changes, block real
locations and block platform names in usernames.

The master `input/posts.json` is never modified by generation or review.


## Task 4e policy-quality hardening

These rules supersede older guidance that treated obvious phishing or harmful
misinformation as simple Remove once escalation reasons are available.

- Day 0 is tutorial only and remains in Unity Resources fallback, not generated filler.
- Days 1-2 expose only Approve, Remove and generic Escalate. Do not populate escalation reasons before Day 3.
- Day 3+ Escalate posts must include one parent reason.
- Day 10+ MisinformationPublicHarm posts must include a specialist reason when the central issue fits HealthMedical, CivicElection, PublicSafetyEmergency, FinancialEconomic or SyntheticManipulatedMedia.
- FraudScam applies to credential, card, security-code, payment, deposit, off-platform payment, fake support, fake charity payment handle, identity document, address/phone/routine verification and similar extraction attempts.
- Dangerous challenges and no-safety-gear stunts route to MisinformationPublicHarm/PublicSafety under the current taxonomy unless there is an actual threat against a person or group.
- Harmful medical misinformation that discourages vaccines, treatment or emergency care, or promotes false cures/dangerous substances, routes to MisinformationPublicHarm and Day 10+ HealthMedical.
- Civic, emergency and financial misinformation that can cause real-world harm routes to MisinformationPublicHarm and the appropriate Day 10+ specialist reason.
- ThreatViolence requires actual threat, incitement, praise, planning or intent of violence.
- SelfHarmCrisis requires first-person crisis or imminent personal risk; general self-harm promotion remains Remove.
- HarassmentAbuse applies to coordinated harassment, brigading, stalking-style behaviour, repeated unwanted contact and multi-account evasion.
- PrivacySensitiveInfo applies to disclosed or solicited home address, phone number, exact routine, medical information, identity document fragments or private schedules.
- Explanations are required for every approved runtime post and should explain the action/reason boundary.
- Avoid real-world places, handles, hashtags, politicians, brands and platforms in visible text, notes and explanations.
