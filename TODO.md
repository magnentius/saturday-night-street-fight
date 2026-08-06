# Saturday Night Street Fight — Open Issues

Remaining items from the full rules audit of `rules.md` and `gm.md`. Everything the audit
raised that was a straightforward contradiction, dead end, or arithmetic error has been
fixed (see commits `da07798`, `8f736fe`, `d97daa8`). What follows is what is genuinely
left: one design decision, a set of balance concerns, unwritten promises in the flavour
text, and missing GM content.

Items are referenced by section rather than line number, since line numbers drift.

---

## 1. Open design decision

### Critical hits on heavy attacks are almost always lethal
**Where:** `rules.md` §6.2 Success Modifier, §2.2 Attribute Cap

High Impact deals **3**, a Critical Hit adds **+1**, and the Attribute Cap is **4**. So any
critical high-impact hit against an unblocked target drives an attribute straight to 0 —
an automatic TKO — and criticals fire on roughly **1 contested roll in 5**. This affects
High Kick, Uppercut, Body Kick, Hip/Shoulder Throw, Takedown, and Submission Hold.
Karate's *Ikken Hissatsu* pushes it to 5.

Two consequences worth weighing:

- Mitigation is currently the *only* thing making these survivable — a guard that loses its
  clash still absorbs 2, turning a lethal 4 into a survivable 2. That is a decent argument
  the mitigation model is pulling its weight, but it means declining to block is close to
  fatal against any heavy attacker.
- Any future **"on a Critical Hit"** rider attached to a heavy attack will be dead text,
  because the target is knocked out rather than experiencing the rider. This already forced
  an asymmetry in the Stunned trigger (`d97daa8`).

**Possible directions:** lower High Impact to 2 and widen the damage band; make the crit
bonus a secondary effect rather than +1 damage on already-heavy attacks; or raise the
Attribute Cap and retune every damage number against it. All three are substantial.

---

## 2. Balance

### Wrestling's pin loop
**Where:** `rules.md` §3.4 *Ground Control*, §9.2 Pinned

*Ground Control* pins on any won Black-vs-Black. Pinned means no Strike, no Dodge, and
Disadvantage on defence, while the wrestler applies Submission Hold for 3 Stamina a round.
Worse, of the two escape routes only one is real: the Agility Escape is a Block-stance
action, which loses the counter wheel to the wrestler's Throw stance.

### Taunt now interacts badly with the Cool economy
**Where:** `rules.md` §5.1.C Taunt, §9.5 Shaken, §7.3 The Cool Economy

Two landed Taunts leave a starting fighter Shaken, with no in-combat recovery. Since Cool
is now the game's currency, a taunt-heavy opponent can also bankrupt the crew's ability to
bribe, bluff, or get a wounded crewmate admitted to hospital. Taunt costs the user nothing
and nothing damages Cool back.

### Character creation converges on a single build
**Where:** `rules.md` §1.2

50 XP against a pool of 8–10 techniques means every Boxer buys all 8 techniques (24 XP) and
two attributes at 3 (20 XP), banking the rest. The same is true of every other style. There
is no meaningful build choice at Rank 50 — the budget exceeds what a style can absorb.

### Muay Thai's *Heavy Leg Kicks* is a near-empty perk
**Where:** `rules.md` §3.2

Low Kick already inflicts Hobbled by default, so the perk grants only "target cannot Dodge
next round" — worth nothing against Muay Thai, Judo, Wrestling, or Karate, none of which
have Dodge.

### XP income does not reach the top tiers
**Where:** `rules.md` §12, `gm.md` Threat Tier & XP Budget

Keys pay 1–2 XP per encounter. Rank 150 needs 100 XP past creation and Rank 200+ needs 150,
so Tier 4 and Tier 4+ bosses sit 25–75 sessions away and are effectively unreachable
content in most campaigns.

### Street Craps is a risk-free XP faucet
**Where:** `gm.md` Danger Rank 2, entry 3

A repeatable contested Cool check for +1 XP, outside the Key economy and with no downside.

### Muay Thai pays more for the Rank 150 milestone
**Where:** `rules.md` §12.2

Rank 150 requires mastering every Primary Style technique. Muay Thai carries 10 techniques
where every other style carries 8, so it pays roughly 18 XP more for the same milestone.

---

## 3. Flavour that promises mechanics which do not exist

### The speed / tempo layer
**Where:** `rules.md` §5.1, §5.3

Descriptions throughout reference a tempo system that was never implemented: "interrupts
slower actions" (Jab), "highly vulnerable to fast punches" (Uppercut), "easily parried or
caught" (High Kick), "cancels throw/clinch attempts" (Push Kick), and speed grades attached
to most techniques. Push Kick is labelled "low damage" but deals 2 — the same as the
"high damage" Cross.

Either build a tempo mechanic or rewrite the descriptions to match what actually resolves.
The parry riposte and the guard heights (`8f736fe`) were the same class of problem and were
fixed by the latter approach.

### Hook's conditional damage bonus
**Where:** `rules.md` §5.1.A

"Gaining a damage bonus if the opponent also chose a Strike" — the bonus is never
quantified.

---

## 4. Missing GM content

### Police stat block
**Where:** `gm.md` Police Siren Clock, Danger Rank 1 entry 3

Danger Rank 1 entry 3 summons police enforcers on any combat action, and the Siren Clock
delivers officers to every fight that runs long — but there is no stat block, and no rules
for fighting them rather than fleeing or bluffing.

### Guard dog
**Where:** `gm.md` Danger Rank 3, entry 8

An aggressive guard dog enforces a turf line, with no stats and no rules for animals.

### Stance selection for individual NPCs
**Where:** `gm.md` NPC Stats & Threat Tiers

Mobs got a 1d10 stance table. Tier 2 Thugs and Tier 3 Bosses still have none, which matters
because the GM commits their stance secretly and simultaneously against the players — a
blind-commit game needs either a procedure or a table.

### Siren Clock location types contradict the Danger Rank definitions
**Where:** `gm.md` Police Siren Clock

The clock table labels Danger Rank 4 a "Dark Alley / Dive Bar" while §4 defines Rank 4 as an
active turf war zone, and it gives the *safest* blocks the *tightest* 3-round clock — so
most Home Turf fights end in police arrival.

### GM-side XP guidance
**Where:** `gm.md`

XP Keys are entirely player-facing. The GM guide offers no advice on awarding XP, and the
only GM-side source is the Street Craps faucet above.

### Boss lair content and a syndicate generator
**Where:** `gm.md` Subway Traversal, Turf Control

The "Final Station (Boss's Lair)" is referenced by the traversal rules but never generated,
and there is no generator for syndicates or gangs as factions despite turf war being the
campaign's spine. `names.md` covers people, not crews.

### Campaign calendar
**Where:** `rules.md` §10, `gm.md` Police Shakedown

Hospitalisation runs 1–3 weeks and lockup costs days, but there is no time-tracking
framework and no guidance on what the rest of the crew does while a member is out.

---

## 5. Minor

### "Reaction" is overloaded three ways
The **Reaction** attribute, the **Reaction Roll** (NPC disposition, which uses Cool), and
the **Perk Reaction** (immediate style follow-up) are three unrelated things sharing a name.
`gm.md`'s Steam Vent hazard — "any reaction-based action" — is ambiguous between them.

### Tier 2 and Tier 3 morale
Mobs now break and scatter. Individual Thugs and Bosses have no morale rule and never
surrender or flee.
