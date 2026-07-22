#!/usr/bin/env python3
import sys
import os
import random

# Core definitions for styles and their allowed sub-actions
STYLES = {
    "Boxing": {
        "Focus": "Punches & Head Movement",
        "Strikes": ["jab", "cross", "hook", "uppercut"],
        "Blocks": ["high guard", "parry", "dodge"],
        "Throws": ["clinch"],
        "Perks": [
            "**Slip & Counter**: Defending with Dodge allows free Hook or Uppercut counter next round.",
            "**Iron Chin**: High Guard mitigates +1 damage against Punches (total 3 damage)."
        ]
    },
    "Muay Thai": {
        "Focus": "Bone-breaking Kicks & Clinch Grappling",
        "Strikes": ["jab", "hook", "low kick", "body kick", "high kick", "push kick"],
        "Blocks": ["high guard", "parry"],
        "Throws": ["clinch"],
        "Perks": [
            "**Thai Clinch**: While clinching, Knee strikes (Timing-based) deal 3 damage to Timing or Stamina.",
            "**Heavy Leg Kicks**: Low Kicks deal 2 Footwork damage and apply a severe Hobbled status condition (-2 penalty next round)."
        ]
    },
    "Judo": {
        "Focus": "Redirection & High-Impact Throws",
        "Strikes": ["jab", "ground & pound"],
        "Blocks": ["high guard", "parry"],
        "Throws": ["clinch", "trip", "hip throw"],
        "Perks": [
            "**Kuzushi (Off-Balance)**: Successfully parrying a strike lets you immediately attempt a Hip Throw or Trip as a free reaction check.",
            "**Sweeping Reversal**: Trip/Sweep gains Advantage against opponents performing a High Kick."
        ]
    },
    "Wrestling": {
        "Focus": "Clinches & Power Takedowns",
        "Strikes": ["jab", "dirty punch", "ground & pound"],
        "Blocks": ["high guard", "low guard"],
        "Throws": ["clinch", "trip", "takedown"],
        "Perks": [
            "**Shooter**: Double Leg Takedowns gain Advantage against opponents in a High Guard.",
            "**Ground Control**: Winning a Grapple Struggle (Black vs Black) automatically knocks the opponent prone and pins them."
        ]
    },
    "Taekwondo": {
        "Focus": "Agile Footwork & High Kicks",
        "Strikes": ["jab", "cross", "low kick", "body kick", "high kick", "push kick"],
        "Blocks": ["high guard", "dodge"],
        "Throws": [],
        "Perks": [
            "**Spinning Kicks**: High Kicks gain a +2 bonus if performed immediately following a successful Push Kick (Teep).",
            "**Outfighting**: Evasion/Dodge actions gain a +2 bonus if you are outside of Clinch Range."
        ]
    }
}

ATTRIBUTES = ["timing", "posture", "footwork", "stamina", "cool"]

def print_header(title):
    print("=" * 60)
    print(f" {title.upper()} ".center(60, "="))
    print("=" * 60)

def generate_random_character(name=None):
    if not name:
        first_names = ["Jack", "Kenji", "Vinnie", "Mickey", "Spider", "Buster", "Sonny", "Cassius", "Rocky", "Dutch"]
        last_names = ["Cooper", "Sato", "Gambini", "O'Neill", "Cruz", "Keaton", "Barbosa", "Mercer", "Kovacs", "Miller"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"

    style_name = random.choice(list(STYLES.keys()))
    style = STYLES[style_name]
    
    xp = 50
    attrs = {attr: 2 for attr in ATTRIBUTES}
    
    # Archetype guidelines for intelligent stat & mastery allocation
    archetypes = {
        "Boxing": [
            {
                "name": "Classic Slugger",
                "attrs": ["timing", "stamina", "posture"],
                "moves_priority": [
                    ("hook", 2),       # Primary attack (Mastered)
                    ("dodge", 1),      # Primary defense (Trained)
                    ("jab", 1),        # Set up counters (Trained)
                    ("dodge", 2),      # Master defense (Mastered)
                    ("cross", 1)       # Secondary attack (Trained)
                ]
            },
            {
                "name": "The Showman (Cool-Focused)",
                "attrs": ["cool", "timing", "stamina"],
                "moves_priority": [
                    ("taunt", 2),      # Master mental damage (Mastered)
                    ("dodge", 1),      # Composure defense (Trained)
                    ("hook", 1),       # Attack (Trained)
                    ("taunt", 2),      # Ensure Taunt is fully Mastered
                    ("parry", 1)       # Defensive option (Trained)
                ]
            }
        ],
        "Muay Thai": [
            {
                "name": "Classic Clincher",
                "attrs": ["stamina", "timing", "footwork"],
                "moves_priority": [
                    ("low kick", 2),   # Primary attack (Mastered)
                    ("clinch", 1),     # Set up Thai Clinch knees (Trained)
                    ("high guard", 1), # Composure defense (Trained)
                    ("push kick", 1),  # Range control (Trained)
                    ("hook", 1)        # Backup punch (Trained)
                ]
            },
            {
                "name": "The Intimidator (Cool-Focused)",
                "attrs": ["cool", "stamina", "timing"],
                "moves_priority": [
                    ("taunt", 2),      # Master mental pressure (Mastered)
                    ("clinch", 1),     # Force grapple (Trained)
                    ("low kick", 1),   # Harass legs (Trained)
                    ("high guard", 1), # Cover up (Trained)
                    ("jab", 1)         # Fast strike (Trained)
                ]
            }
        ],
        "Judo": [
            {
                "name": "Classic Kuzushi Thrower",
                "attrs": ["posture", "timing", "cool"],
                "moves_priority": [
                    ("hip throw", 2),  # Primary projection (Mastered)
                    ("parry", 1),      # Trigger Kuzushi reaction (Trained)
                    ("clinch", 1),     # Close distance (Trained)
                    ("ground & pound", 1), # Exploit down position (Trained)
                    ("trip", 1)        # Secondary sweep (Trained)
                ]
            },
            {
                "name": "The Stoic Master (Cool-Focused)",
                "attrs": ["cool", "posture", "timing"],
                "moves_priority": [
                    ("taunt", 2),      # Mental pressure (Mastered)
                    ("hip throw", 1),  # Retaliatory throw (Trained)
                    ("parry", 1),      # Set up counters (Trained)
                    ("ground & pound", 1), # Exploit down position (Trained)
                    ("hip throw", 2)   # Master throw (Mastered)
                ]
            }
        ],
        "Wrestling": [
            {
                "name": "Classic Takedown Dominator",
                "attrs": ["posture", "stamina", "cool"],
                "moves_priority": [
                    ("takedown", 2),   # Primary power takedown (Mastered)
                    ("dirty punch", 1), # Neutral strike option (Trained)
                    ("clinch", 1),     # Close distance (Trained)
                    ("ground & pound", 1), # Exploit down position (Trained)
                    ("low guard", 1)   # Keep base low (Trained)
                ]
            },
            {
                "name": "The Ring Warlord (Cool-Focused)",
                "attrs": ["cool", "posture", "stamina"],
                "moves_priority": [
                    ("taunt", 2),      # Demoralize opponent (Mastered)
                    ("takedown", 1),   # Close the show (Trained)
                    ("dirty punch", 1), # Strike threat (Trained)
                    ("ground & pound", 1), # Exploit pin position (Trained)
                    ("takedown", 2)    # Master takedown (Mastered)
                ]
            }
        ],
        "Taekwondo": [
            {
                "name": "Classic Outfighting Kicker",
                "attrs": ["footwork", "timing", "stamina"],
                "moves_priority": [
                    ("dodge", 2),      # Master outfighting evasion (Mastered)
                    ("push kick", 1),  # Set up spinning kicks (Trained)
                    ("high kick", 2),  # Primary strike (Mastered)
                    ("cross", 1)       # Secondary punch (Trained)
                ]
            },
            {
                "name": "The Flashy Showman (Cool-Focused)",
                "attrs": ["cool", "footwork", "timing"],
                "moves_priority": [
                    ("taunt", 2),      # Trash talk (Mastered)
                    ("dodge", 1),      # Flashy defense (Trained)
                    ("push kick", 1),  # Distance maker (Trained)
                    ("high kick", 1),  # Head strike (Trained)
                    ("dodge", 2)       # Master evasion (Mastered)
                ]
            }
        ]
    }

    arch = random.choice(archetypes[style_name])

    # 1. Allocate attributes based on style priority (costs 10 XP each to bump to 3)
    for attr in arch["attrs"]:
        if xp >= 10:
            attrs[attr] = 3
            xp -= 10

    # 2. Spend remaining XP on prioritized moves list
    masteries = {}
    for move, target_rank in arch["moves_priority"]:
        curr_rank = masteries.get(move, 0)

        if curr_rank < target_rank:
            if target_rank == 1 and curr_rank == 0:
                if xp >= 3:
                    masteries[move] = 1
                    xp -= 3
            elif target_rank == 2 and curr_rank == 0:
                if xp >= 9:
                    masteries[move] = 2
                    xp -= 9
                elif xp >= 3:
                    masteries[move] = 1
                    xp -= 3
            elif target_rank == 2 and curr_rank == 1:
                if xp >= 6:
                    masteries[move] = 2
                    xp -= 6

    # 3. Spend leftover XP randomly on any remaining allowed moves
    allowed_moves = style["Strikes"] + style["Blocks"] + style["Throws"]
    attempts = 0
    while xp >= 3 and attempts < 100:
        attempts += 1
        move = random.choice(allowed_moves)
        curr_rank = masteries.get(move, 0)
        
        if curr_rank == 0:
            masteries[move] = 1
            xp -= 3
        elif curr_rank == 1 and xp >= 6:
            masteries[move] = 2
            xp -= 6

    return name, style_name, arch["name"], attrs, masteries, xp

def format_character_sheet(name, style_name, attrs, masteries, unspent_xp, archetype_name=None):
    style = STYLES[style_name]
    sheet = []
    sheet.append(f"# Character Sheet: {name}")
    if archetype_name:
        sheet.append(f"**Style**: {style_name} — Archetype: {archetype_name} (*{style['Focus']}*)")
    else:
        sheet.append(f"**Style**: {style_name} (*{style['Focus']}*)")
    sheet.append(f"**Unspent Experience**: {unspent_xp} XP\n")
    
    sheet.append("## Attributes")
    for attr in ATTRIBUTES:
        sheet.append(f"*   **{attr.capitalize()}**: {attrs[attr]} (Max 4)")
    sheet.append("")
    
    sheet.append("## Technique Masteries")
    if not masteries:
        sheet.append("*   *None (All sub-actions are Untrained Rank 0)*")
    for move, rank in masteries.items():
        rank_text = "Trained (Rank 1, +3)" if rank == 1 else "Mastered (Rank 2, +5)"
        sheet.append(f"*   **{move.title()}**: {rank_text}")
    sheet.append("")
    
    sheet.append("## Style Perks")
    for perk in style["Perks"]:
        sheet.append(f"*   {perk}")
    
    return "\n".join(sheet)

def interactive_generation(should_write=False):
    print_header("Fighter Creation System")
    name = input("Enter your fighter's name: ").strip()
    if not name:
        name = "Unknown Fighter"

    print("\nChoose your Martial Arts Style:")
    styles_list = list(STYLES.keys())
    for idx, s in enumerate(styles_list, 1):
        print(f"  {idx}. {s} — {STYLES[s]['Focus']}")
    
    while True:
        try:
            choice = int(input("\nSelect style (1-5): "))
            if 1 <= choice <= 5:
                style_name = styles_list[choice - 1]
                break
        except ValueError:
            pass
        print("Invalid choice, try again.")

    style = STYLES[style_name]
    print(f"\nYou selected: {style_name}")
    print(f"Allowed moves: {', '.join(style['Strikes'] + style['Blocks'] + style['Throws'])}")

    xp = 50
    attrs = {attr: 2 for attr in ATTRIBUTES}

    print_header("Attribute Allocation")
    print("Each attribute starts at 2. Spending 10 XP upgrades it to 3 (Max cap at creation).")
    
    for attr in ATTRIBUTES:
        while True:
            print(f"\nRemaining XP: {xp} XP")
            print(f"Current {attr.capitalize()}: {attrs[attr]}")
            up = input(f"Upgrade {attr.capitalize()} to 3? (y/n): ").strip().lower()
            if up == 'y':
                if xp >= 10:
                    attrs[attr] = 3
                    xp -= 10
                    break
                else:
                    print("Not enough XP!")
            elif up == 'n':
                break
            else:
                print("Please enter 'y' or 'n'.")

    print_header("Technique Mastery Allocation")
    print("Train (Rank 1, +2 bonus) costs 3 XP.")
    print("Master (Rank 2, +5 bonus) costs 6 XP (requires Trained first).")
    
    allowed_moves = style["Strikes"] + style["Blocks"] + style["Throws"]
    masteries = {}

    while xp >= 3:
        print(f"\nRemaining XP: {xp} XP")
        print("Available moves to upgrade:")
        choices = []
        for idx, move in enumerate(allowed_moves, 1):
            curr_rank = masteries.get(move, 0)
            status = "Untrained (Rank 0)"
            if curr_rank == 1:
                status = "Trained (Rank 1)"
            elif curr_rank == 2:
                status = "Mastered (Rank 2)"
            
            cost_text = ""
            if curr_rank == 0:
                cost_text = " (Upgrade: 3 XP)"
            elif curr_rank == 1:
                cost_text = " (Upgrade: 6 XP)"
            
            print(f"  {idx}. {move.title()} [{status}]{cost_text}")
        print("  0. Finish & Save Character")

        try:
            m_choice = int(input(f"\nSelect move to upgrade (0-{len(allowed_moves)}): "))
            if m_choice == 0:
                break
            if 1 <= m_choice <= len(allowed_moves):
                move = allowed_moves[m_choice - 1]
                curr_rank = masteries.get(move, 0)
                
                if curr_rank == 0:
                    masteries[move] = 1
                    xp -= 3
                    print(f"-> Trained {move.title()}!")
                elif curr_rank == 1:
                    if xp >= 6:
                        masteries[move] = 2
                        xp -= 6
                        print(f"-> Mastered {move.title()}!")
                    else:
                        print("Not enough XP to Master this move (requires 6 XP).")
                else:
                    print("This move is already fully Mastered!")
        except ValueError:
            print("Invalid input.")

    # Save character sheet
    sheet_content = format_character_sheet(name, style_name, attrs, masteries, xp)
    print_header("Fighter Created Successfully!")
    print(sheet_content)
    
    if should_write:
        filename = f"{name.replace(' ', '_').lower()}_sheet.md"
        with open(filename, "w") as f:
            f.write(sheet_content)
        print(f"\nCharacter sheet saved to: {os.path.abspath(filename)}")

def main():
    should_write = "-w" in sys.argv or "--write" in sys.argv
    args = [a for a in sys.argv if a not in ["-w", "--write"]]

    if len(args) > 1:
        arg = args[1]
        if arg in ["--random", "-r"]:
            name, style_name, arch_name, attrs, masteries, xp = generate_random_character()
            sheet_content = format_character_sheet(name, style_name, attrs, masteries, xp, arch_name)
            print_header("Random Fighter Generated")
            print(sheet_content)
            
            if should_write:
                filename = f"{name.replace(' ', '_').lower()}_sheet.md"
                with open(filename, "w") as f:
                    f.write(sheet_content)
                print(f"\nSaved to: {os.path.abspath(filename)}")
        elif arg in ["--help", "-h"]:
            print("Saturday Night Street Fight — Character Generator")
            print("Usage:")
            print("  ./pc_generator.py          : Launch interactive character builder")
            print("  ./pc_generator.py --random : Generate a random, fully valid character sheet")
            print("  ./pc_generator.py -r       : Generate a random, fully valid character sheet")
            print("  Options:")
            print("    -w, --write              : Save the character sheet to a Markdown file")
            print("    -h, --help               : Show this help menu")
        else:
            print(f"Unknown argument: {arg}")
            print("Run with --help or -h to see options.")
    else:
        interactive_generation(should_write=should_write)

if __name__ == "__main__":
    main()
