# RPG Combat Rules

## Fighter Creation

To build a fighter, follow these four simple steps:

### 1. Allocate Combat Attributes
Your three core attributes represent your physical and mental defaults:
*   **Footwork**: Agility, movement speed, evasive positioning, and lower-body dexterity.
*   **Posture**: Physical structure, strength, balance, stability, and leverage.
*   **Timing**: Perception, reaction speed, precision, and mental focus.

**Point Buy**:
*   All three attributes start at **1**.
*   You have **5 points** to distribute among them.
*   No attribute can be higher than **4** at character creation.
    *   *Example allocation: Footwork 3, Posture 2, Timing 3.*

### 2. Choose a Martial Arts Style
Select **one** Martial Arts Style (Boxing, Muay Thai, Judo, Wrestling, or Taekwondo). 
*   This grants you your Style Perks and dictates which sub-actions you are allowed to perform (see **Martial Arts Styles** below).

### 3. Purchase Technique Masteries
You have **4 Mastery Points** to spend on the sub-actions allowed by your chosen style:
*   **Trained (Rank 1)** ($+2$ bonus to rolls): Costs **1 point**.
*   **Mastered (Rank 2)** (Advantage and $+2$ bonus to rolls): Costs **2 points** (requires Rank 1 first).
    *   *Example (Boxer): Spent 1 point to Train Jab, 1 point to Train Dodge, and 2 points to Master Hook.*

### 4. Calculate Secondary Stats
*   **Max Stamina**: $10 + (\text{Posture} \times 2)$.
*   **Starting Stamina**: Matches Max Stamina.
*   **Starting ISS (Injury Severity Score)**: $0$ (no injuries).

---

## Combat Actions Triangle

The core combat dynamic follows a rock-paper-scissors-style relationship:

*   **Strike** beats **Throw** ($\text{Strike} > \text{Throw}$): A strike interrupts the grab attempt.
*   **Block** beats **Strike** ($\text{Block} > \text{Strike}$): A guard absorbs or deflects the blow.
*   **Throw** beats **Block** ($\text{Throw} > \text{Block}$): A passive defensive guard makes you easy to grapple.

---

## Action Types & Sub-Actions

When choosing an action, you must also select one of its sub-actions. Each sub-action offers tactical trade-offs in speed, power, and secondary effects.

### 1. Strikes
Strikes aim to inflict damage and interrupt throws.

#### A. Punches
*   **Jab** (0 Stamina): Fastest punch. High accuracy, low damage. Interrupts slower actions.
*   **Cross** (1 Stamina): Straight power punch. Moderate speed, high damage. Standard damage-dealer.
*   **Hook** (1 Stamina): Looping power punch. Slower speed, high damage. Acts as a counterpunch, gaining a damage bonus if the opponent also chose a Strike.
*   **Uppercut** (2 Stamina): Vertical power punch. Slow speed, massive damage. Bypasses low guards/crouching stances, but highly vulnerable to fast punches.

#### B. Kicks
*   **Low Kick** (1 Stamina): Fast leg strike. Targets stability; successful hits reduce the opponent's speed and evasion next round.
*   **Body Kick** (2 Stamina): Mid-height power kick. Moderate speed and damage. Focuses on exhaustion, draining 3 Stamina from the opponent.
*   **High Kick** (2 Stamina): High-impact head kick. Very slow speed, massive damage. High chance to stun or knock out the opponent, but easily parried or caught.
*   **Push Kick (Teep)** (1 Stamina): Straight thrusting kick. Fast speed, low damage. Pushes the opponent back, resetting combat to neutral range and canceling throw/clinch attempts.

---

### 2. Blocks
Blocks aim to mitigate damage from incoming strikes.

*   **High Guard** (0 Stamina): Standard standing block protecting the head and torso. Negates most punch damage and high/mid kicks. Vulnerable to low kicks and easily bypassed by Throws.
*   **Low Guard** (0 Stamina): Crouching or dropped block protecting the legs. Negates low kicks and leg attacks. Vulnerable to high strikes and easily bypassed by Throws.
*   **Parry** (1 Stamina): High-skill deflection. Low passive defense, but if successful against a Strike, it staggers the opponent and allows a guaranteed fast counter-strike (e.g., a Jab) on the next action.
*   **Dodge / Evasion** (2 Stamina): Dynamic movement to completely avoid attacks. Completely avoids any Strike regardless of height. Succeeding grants a movement or positioning advantage.

---

### 3. Throws
Throws aim to bypass blocks, control the opponent, and force them to the ground.

*   **Clinch / Grab** (0 Stamina): Simple entry grapple to hold the opponent. Deals no initial damage, but prevents the opponent from backing away and sets up advanced grappling.
*   **Trip / Sweep** (1 Stamina): Quick attack on the opponent's base/balance. Fast speed, low damage. Knocks opponent prone. Especially effective against High Guards.
*   **Hip / Shoulder Throw** (2 Stamina): High-impact projection throw. Moderate speed, high damage. Knocks the opponent prone and stuns them for a turn.
*   **Takedown (Double Leg)** (2 Stamina): Power drive to force the opponent down. Bypasses High Guards entirely, but highly vulnerable to fast Strikes like Uppercuts or Jabs.

---

## Attributes & Technique Masteries

A character's physical and mental combat capabilities are defined by three Attributes (**Option 3**), a secondary pool of Stamina, and their specific training in various sub-actions, called Technique Masteries (**Option 2**).

### Combat Attributes
*   **Footwork**: Agility, movement speed, evasive positioning, and lower-body dexterity.
*   **Posture**: Physical structure, strength, balance, stability, and leverage.
*   **Timing**: Perception, reaction speed, precision, and mental focus.

### Combat Resources: Stamina
Physical combat is taxing. Characters have a **Stamina** pool representing their short-term endurance.
*   **Max Stamina**: Derived from Posture: $\text{Max Stamina} = 10 + (\text{Posture} \times 2)$.
*   **Stamina Recovery**: At the end of each round, all combatants recover $2$ Stamina.
*   **Stamina Costs**: Sub-actions cost 0, 1, or 2 Stamina to perform (see mapping below).
*   **Exhaustion (0 Stamina)**: If a character’s Stamina reaches 0:
    *   They cannot choose any **Heavy Actions** (2 Stamina cost).
    *   All their action rolls suffer **Disadvantage** (roll $3\text{d}10$ and keep the two *lowest* dice).

### Technique Masteries (Skills)
Characters can train in individual sub-actions (e.g., *Jab*, *Low Kick*, *Parry*, *Hip/Shoulder Throw*):
*   **Untrained (Rank 0)**: You only add your governing Attribute to your roll.
*   **Trained (Rank 1)**: You gain a $+2$ bonus to your roll.
*   **Mastered (Rank 2)**: You gain **Advantage** (roll $3\text{d}10$, keep the two highest dice) and a $+2$ bonus to your roll.

### Attribute & Stamina Mapping
Each sub-action is governed by a specific Attribute and has a set Stamina cost:

| Sub-Action | Governing Attribute | Main Action | Stamina Cost | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Jab** | **Timing** | Strike | 0 | Speed and timing-based entry. |
| **Cross** | **Posture** | Strike | 1 | Strong structure and weight transfer. |
| **Hook** | **Timing** | Strike | 1 | Precise flanking angle. |
| **Uppercut** | **Posture** | Strike | 2 | Power generated from legs/base. |
| **Low Kick** | **Footwork** | Strike | 1 | Quick leg sweep/strike. |
| **Body Kick** | **Posture** | Strike | 2 | Strong hip rotation and structure. Drains target stamina. |
| **High Kick** | **Footwork** | Strike | 2 | Balance and flexibility. High impact. |
| **Push Kick (Teep)** | **Footwork** | Strike | 1 | Spacing and foot placement. |
| **High Guard** | **Posture** | Block | 0 | Standing structure and stance. |
| **Low Guard** | **Posture** | Block | 0 | Crouching stability. |
| **Parry** | **Timing** | Block | 1 | Precise timing of deflection. |
| **Dodge / Evasion** | **Footwork** | Block | 2 | Moving the body out of range. |
| **Clinch / Grab** | **Timing** | Throw | 0 | Catching/securing limbs. |
| **Trip / Sweep** | **Footwork** | Throw | 1 | Precise foot placement and trip. |
| **Hip / Shoulder Throw** | **Posture** | Throw | 2 | Lifting via mechanical leverage. |
| **Takedown (Double Leg)** | **Posture** | Throw | 2 | Driving forward with body structure. |

---

## Injuries & Trauma (Simplified ISS)

Instead of using a numerical hitpoint pool, this system uses a simplified version of the clinical **Injury Severity Score (ISS)** and **Abbreviated Injury Scale (AIS)** to track bodily trauma. Combatants suffer discrete injuries that degrade their combat attributes in real-time, eventually leading to a knockout or stoppage.

### 1. Body Regions & Attribute Penalties
Injuries are categorized into three distinct body regions. The highest AIS injury in a region acts as a direct penalty to its corresponding attribute:

*   **Head & Face** (governs **Timing**): Concussions, broken jaws, brain bleeds, orbital fractures.
*   **Body & Torso** (governs **Posture**): Broken ribs, winded lungs, internal organ trauma.
*   **Limbs & Extremities** (governs **Footwork**): Sprained ankles, broken hands, swept legs.

### 2. The Abbreviated Injury Scale (AIS)
Every injury has an AIS severity rating from 1 to 5:

| AIS Rating | Severity | Attribute Penalty | Example Injuries |
| :--- | :--- | :--- | :--- |
| **AIS 1** | Minor | None (Drains 2 Stamina) | Swollen eye, bruised ribs, superficial cut. |
| **AIS 2** | Moderate | $-1$ to Region's Attribute | Mild concussion, cracked rib, sprained wrist. |
| **AIS 3** | Serious | $-2$ to Region's Attribute | Shattered nose/jaw, fractured hand, deep muscle tear. |
| **AIS 4** | Severe | $-3$ to Region's Attribute | Severe brain bleed, fractured knee, broken collarbone. |
| **AIS 5** | Critical | Instant Defeat / Stoppage | Unconsciousness, ruptured organ, broken spine. |

### 3. Injury Severity Score (ISS)
A combatant's overall trauma is represented by their ISS, which is the sum of the single highest AIS score from each of the three regions:

$$\text{ISS} = \text{Head Max AIS} + \text{Body Max AIS} + \text{Limbs Max AIS}$$

*   **Major Trauma (Stoppage)**: If a combatant's **ISS reaches 10**, or if any single region suffers an **AIS 5** injury, they are immediately defeated (knocked out, submit, or stopped by the referee/medical staff).

### 4. Inflicting & Mitigating Injuries

#### Inflicting Injuries
When an attack connects, it inflicts a base AIS score depending on its impact power:
*   **Low Impact (AIS 1)**: Jab (Targets Head or Body, attacker's choice).
*   **Medium Impact (AIS 2)**: Cross (Head/Body), Hook (Head/Body), Low Kick (Targets Limbs), Push Kick (Targets Body), Trip/Sweep (Targets Limbs).
*   **High Impact (AIS 3)**: Uppercut (Head/Body), Body Kick (Targets Body), High Kick (Targets Head), Hip/Shoulder Throw (Targets Body), Takedown (Targets Limbs).

*Note: Successful Throws also knock the target **Prone**.*

#### Success Modifier
If the attacker wins the clash with a **Critical Success** (succeeding by a margin of 5 or more), the injury severity increases by $+1$ AIS (up to a maximum of AIS 5).

#### Cumulative Trauma
Injuries to the same region accumulate. If a region already has an injury, and a new attack connects and inflicts an injury of at least AIS 1:
*   If the new injury is **equal to or higher than** the existing injury, the region's AIS rating increases to the new value, plus $+1$.
*   If the new injury is **lower than** the existing injury, the region's AIS rating increases by $+1$ (representing cumulative swelling, bleeding, or structural wear).
*   *Note: A region's AIS rating can never exceed 5 (Critical/Defeat).*


#### Mitigation (Blocking & Dodging)
If a defender successfully guards or dodges, they subtract their defense rating from the incoming attack's base AIS before applying the injury:
*   **High/Low Guard**: Mitigates 2 AIS.
*   **Dodge / Evasion**: Mitigates 3 AIS.
*   **Parry**: If the parry check succeeds, it mitigates 100% of incoming AIS and staggers the attacker.

*Example: A combatant is hit by a High Kick (Base AIS 3) while using a High Guard (Mitigates 2). The final injury is AIS 1 (3 - 2 = 1) to the Head & Face region, draining 2 Stamina but causing no attribute penalty.*

---

## Range & Movement

Combat takes place across three fluid **Ranges**. Combatants control the distance by using their actions to advance, retreat, or push their opponent back.

### 1. The Three Combat Ranges

*   **Outfighting (Long Range)**: Spaced out, circling.
    *   *Allowed Actions*: Only long Strikes (Low Kick, Body Kick, High Kick, Push Kick). Punches and Throws are out of range.
    *   *Mobility Perk*: **Dodge / Evasion** costs $0$ Stamina at this range.
*   **Striking Range (Medium Range)**: The pocket, exchange range.
    *   *Allowed Actions*: All Strikes (Punches & Kicks) and Blocks. Throws are out of range.
*   **Clinch Range (Close Range)**: Grappling, tied up.
    *   *Allowed Actions*: All Throws (Clinch/Grab, Trip, Hip Throw, Takedown). Punches and Kicks cannot be used (except Uppercuts and style-specific Clinch strikes).

### 2. Controlling the Distance
Fighters change range by winning clashes with specific sub-actions:

#### A. Advancing (Closing the Distance)
To move closer, perform a **Throw (Black)** action:
*   **Clinch / Grab** or **Takedown**: Winning the check moves you forward one range step (e.g., Striking $\rightarrow$ Clinch).
*   *Critical Success*: Advancing with a Critical Success allows you to move two range steps (e.g., Outfighting $\rightarrow$ Clinch).

#### B. Retreating (Creating Distance)
To step back safely, perform an evasive **Block (White)** action:
*   **Dodge / Evasion**: Winning the check allows you to retreat one range step (e.g., Clinch $\rightarrow$ Striking).
*   *Note: If the check fails, the attacker keeps you trapped at the closer range.*

#### C. Forcing Distance (Pushing Back)
To actively push an opponent away, perform a specialized **Strike (Red)** action:
*   **Push Kick (Teep)**: A successful hit pushes the opponent back one range step (e.g., Clinch $\rightarrow$ Striking).

---

## Mechanics & Resolution

### Contested Round Structure
Combat is played in simultaneous **Rounds** resolved by a single **Contested Roll**:

1. **Phase 1: Choose & Roll**
   * Combatants secretly select the $2\text{d}10$ color pair corresponding to their main action:
     * **Red Dice** = **Strike**
     * **White Dice** = **Block (Defend)**
     * **Black Dice** = **Throw**
   * Both combatants roll their chosen dice simultaneously and verbally declare their chosen sub-action (e.g., "Jab" or "Dodge").

2. **Phase 2: Resolve (Contested Roll-Off)**
   * Each combatant calculates their **Roll Total**:
     $$\text{Roll Total} = \text{Dice Result} + \text{Governing Attribute} + \text{Technique Mastery Bonus}$$
   * The combatant with the **higher Roll Total wins the round**, and their chosen sub-action succeeds. The loser's action fails.
   * **The RPS Triangle** determines who rolls with a mechanical advantage:
     * **Triangle Winner**: Rolls with **Advantage** (roll $3\text{d}10$, keep the two highest dice) and adds $+2$ to their total.
     * **Triangle Loser**: Rolls their standard $2\text{d}10$ check.
     * *Note: The triangle winner is statistically favored to win the contest, but a high-rolling triangle loser can still overcome the advantage and win the round.*

---

### 1. Resolving the Triangle (RPS)

*   **Different Actions (Triangle Check)**: If the rolled colors match a winning/losing pair (e.g., Red vs. Black / Strike vs. Throw):
    *   The triangle winner rolls with Advantage $+2$.
    *   The triangle loser rolls normally.
    *   *Example (Block vs. Strike)*: White beats Red. The Blocker rolls with Advantage $+2$; the Striker rolls normally. 
        *   If the **Blocker wins the contested roll**, the block succeeds and mitigates the strike's AIS.
        *   If the **Striker wins the contested roll** (beating the blocker's roll despite the blocker's advantage), the strike bypasses the guard entirely, dealing full, unmitigated AIS injury.
*   **Same Actions (Same Color Rolls)**:
    *   **Red vs. Red (Strike vs. Strike)**: Both roll normally (no Advantage). The higher total wins the round, landing their strike. The loser's strike misses or is beat to the punch.
    *   **White vs. White (Block vs. Block)**: No contest is needed. Both combatants remain passive in guard. Both recover $+2$ extra Stamina (for a total of 4 recovered this round).
    *   **Black vs. Black (Throw vs. Throw)**: A grapple struggle. Both roll off normally using either **Posture** or **Timing**. The higher total wins the check, securing a Clinch or a throw.

### 2. Dice Checks (2d10 System)
To resolve the contested roll, combatants calculate their totals using the following:
*   **Action Roll**: Roll the chosen $2\text{d}10$ (or $3\text{d}10$ based on Advantage or Technique Mastery).
*   **Attribute Modifier**: Add the governing Attribute (**Footwork**, **Posture**, or **Timing**).
*   **Mastery Modifier**: Add the Technique Mastery bonus ($+2$ if Trained or Mastered).
*   **Compare Totals**:
    *   **Success**: Have the higher Roll Total.
    *   **Critical Success**: Succeeding by a margin of 5 or more (Winner Total - Loser Total $\ge 5$) activates secondary weapon/style/critical effects, and increases incoming injury by $+1$ AIS.

---

## Martial Arts Styles

Characters can adopt a specific Martial Arts Style, which dictates their available sub-actions and provides unique mechanical perks:

### 1. Boxing (The Sweet Science)
*   **Focus**: Punches & Head Movement.
*   **Allowed Actions**:
    *   *Strikes*: Jab, Cross, Hook, Uppercut (No Kicks).
    *   *Blocks*: High Guard, Parry, Dodge/Evasion (No Low Guard).
    *   *Throws*: Clinch/Grab only (No Trip, Hip Throw, or Takedown).
*   **Style Perks**:
    *   **Slip & Counter**: Successfully defending with Dodge/Evasion allows a free Hook or Uppercut counter-attack on your next turn.
    *   **Iron Chin**: High Guard mitigates 100% of punch damage (normally absorbs 80%).

### 2. Muay Thai (Art of Eight Limbs)
*   **Focus**: Bone-breaking Kicks & Clinch Grappling.
*   **Allowed Actions**:
    *   *Strikes*: Jab, Hook, and all Kicks (Low, Body, High, Push).
    *   *Blocks*: High Guard, Parry (No Low Guard or Dodge).
    *   *Throws*: Clinch/Grab only (No Trip, Hip Throw, or Takedown).
*   **Style Perks**:
    *   **Thai Clinch**: While holding an opponent in a Clinch/Grab, you can execute Knee strikes (deals Uppercut damage at Jab speed).
    *   **Heavy Leg Kicks**: Low Kicks deal moderate damage in addition to reducing the opponent's speed and evasion.

### 3. Judo (The Gentle Way)
*   **Focus**: Redirection & High-Impact Throws.
*   **Allowed Actions**:
    *   *Strikes*: None.
    *   *Blocks*: High Guard, Parry (No Low Guard or Dodge).
    *   *Throws*: Clinch/Grab, Trip/Sweep, Hip/Shoulder Throw.
*   **Style Perks**:
    *   **Kuzushi (Off-Balance)**: If you successfully parry a Strike (White vs. Red), you can immediately attempt a Hip/Shoulder Throw or Trip/Sweep as a free reaction check.
    *   **Sweeping Reversal**: Your Trip/Sweep gains Advantage against opponents performing a High Kick.

### 4. Wrestling (Ground Dominance)
*   **Focus**: Clinches & Power Takedowns.
*   **Allowed Actions**:
    *   *Strikes*: None.
    *   *Blocks*: High Guard, Low Guard (No Parry or Dodge).
    *   *Throws*: Clinch/Grab, Trip/Sweep, Takedown (Double Leg).
*   **Style Perks**:
    *   **Shooter**: Double Leg Takedowns gain Advantage against opponents in a High Guard.
    *   **Ground Control**: Winning a Grapple Struggle (Black vs. Black) automatically knocks the opponent prone and pins them, preventing them from choosing a Strike next turn.

### 5. Taekwondo / Karate (Long-Range Kicking)
*   **Focus**: Agile Footwork & High Kicks.
*   **Allowed Actions**:
    *   *Strikes*: Jab, Cross, and all Kicks.
    *   *Blocks*: High Guard, Dodge/Evasion (No Low Guard or Parry).
    *   *Throws*: None.
*   **Style Perks**:
    *   **Spinning Kicks**: High Kicks do not suffer speed penalties if performed immediately following a successful Push Kick (Teep).
    *   **Outfighting**: Evasion actions do not cost stamina if you are outside of clinch range.

---

## Healing & Recovery

### 1. Post-Fight Healing (Long-Term Rest)
Outside of active combat, injuries heal naturally over time depending on their severity. If a fighter goes on medical suspension or takes downtime, refer to the table below:

| Injury Severity | Recovery Time | Medical Requirement | Permanent Effects |
| :--- | :--- | :--- | :--- |
| **AIS 1 (Minor)** | Short Rest (10 mins) or Sleep | None | None |
| **AIS 2 (Moderate)**| 1 Week of light activity | Basic rest, ice, braces | None |
| **AIS 3 (Serious)** | 3 Weeks of strict rest | Stitches, splints, or casts | Requires a **Posture** check (DC 10) to avoid scarring or a permanent $-1$ penalty to that region. |
| **AIS 4 (Severe)**  | 2 Months of downtime | Hospital stay, surgery | Requires a **Posture** check (DC 12) to avoid permanent $-1$ attribute reduction. |
| **AIS 5 (Critical)**| 4+ Months of rehabilitation | Advanced surgery & physical therapy | Must pass a DC 14 **Posture** check; failure results in permanent $-1$ to all attributes. |

### 2. Stamina Recovery Outside Combat
*   Once combat ends and the fighter catches their breath (approx. 5 minutes of rest), their **Stamina is fully restored** to their current maximum.
