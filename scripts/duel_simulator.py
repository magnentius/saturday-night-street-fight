#!/usr/bin/env python3
import sys
import os
import random
import time

# Add current directory to path just in case
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pc_generator import STYLES, ATTRIBUTES, generate_random_character, format_character_sheet
from npc_generator import generate_punk, generate_thug, generate_boss

# ANSI Color codes for premium terminal look
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

# Global logging system
log_lines = []

def log_print(text="", color=""):
    # Strip ANSI color codes for raw logging
    clean_text = text
    for ansi in [C_RED, C_GREEN, C_YELLOW, C_BLUE, C_MAGENTA, C_CYAN, C_WHITE, C_RESET, C_BOLD]:
        clean_text = clean_text.replace(ansi, "")
    log_lines.append(clean_text)
    print(color + text + C_RESET)

def print_banner(text, color=C_BOLD + C_YELLOW):
    log_print("=" * 70, color)
    log_print(f" {text.upper()} ".center(70, "="), color)
    log_print("=" * 70, color)

class Combatant:
    def __init__(self, name, tier, attrs, masteries, style_name=None):
        self.name = name
        self.tier = tier
        self.style_name = style_name
        
        # Max/Current Attributes
        self.max_attrs = dict(attrs)
        self.attrs = dict(attrs)
        
        # Masteries: move name -> rank (1 = Trained (+2), 2 = Mastered (+5))
        self.masteries = dict(masteries)
        
        # Status Conditions
        self.prone = False
        self.pinned = False
        self.staggered = False
        self.stunned = False
        self.shaken = False
        self.hobbled = 0   # 0 = normal, 1 = Hobbled (-1), 2 = Muay Thai Hobbled (-2)
        self.winded = False # Winded (-1 Stamina)
        
        # Ranges: "striking" or "clinch"
        self.range = "striking"

    def is_defeated(self):
        return (self.attrs["timing"] <= 0 or 
                self.attrs["posture"] <= 0 or 
                self.attrs["footwork"] <= 0 or 
                self.attrs["stamina"] <= 0)

    def print_status(self):
        # Format attributes
        attr_strs = []
        for a in ATTRIBUTES:
            val = self.attrs[a]
            max_val = self.max_attrs[a]
            attr_strs.append(f"{a[0].upper()}:{val}/{max_val}")
            
        status_line = f"  {self.name} [{' '.join(attr_strs)}]"
        
        # Active conditions
        conds = []
        if self.prone: conds.append("PRONE")
        if self.pinned: conds.append("PINNED")
        if self.staggered: conds.append("STAGGERED")
        if self.stunned: conds.append("STUNNED")
        if self.shaken: conds.append("SHAKEN")
        if self.hobbled > 0: conds.append(f"HOBBLED (-{self.hobbled})")
        if self.winded: conds.append("WINDED (-1)")
        
        if conds:
            status_line += f" Conds: {', '.join(conds)}"
        log_print(status_line)

    def select_action(self, read_opponent_color=None, opponent_down=False):
        """
        AI Action Choice logic.
        If read_opponent_color is provided (e.g. 'red', 'white', or 'black'), select the counter card.
        Otherwise, roll based on Style priorities and active conditions.
        """
        if self.stunned:
            choices = ["block"]
            sub = "high guard" if random.random() < 0.5 else "low guard"
            if self.style_name and "low guard" not in STYLES[self.style_name]["Blocks"]:
                sub = "high guard"
            return "block", sub

        if read_opponent_color:
            if read_opponent_color == "red":
                color = "block"
            elif read_opponent_color == "white":
                color = "throw"
            else:
                color = "strike"
            
            sub = self._pick_subaction(color, opponent_down)
            return color, sub

        weights = {"strike": 0.34, "block": 0.33, "throw": 0.33}
        if self.style_name == "Boxing":
            weights = {"strike": 0.5, "block": 0.4, "throw": 0.1}
        elif self.style_name == "Muay Thai":
            weights = {"strike": 0.6, "block": 0.3, "throw": 0.1}
        elif self.style_name == "Judo":
            if opponent_down:
                weights = {"strike": 0.6, "block": 0.3, "throw": 0.1}
            else:
                weights = {"strike": 0.1, "block": 0.4, "throw": 0.5}
        elif self.style_name == "Wrestling":
            if opponent_down:
                weights = {"strike": 0.7, "block": 0.2, "throw": 0.1}
            else:
                weights = {"strike": 0.3, "block": 0.3, "throw": 0.4}
        elif self.style_name == "Taekwondo":
            weights = {"strike": 0.6, "block": 0.4, "throw": 0.0}

        if self.prone:
            weights["strike"] = 0.0
            total = weights["block"] + weights["throw"]
            if total > 0:
                weights["block"] /= total
                weights["throw"] /= total
            else:
                weights["block"] = 1.0

        r = random.random()
        if r < weights.get("strike", 0):
            color = "strike"
        elif r < weights.get("strike", 0) + weights.get("block", 0):
            color = "block"
        else:
            color = "throw"

        sub = self._pick_subaction(color, opponent_down)
        return color, sub

    def _pick_subaction(self, color, opponent_down=False):
        if not self.style_name:
            if color == "strike": return "jab"
            if color == "block": return "high guard"
            return "clinch"
            
        style = STYLES[self.style_name]
        
        if self.prone:
            if color == "block":
                return "stand up" if random.random() < 0.6 else "high guard"
            if color == "throw":
                return "clinch"
        
        if color == "strike":
            moves = list(style["Strikes"])
            if not opponent_down and "ground & pound" in moves:
                moves.remove("ground & pound")
                
            favored = [m for m in moves if self.masteries.get(m, 0) > 0]
            if self.max_attrs["cool"] >= 3:
                moves.append("taunt")
                if self.masteries.get("taunt", 0) > 0:
                    favored.append("taunt")
            if favored and random.random() < 0.7:
                return random.choice(favored)
            return random.choice(moves) if moves else "jab"
            
        elif color == "block":
            moves = style["Blocks"]
            favored = [m for m in moves if self.masteries.get(m, 0) > 0]
            if favored and random.random() < 0.7:
                return random.choice(favored)
            return random.choice(moves) if moves else "high guard"
            
        else: # throw
            moves = style["Throws"]
            if not moves: return "clinch"
            favored = [m for m in moves if self.masteries.get(m, 0) > 0]
            if favored and random.random() < 0.7:
                return random.choice(favored)
            return random.choice(moves)

    def roll_dice(self, num_dice, keep_highest=True):
        rolls = [random.randint(1, 10) for _ in range(num_dice)]
        rolls.sort()
        if keep_highest and num_dice > 2:
            return sum(rolls[-2:])
        elif not keep_highest and num_dice > 2:
            return sum(rolls[:2])
        return sum(rolls)

    def calculate_check(self, action, subaction, rps_advantage):
        attr_name = "timing"
        
        if subaction in ["jab", "cross", "parry", "clinch"]:
            attr_name = "timing"
        elif subaction in ["high kick", "body kick", "push kick", "high guard", "low guard"]:
            attr_name = "stamina"
        elif subaction in ["low kick", "trip", "dodge", "stand up"]:
            attr_name = "footwork"
        elif subaction in ["hip throw", "takedown", "dirty punch", "ground & pound"]:
            attr_name = "posture"
        elif subaction == "taunt":
            attr_name = "cool"

        attr_val = self.attrs[attr_name]
        
        mastery_rank = self.masteries.get(subaction, 0)
        mastery_bonus = 0
        if mastery_rank == 1:
            mastery_bonus = 2
        elif mastery_rank == 2:
            mastery_bonus = 5
            
        num_dice = 2
        if rps_advantage:
            num_dice = 3
            
        keep_highest = True
        if self.prone or self.pinned or self.staggered or (self.stunned and action == "block"):
            keep_highest = False
            if num_dice == 2:
                num_dice = 3

        dice_sum = self.roll_dice(num_dice, keep_highest=keep_highest)
        
        flat_mod = attr_val + mastery_bonus
        
        temp_penalty = 0
        if attr_name == "footwork" and self.hobbled > 0:
            temp_penalty += self.hobbled
        if attr_name == "stamina" and self.winded:
            temp_penalty += 1
        if self.shaken and attr_name == "timing":
            temp_penalty += 2
            
        flat_mod -= temp_penalty
        if flat_mod > 10:
            flat_mod = 10
        
        total = dice_sum + flat_mod
        
        adv_text = "ADV" if rps_advantage else "Normal"
        if not keep_highest:
            adv_text = "DISADV"
            
        roll_log = f"{total} ({dice_sum} on dice + {attr_val} {attr_name.upper()} + {mastery_bonus} Mastery"
        if temp_penalty > 0:
            roll_log += f" - {temp_penalty} Status"
        roll_log += f", {adv_text})"
        
        return total, roll_log, attr_name

def run_fight(p1, p2):
    global log_lines
    log_lines = []
    
    # Initialize metrics structure
    metrics = {
        "rounds": 0,
        "clashes": 0,
        "p1": {
            "name": p1.name,
            "style": p1.style_name or "Brawler",
            "strikes": 0,
            "blocks": 0,
            "throws": 0,
            "damage_dealt": {"timing": 0, "posture": 0, "footwork": 0, "stamina": 0, "cool": 0},
            "damage_taken": {"timing": 0, "posture": 0, "footwork": 0, "stamina": 0, "cool": 0},
            "reads_won": 0,
            "crits": 0
        },
        "p2": {
            "name": p2.name,
            "style": p2.style_name or "Brawler",
            "strikes": 0,
            "blocks": 0,
            "throws": 0,
            "damage_dealt": {"timing": 0, "posture": 0, "footwork": 0, "stamina": 0, "cool": 0},
            "damage_taken": {"timing": 0, "posture": 0, "footwork": 0, "stamina": 0, "cool": 0},
            "reads_won": 0,
            "crits": 0
        }
    }

    print_banner("The Street Duel Begins")
    log_print(f"{C_BOLD}{p1.name}{C_RESET} ({p1.style_name or 'Brawler'}) VS {C_BOLD}{p2.name}{C_RESET} ({p2.style_name or 'Brawler'})\n")
    
    round_count = 0
    while not p1.is_defeated() and not p2.is_defeated():
        round_count += 1
        metrics["rounds"] = round_count
        
        log_print(f"\n{C_BOLD}{C_CYAN}=== ROUND {round_count} ==={C_RESET}")
        p1.print_status()
        p2.print_status()
        log_print("-" * 55)
        
        # --- PHASE 1: READING THE STANCE (Telegraphing) ---
        p1_read_success = False
        p2_read_success = False
        
        if not p1.stunned and not p2.stunned:
            p1_roll = p1.roll_dice(2) + max(p1.attrs["timing"], p1.attrs["cool"])
            p2_roll = p2.roll_dice(2) + max(p2.attrs["timing"], p2.attrs["cool"])
            
            if p1_roll > p2_roll:
                p1_read_success = True
                metrics["p1"]["reads_won"] += 1
                log_print(f"-> {C_GREEN}{p1.name} reads {p2.name}'s stance!{C_RESET} (Roll: {p1_roll} vs {p2_roll})")
            elif p2_roll > p1_roll:
                p2_read_success = True
                metrics["p2"]["reads_won"] += 1
                log_print(f"-> {C_GREEN}{p2.name} reads {p1.name}'s stance!{C_RESET} (Roll: {p2_roll} vs {p1_roll})")
        
        # --- PHASE 2: COMMIT & REVEAL ---
        p1_color, p1_sub = None, None
        p2_color, p2_sub = None, None
        
        p1_down = p1.prone or p1.pinned
        p2_down = p2.prone or p2.pinned

        if p1_read_success:
            p2_color, p2_sub = p2.select_action(opponent_down=p1_down)
            p1_color, p1_sub = p1.select_action(read_opponent_color=p2_color, opponent_down=p2_down)
        elif p2_read_success:
            p1_color, p1_sub = p1.select_action(opponent_down=p2_down)
            p2_color, p2_sub = p2.select_action(read_opponent_color=p1_color, opponent_down=p1_down)
        else:
            p1_color, p1_sub = p1.select_action(opponent_down=p2_down)
            p2_color, p2_sub = p2.select_action(opponent_down=p1_down)

        # Track actions chosen
        metrics["p1"][f"{p1_color}s"] += 1
        metrics["p2"][f"{p2_color}s"] += 1

        # Display declarations
        log_print(f"  {p1.name} commits: {p1_color.upper()} ({p1_sub.upper()})")
        log_print(f"  {p2.name} commits: {p2_color.upper()} ({p2_sub.upper()})")
        log_print("-" * 55)

        # --- PHASE 3: RESOLVE RPS TRIANGLE ---
        p1_advantage = False
        p2_advantage = False
        
        if p1_color == "strike" and p2_color == "throw":
            p1_advantage = True
        elif p1_color == "throw" and p2_color == "block":
            p1_advantage = True
        elif p1_color == "block" and p2_color == "strike":
            p1_advantage = True
        elif p2_color == "strike" and p1_color == "throw":
            p2_advantage = True
        elif p2_color == "throw" and p1_color == "block":
            p2_advantage = True
        elif p2_color == "block" and p1_color == "strike":
            p2_advantage = True

        # --- PHASE 4: ROLL & RESOLVE ---
        p1_total, p1_log, p1_attr = p1.calculate_check(p1_color, p1_sub, p1_advantage)
        p2_total, p2_log, p2_attr = p2.calculate_check(p2_color, p2_sub, p2_advantage)
        
        log_print(f"  {p1.name} rolls: {p1_log}")
        log_print(f"  {p2.name} rolls: {p2_log}")
        
        # Reset one-turn conditions at start of check resolution
        p1.staggered = False
        p2.staggered = False
        
        p1.hobbled = 0
        p2.hobbled = 0
        p1.winded = False
        p2.winded = False

        winner, loser = None, None
        w_total, l_total = 0, 0
        w_color, l_color = "", ""
        w_sub, l_sub = "", ""
        
        if p1_total > p2_total:
            winner, loser = p1, p2
            w_total, l_total = p1_total, p2_total
            w_color, l_color = p1_color, p2_color
            w_sub, l_sub = p1_sub, p2_sub
            w_key, l_key = "p1", "p2"
        elif p2_total > p1_total:
            winner, loser = p2, p1
            w_total, l_total = p2_total, p1_total
            w_color, l_color = p2_color, p1_color
            w_sub, l_sub = p2_sub, p1_sub
            w_key, l_key = "p2", "p1"
        else:
            # TIE! Roll standoff or Clash rules
            metrics["clashes"] += 1
            log_print(f"\n{C_BOLD}{C_YELLOW}--> CLASH RESOLUTION (Tied rolls: {p1_total} vs {p2_total}){C_RESET}")
            if p1_color == "strike" and p2_color == "strike":
                log_print("  -> Both strikes hit simultaneously!")
                resolve_hit(p1, p1_sub, p2, 2, False, metrics, "p1", "p2")
                resolve_hit(p2, p2_sub, p1, 2, False, metrics, "p2", "p1")
            elif p1_color == "strike" and p2_color == "block":
                log_print(f"  -> {p2.name}'s block holds, but they are STAGGERED next turn.")
                p2.staggered = True
            elif p2_color == "strike" and p1_color == "block":
                log_print(f"  -> {p1.name}'s block holds, but they are STAGGERED next turn.")
                p1.staggered = True
            else:
                log_print("  -> Standoff! Fighters reset to neutral.")
            continue

        # Winner-take-all resolution
        margin = w_total - l_total
        crit = margin >= 5
        log_print(f"\n-> {C_GREEN}{C_BOLD}{winner.name} wins the exchange!{C_RESET} (Margin: {margin})")
        if crit:
            metrics[w_key]["crits"] += 1
            log_print(f"   {C_RED}{C_BOLD}*** CRITICAL HIT! ***{C_RESET}")
            
        # 1. Resolve Strike
        if w_color == "strike":
            base_dmg = 2
            if w_sub in ["uppercut", "high kick", "body kick"]:
                base_dmg = 3
            if w_sub == "taunt":
                base_dmg = 1
                
            if crit:
                base_dmg += 1
                
            if l_color == "block":
                # Block mitigation
                mitigation = 0
                if l_sub == "high guard":
                    mitigation = 2
                    if l_sub == "high guard" and winner.style_name == "Boxing" and w_sub in ["jab", "cross", "hook", "uppercut"]:
                        mitigation = 3
                elif l_sub == "low guard":
                    mitigation = 2
                    
                net_dmg = max(0, base_dmg - mitigation)
                log_print(f"   {loser.name} blocks with {l_sub} (mitigates {mitigation} damage). Net: {net_dmg}")
                if net_dmg > 0:
                    resolve_hit(winner, w_sub, loser, net_dmg, crit, metrics, w_key, l_key)
            else:
                resolve_hit(winner, w_sub, loser, base_dmg, crit, metrics, w_key, l_key)

        # 2. Resolve Block (Parry/Dodge)
        elif w_color == "block":
            log_print(f"   {winner.name} successfully defends using {w_sub}.")
            if w_sub == "parry" and winner.style_name == "Judo" and l_color == "strike":
                log_print(f"   {C_GREEN}[Judo Kuzushi]{C_RESET} {winner.name} parried a strike! Free throw attempt!")
                t_roll = winner.roll_dice(2) + winner.attrs["posture"]
                d_roll = loser.roll_dice(2) + loser.attrs["footwork"]
                if t_roll > d_roll:
                    log_print(f"   -> Sweep projection success! {loser.name} is thrown to the ground!")
                    loser.prone = True
                    loser.attrs["posture"] = max(0, loser.attrs["posture"] - 2)
                    metrics[w_key]["damage_dealt"]["posture"] += 2
                    metrics[l_key]["damage_taken"]["posture"] += 2
                else:
                    log_print("   -> Loser retains their footing.")
            elif w_sub == "dodge" and winner.style_name == "Boxing" and l_color == "strike":
                log_print(f"   {C_GREEN}[Boxing Slip & Counter]{C_RESET} {winner.name} dodged! Next strike has advantage.")
                
            if w_sub == "stand up" and winner.prone:
                log_print(f"   {winner.name} stands back up.")
                winner.prone = False

        # 3. Resolve Throw
        elif w_color == "throw":
            if w_sub == "clinch":
                log_print(f"   {winner.name} locks {loser.name} in a Clinch/Grab.")
                winner.range = "clinch"
                loser.range = "clinch"
            elif w_sub == "trip":
                log_print(f"   {winner.name} sweeps {loser.name}'s legs!")
                loser.prone = True
                dmg = 2
                if crit: dmg += 1
                loser.attrs["footwork"] = max(0, loser.attrs["footwork"] - dmg)
                metrics[w_key]["damage_dealt"]["footwork"] += dmg
                metrics[l_key]["damage_taken"]["footwork"] += dmg
                log_print(f"   {loser.name} takes {dmg} FOOTWORK damage.")
            elif w_sub == "hip throw":
                log_print(f"   {winner.name} throws {loser.name} over their shoulder!")
                loser.prone = True
                dmg = 3
                if crit: dmg += 1
                loser.attrs["posture"] = max(0, loser.attrs["posture"] - dmg)
                metrics[w_key]["damage_dealt"]["posture"] += dmg
                metrics[l_key]["damage_taken"]["posture"] += dmg
                log_print(f"   {loser.name} takes {dmg} POSTURE damage.")
                if crit:
                    log_print(f"   {loser.name} is STUNNED by the impact!")
                    loser.stunned = True
            elif w_sub == "takedown":
                log_print(f"   {winner.name} drives through with a Double Leg Takedown!")
                loser.prone = True
                dmg = 3
                if crit: dmg += 1
                loser.attrs["posture"] = max(0, loser.attrs["posture"] - dmg)
                metrics[w_key]["damage_dealt"]["posture"] += dmg
                metrics[l_key]["damage_taken"]["posture"] += dmg
                log_print(f"   {loser.name} takes {dmg} POSTURE damage.")
                if winner.style_name == "Wrestling":
                    log_print(f"   {C_GREEN}[Wrestling Ground Control]{C_RESET} opponent is PINNED on the canvas!")
                    loser.pinned = True

        # Clear stun duration
        if p1.stunned and winner == p1: p1.stunned = False
        if p2.stunned and winner == p2: p2.stunned = False
        
        time.sleep(0.5)

    # --- MATCH OVER ---
    print_banner("Fight Over")
    
    match_result = ""
    if p1.is_defeated() and p2.is_defeated():
        log_print(f"{C_RED}{C_BOLD}DOUBLE TKO! Both fighters collapsed onto the concrete floor!{C_RESET}")
        match_result = "Double TKO"
    elif p1.is_defeated():
        log_print(f"{C_GREEN}{C_BOLD}{p2.name} WINS the duel!{C_RESET} {p1.name} was Knocked Out.")
        match_result = f"{p2.name} wins via TKO"
    else:
        log_print(f"{C_GREEN}{C_BOLD}{p1.name} WINS the duel!{C_RESET} {p2.name} was Knocked Out.")
        match_result = f"{p1.name} wins via TKO"

    # Write report and print final metrics
    write_metrics_report(p1, p2, metrics, match_result)

def resolve_hit(attacker, move, target, damage, crit, metrics, att_key, def_key):
    target_attr = "timing"
    if move in ["jab", "cross", "high kick", "dirty punch"]:
        target_attr = "timing"
    elif move == "hook":
        target_attr = "stamina" if target.attrs["stamina"] <= target.attrs["posture"] else "posture"
    elif move == "uppercut":
        target_attr = "posture"
    elif move in ["body kick", "push kick"]:
        target_attr = "stamina"
    elif move == "low kick":
        target_attr = "footwork"
    elif move == "taunt":
        target_attr = "cool"
    elif move == "ground & pound":
        target_attr = "posture" if target.attrs["posture"] <= target.attrs["stamina"] else "stamina"

    # Deal damage
    target.attrs[target_attr] = max(0, target.attrs[target_attr] - damage)
    metrics[att_key]["damage_dealt"][target_attr] += damage
    metrics[def_key]["damage_taken"][target_attr] += damage
    
    log_print(f"   {attacker.name}'s {move.upper()} hits {target.name} for {C_RED}{damage} {target_attr.upper()} damage!{C_RESET} (New: {target.attrs[target_attr]})")
    
    if move == "low kick":
        penalty = 2 if attacker.style_name == "Muay Thai" else 1
        target.hobbled = penalty
        log_print(f"   -> {target.name} is HOBBLED (-{penalty} Footwork rolls next round)")
    elif move == "body kick":
        target.winded = True
        log_print(f"   -> {target.name} is WINDED (-1 Stamina rolls next round)")
    elif move == "taunt":
        if target.attrs["cool"] <= 0:
            target.shaken = True
            log_print(f"   -> {target.name} is SHAKEN! (Cool reduced to 0. Timings suffer -2; perks suspended)")

    if crit and move == "high kick":
        log_print(f"   -> {target.name} is STUNNED by the massive blow!")
        target.stunned = True

def write_metrics_report(p1, p2, metrics, match_result):
    p1_stats = metrics["p1"]
    p2_stats = metrics["p2"]
    
    # Generate terminal report summary
    print_banner("Combat Metrics Summary", C_BOLD + C_CYAN)
    log_print(f"Total Rounds Played: {metrics['rounds']}")
    log_print(f"Total Clashes:        {metrics['clashes']}")
    log_print(f"Match Result:         {match_result}\n")
    
    log_print(f"{C_BOLD}Fighter: {p1.name} ({p1.style_name or 'Brawler'}){C_RESET}")
    log_print(f"  Actions:  {p1_stats['strikes']} Strikes | {p1_stats['blocks']} Blocks | {p1_stats['throws']} Throws")
    log_print(f"  Reads:    {p1_stats['reads_won']} Stance Reads Won")
    log_print(f"  Crits:    {p1_stats['crits']} Critical Hits Landed")
    log_print(f"  Damage Dealt: T:{p1_stats['damage_dealt']['timing']} P:{p1_stats['damage_dealt']['posture']} F:{p1_stats['damage_dealt']['footwork']} S:{p1_stats['damage_dealt']['stamina']} C:{p1_stats['damage_dealt']['cool']}")
    
    log_print(f"\n{C_BOLD}Fighter: {p2.name} ({p2.style_name or 'Brawler'}){C_RESET}")
    log_print(f"  Actions:  {p2_stats['strikes']} Strikes | {p2_stats['blocks']} Blocks | {p2_stats['throws']} Throws")
    log_print(f"  Reads:    {p2_stats['reads_won']} Stance Reads Won")
    log_print(f"  Crits:    {p2_stats['crits']} Critical Hits Landed")
    log_print(f"  Damage Dealt: T:{p2_stats['damage_dealt']['timing']} P:{p2_stats['damage_dealt']['posture']} F:{p2_stats['damage_dealt']['footwork']} S:{p2_stats['damage_dealt']['stamina']} C:{p2_stats['damage_dealt']['cool']}")
    
    # Generate Markdown File Content
    md = []
    md.append(f"# Saturday Night Street Fight — Combat Report")
    md.append(f"**Date**: 1970s Brooklyn Street Grid")
    md.append(f"**Fighter 1**: {p1.name} ({p1.style_name or 'Brawler'})")
    md.append(f"**Fighter 2**: {p2.name} ({p2.style_name or 'Brawler'})")
    md.append(f"**Result**: {match_result}")
    md.append(f"**Rounds**: {metrics['rounds']} | **Clashes**: {metrics['clashes']}\n")
    
    md.append("## Combat Metrics Summary\n")
    md.append("| Metric | " + f"{p1.name} ({p1.style_name or 'Brawler'})" + " | " + f"{p2.name} ({p2.style_name or 'Brawler'})" + " |")
    md.append("| :--- | :--- | :--- |")
    md.append(f"| **Strikes Declared** | {p1_stats['strikes']} | {p2_stats['strikes']} |")
    md.append(f"| **Blocks Declared** | {p1_stats['blocks']} | {p2_stats['blocks']} |")
    md.append(f"| **Throws Declared** | {p1_stats['throws']} | {p2_stats['throws']} |")
    md.append(f"| **Stance Reads Won** | {p1_stats['reads_won']} | {p2_stats['reads_won']} |")
    md.append(f"| **Critical Hits Landed** | {p1_stats['crits']} | {p2_stats['crits']} |")
    md.append(f"| **Timing Damage Dealt** | {p1_stats['damage_dealt']['timing']} | {p2_stats['damage_dealt']['timing']} |")
    md.append(f"| **Posture Damage Dealt** | {p1_stats['damage_dealt']['posture']} | {p2_stats['damage_dealt']['posture']} |")
    md.append(f"| **Footwork Damage Dealt** | {p1_stats['damage_dealt']['footwork']} | {p2_stats['damage_dealt']['footwork']} |")
    md.append(f"| **Stamina Damage Dealt** | {p1_stats['damage_dealt']['stamina']} | {p2_stats['damage_dealt']['stamina']} |")
    md.append(f"| **Cool Damage Dealt** | {p1_stats['damage_dealt']['cool']} | {p2_stats['damage_dealt']['cool']} |")
    md.append("\n---\n")
    
    md.append("## Round-by-Round Playlog\n")
    for line in log_lines:
        md.append(line)
        
    report_content = "\n".join(md)
    filename = "duel_report.md"
    
    # Save inside scripts folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, filename)
    
    with open(report_path, "w") as f:
        f.write(report_content)
        
    print(f"\nDetailed markdown combat log written to: {report_path}")

def main():
    print_banner("1v1 Street Fight Duel Simulator")
    
    # Option to select Tiers
    print("Select Fighter 1 (Player Character):")
    print("  1. Generate random PC")
    print("  2. Build custom PC (Launch interactive generator)")
    try:
        p1_choice = input("Select option (1-2, default 1): ").strip()
    except (KeyboardInterrupt, SystemExit):
        print("\nExiting.")
        sys.exit(0)
        
    if p1_choice == "2":
        print("Launching interactive PC Builder...")
        from pc_generator import interactive_generation
        interactive_generation()
        print("\nNow let's load that character or roll a random brawler for the duel...")
        name, style_name, arch_name, attrs, masteries, xp = generate_random_character()
    else:
        name, style_name, arch_name, attrs, masteries, xp = generate_random_character()

    p1 = Combatant(name, "PC", attrs, masteries, style_name)

    print("\nSelect Opponent (NPC):")
    print("  1. Tier 1 Punk / Lookout")
    print("  2. Tier 2 Standard Thug")
    print("  3. Tier 3 Syndicate Boss")
    try:
        opp_choice = input("Select opponent tier (1-3, default 2): ").strip()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

    if opp_choice == "1":
        npc_data = generate_punk()
    elif opp_choice == "3":
        npc_data = generate_boss()
    else:
        npc_data = generate_thug()

    p2 = Combatant(
        npc_data["name"].split(" (")[0].replace("'", ""), 
        npc_data["tier"], 
        npc_data["attrs"], 
        npc_data["masteries"], 
        npc_data.get("style", None)
    )

    run_fight(p1, p2)

if __name__ == "__main__":
    main()
