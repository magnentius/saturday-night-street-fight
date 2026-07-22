#!/usr/bin/env python3
import sys
import os
import random
from pc_generator import STYLES, ATTRIBUTES, generate_random_character, format_character_sheet

PUNK_NICKNAMES = [
    "Slick", "Weasel", "Razor", "Spitfire", "Zipper", "Ditch", "Gator", "Rat", "Clutch", "Flea", 
    "Switchblade", "Sneaker", "Cricket", "Shadow", "Grease", "Buster", "Chucky", "Rusty", "Blinky"
]

THUG_NICKNAMES = [
    "Knuckles", "Meat hook", "Hammer", "Chainsaw", "Mad Dog", "Ironhide", "Bruiser", "Brick", 
    "The Enforcer", "Slugger", "Chopper", "Grizzly", "Viper", "Tracker", "Basher", "Crusher"
]

BOSS_NICKNAMES = [
    "The Don", "Kingpin", "The Overlord", "Mr. Big", "The Syndicate Lead", "The Warlord", 
    "The Shadow Boss", "The Neon King", "Ringleader", "The Captain", "Iron Fist"
]

ENCOUNTERS = {
    1: [
        ("Empty Street", "A quiet, peaceful night under the streetlights. No threats."),
        ("Friendly Merchant", "A local vendor or ally offers a discount. Buy warm food to recover 1 attribute damage (3 XP, or 1 XP with a Cool Check [DC 10] success)."),
        ("Transit Police Patrol", "Active police presence. Brawling is forbidden; combat actions immediately summon police enforcers."),
        ("Local Informant", "A street contact shares rumors. Roll a Cool Check (DC 10) to gain Advantage on the next Subway Station Event roll."),
        ("Safe Alleyway", "A hidden, dry alcove to hide. Players can safely rest here to recover minor attribute damage (+1 to all stats at 1 or higher)."),
        ("Minor Nuisance", "A single pickpocket (Tier 1 Punk) attempts a grab and run. They flee if the player wins a contested Cool or Timing check.")
    ],
    2: [
        ("Quiet Corridor", "The block is quiet, but shadows flicker in the alleys. No immediate threats."),
        ("Solitary Lookout", "A single Tier 1 Lookout stands guard. Players can sneak past (contested Timing) or bluff past (contested Cool)."),
        ("Street Craps Game", "A group of locals gambling. Players can wager 3 XP on a single contested Cool check against the dealer. Win to gain +6 XP."),
        ("Foot Patrol", "Two Tier 1 Punks walking the beat. They harass the players unless intimidated by a contested Cool check."),
        ("Drunk Fighter", "A single Tier 2 Thug who is highly intoxicated and looking for a brawl (rolls with Disadvantage)."),
        ("Shakedown", "A single Tier 2 Thug demands a toll (1 XP). Players can pay, fight, or bluff past with a contested Cool check.")
    ],
    3: [
        ("Watchful Eyes", "Gang watchmen occupy the rooftops. Crossing without panic requires a contested Cool check to blend into the shadows."),
        ("Rival Patrol", "Two Tier 2 Thugs of the local style patrolling."),
        ("Heavy Hitter", "A single Tier 2 Thug carrying an improvised weapon (baseball bat or pipe), adding +1 damage to all successful Strikes."),
        ("Gang Rush", "A Mob of Punks (Tier 1) rushes the players, starting at Striking Range."),
        ("Corner Defense", "Two Tier 2 Thugs guarding a business entry. They block passage until defeated."),
        ("Alleyway Ambush", "A Mob of Punks (Tier 1) ambushes the players from the shadows, starting immediately at Clinch Range.")
    ],
    4: [
        ("Fortified Blockade", "Barbwire and wooden crates block the street. Crossing requires a contested Posture check against two Tier 2 Thugs."),
        ("Elite Enforcer", "A single Tier 2 Thug who has upgraded one of their style techniques to Mastered Rank 2 (+5) stands guard."),
        ("Warlord Patrol", "Three Tier 2 Thugs patrolling in close coordination."),
        ("The Pack", "A Mob of Punks (Tier 1) led by a Tier 2 Thug enforcer."),
        ("Hit Squad", "Two Tier 2 Thugs who coordinate their attacks to specifically target the players' lowest attribute."),
        ("Double Ambush", "Two separate Mobs of Punks (Tier 1) attack from both sides (Flanking rules apply).")
    ],
    5: [
        ("Grime Trap", "Low visibility and steam vents cover the street. All action rolls on this block suffer a -1 penalty."),
        ("The Elite Guard", "Two Tier 3 Bosses (built using full Character Creation rules) patrolling."),
        ("Syndicate Patrol", "A Mob of Punks (Tier 1) led by an elite Tier 3 Boss enforcer."),
        ("Style Champion", "A Tier 3 Boss who has active style perks and multiple Mastered techniques (+5) challenges the players to a 1-on-1 duel."),
        ("Death Alley Ambush", "Two Tier 2 Thugs and one Tier 3 Boss ambush the players immediately at Clinch Range."),
        ("The Overlord", "The main Boss of the sector is present with a personal bodyguard of two Tier 2 Thugs.")
    ]
}

def generate_punk():
    nickname = random.choice(PUNK_NICKNAMES)
    name = f"'{nickname}'"
    attrs = {attr: 1 for attr in ATTRIBUTES}
    return {
        "name": name,
        "tier": "Tier 1: Punk/Lookout",
        "attrs": attrs,
        "masteries": {},
        "perks": ["None (Untrained)"]
    }

def generate_thug():
    nickname = random.choice(THUG_NICKNAMES)
    style_name = random.choice(list(STYLES.keys()))
    style = STYLES[style_name]
    name = f"'{nickname}' ({style_name})"
    
    attrs = {attr: 2 for attr in ATTRIBUTES}
    
    # 2 Trained masteries (+2 bonus) from allowed moves
    allowed_moves = style["Strikes"] + style["Blocks"] + style["Throws"]
    selected_moves = random.sample(allowed_moves, min(2, len(allowed_moves)))
    masteries = {move: 1 for move in selected_moves}
    
    return {
        "name": name,
        "tier": "Tier 2: Standard Thug",
        "style": style_name,
        "focus": style["Focus"],
        "attrs": attrs,
        "masteries": masteries,
        "perks": style["Perks"]
    }

def generate_boss():
    nickname = random.choice(BOSS_NICKNAMES)
    name, style_name, arch_name, attrs, masteries, unspent_xp = generate_random_character()
    full_name = f"'{nickname}' {name} ({style_name})"
    style = STYLES[style_name]
    return {
        "name": full_name,
        "tier": "Tier 3: Syndicate Boss",
        "style": style_name,
        "focus": style["Focus"],
        "attrs": attrs,
        "masteries": masteries,
        "perks": style["Perks"],
        "unspent_xp": unspent_xp
    }

def print_npc(npc):
    print("-" * 50)
    print(f"Name: {npc['name']}")
    print(f"Tier: {npc['tier']}")
    if "style" in npc:
        print(f"Style: {npc['style']} ({npc['focus']})")
    print(f"Attributes: T{npc['attrs']['timing']}/P{npc['attrs']['posture']}/F{npc['attrs']['footwork']}/S{npc['attrs']['stamina']}/C{npc['attrs']['cool']}")
    
    print("Masteries:")
    if not npc["masteries"]:
        print("  None (Untrained Rank 0)")
    for move, rank in npc["masteries"].items():
        rank_text = "Trained (Rank 1, +2)" if rank == 1 else "Mastered (Rank 2, +5)"
        print(f"  - {move.title()}: {rank_text}")
        
    print("Style Perks:")
    for perk in npc["perks"]:
        # strip markdown formatting for cleaner terminal print
        clean_perk = perk.replace("**", "")
        print(f"  - {clean_perk}")

def print_header(title):
    print("=" * 60)
    print(f" {title.upper()} ".center(60, "="))
    print("=" * 60)

def generate_encounter(danger_rank=None):
    if not danger_rank:
        danger_rank = random.randint(1, 5)
        
    roll = random.randint(1, 6)
    title, desc = ENCOUNTERS[danger_rank][roll - 1]
    
    print_header(f"Danger Rank {danger_rank} Encounter (Roll: {roll})")
    print(f"Encounter: {title}")
    print(f"Description: {desc}\n")
    
    # Spawn NPCs based on encounter type
    npcs = []
    
    if title == "Minor Nuisance":
        npcs.append(generate_punk())
    elif title == "Solitary Lookout":
        npcs.append(generate_punk())
    elif title == "Foot Patrol":
        npcs.append(generate_punk())
        npcs.append(generate_punk())
    elif title == "Drunk Fighter":
        thug = generate_thug()
        thug["name"] += " [INTOXICATED: rolls at Disadvantage]"
        npcs.append(thug)
    elif title == "Shakedown":
        npcs.append(generate_thug())
    elif title == "Rival Patrol":
        npcs.append(generate_thug())
        npcs.append(generate_thug())
    elif title == "Heavy Hitter":
        thug = generate_thug()
        thug["name"] += " [WEAPON: deals +1 damage]"
        npcs.append(thug)
    elif title == "Gang Rush":
        print("Rush Combat: 3 Punks (Tier 1). Spawning Mob Stat Block:")
        mob = {
            "name": "Mob of Punks (3 Members)",
            "tier": "Mob Block (Punks)",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        npcs.append(mob)
    elif title == "Corner Defense":
        npcs.append(generate_thug())
        npcs.append(generate_thug())
    elif title == "Alleyway Ambush":
        print("Ambush Combat: 3 Punks (Tier 1). Spawning Mob Stat Block:")
        mob = {
            "name": "Mob of Punks (3 Members)",
            "tier": "Mob Block (Punks) [AMBUSH: Advantage on first round]",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        npcs.append(mob)
    elif title == "Fortified Blockade":
        print("Fortified defense: 2 Thugs behind barricades.")
        npcs.append(generate_thug())
        npcs.append(generate_thug())
    elif title == "Elite Enforcer":
        thug = generate_thug()
        # Make one move Mastered
        if thug["masteries"]:
            move = list(thug["masteries"].keys())[0]
            thug["masteries"][move] = 2
        thug["name"] = "Elite " + thug["name"]
        npcs.append(thug)
    elif title == "Warlord Patrol":
        npcs.append(generate_thug())
        npcs.append(generate_thug())
        npcs.append(generate_thug())
    elif title == "The Pack":
        print("Spawning 3 Punks Mob led by 1 Thug enforcer.")
        npcs.append(generate_thug())
        mob = {
            "name": "The Pack (Mob of 3 Punks)",
            "tier": "Mob Block (Punks)",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        npcs.append(mob)
    elif title == "Hit Squad":
        print("Hit Squad: Two Thugs targeting lowest player attribute.")
        npcs.append(generate_thug())
        npcs.append(generate_thug())
    elif title == "Double Ambush":
        print("Double Ambush: Two separate Mobs of 3 Punks (Flanking rules apply!).")
        mob1 = {
            "name": "Mob Alpha (3 Punks)",
            "tier": "Mob Block (Punks)",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        mob2 = {
            "name": "Mob Beta (3 Punks)",
            "tier": "Mob Block (Punks)",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        npcs.append(mob1)
        npcs.append(mob2)
    elif title == "The Elite Guard":
        npcs.append(generate_boss())
        npcs.append(generate_boss())
    elif title == "Syndicate Patrol":
        npcs.append(generate_boss())
        mob = {
            "name": "Bodyguard Mob (3 Punks)",
            "tier": "Mob Block (Punks)",
            "attrs": {"timing": 3, "posture": 3, "footwork": 3, "stamina": 3, "cool": 3},
            "masteries": {},
            "perks": ["Mob Rules: Every 3 damage knocks out 1 punk and reduces all attributes by -1."]
        }
        npcs.append(mob)
    elif title == "Style Champion":
        npcs.append(generate_boss())
    elif title == "Death Alley Ambush":
        npcs.append(generate_thug())
        npcs.append(generate_thug())
        npcs.append(generate_boss())
    elif title == "The Overlord":
        boss = generate_boss()
        boss["name"] = "OVERLORD " + boss["name"]
        npcs.append(boss)
        npcs.append(generate_thug())
        npcs.append(generate_thug())

    for npc in npcs:
        print_npc(npc)

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ["--punk", "-p"]:
            print_npc(generate_punk())
        elif arg in ["--thug", "-t"]:
            print_npc(generate_thug())
        elif arg in ["--boss", "-b"]:
            print_npc(generate_boss())
        elif arg in ["--danger", "-d"]:
            try:
                rank = int(sys.argv[2])
                if 1 <= rank <= 5:
                    generate_encounter(rank)
                else:
                    print("Danger Rank must be between 1 and 5.")
            except (IndexError, ValueError):
                print("Usage: ./npc_generator.py --danger <1-5>")
        else:
            print("Options:")
            print("  --punk   : Generate a Tier 1 Punk/Lookout")
            print("  --thug   : Generate a Tier 2 Thug")
            print("  --boss   : Generate a Tier 3 Boss")
            print("  --danger : Generate an encounter for a specific Danger Rank (1-5)")
            print("  (no args): Generate a completely random street block encounter")
    else:
        generate_encounter()

if __name__ == "__main__":
    main()
