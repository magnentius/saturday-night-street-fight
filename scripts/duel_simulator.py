#!/usr/bin/env python3
import sys
import os
import random
import time

# Add current directory to path just in case
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pc_generator import STYLES, ATTRIBUTES, generate_random_character, format_character_sheet
from npc_generator import generate_punk, generate_thug, generate_boss, generate_warlord, generate_overlord

# ANSI Color code constants for terminal output
C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_RED    = "\033[31m"
C_GREEN  = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE   = "\033[34m"
C_CYAN   = "\033[36m"

# Global logging system
log_lines = []

def log_print(text="", color=""):
    # Strip ANSI color codes for raw logging
    clean_text = text
    for ansi in [C_RED, C_GREEN, C_YELLOW, C_BLUE, C_CYAN, C_RESET, C_BOLD]:
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
        
        # Style perk tracking flags
        self.kiai_used = False
        self.slip_adv = False
        self.last_round_struck = False
        
        # Ranges: "outside", "striking", or "grapple"
        self.range = "striking"

    def is_defeated(self):
        return (self.attrs["reaction"] <= 0 or 
                self.attrs["power"] <= 0 or 
                self.attrs["agility"] <= 0 or 
                self.attrs["stamina"] <= 0 or
                self.attrs["cool"] <= 0)

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

    def select_action(self, read_opponent_color=None, eliminate_opponent_color=None, opponent_down=False):
        """
        AI Action Choice logic.
        If read_opponent_color is provided (Margin 7+ Perfect Read), select the hard counter card.
        If eliminate_opponent_color is provided (Margin 4-6 Partial Tell), zero out ineffective stances.
        Otherwise, roll based on Style priorities and active conditions.
        """
        if self.stunned:
            choices = ["block"]
            sub = "high guard" if random.random() < 0.5 else "low guard"
            style_key = self.style_name.split(" / ")[0] if self.style_name and " / " in self.style_name else self.style_name
            if style_key and "low guard" not in STYLES[style_key]["Blocks"]:
                sub = "high guard"
            return "block", sub

        if read_opponent_color:
            if read_opponent_color == "red" or read_opponent_color == "strike":
                color = "block"
            elif read_opponent_color == "white" or read_opponent_color == "block":
                color = "throw"
            else:
                color = "strike"
            
            sub = self._pick_technique(color, opponent_down)
            return color, sub

        weights = {"strike": 0.34, "block": 0.33, "throw": 0.33}
        if self.style_name == "Boxing":
            weights = {"strike": 0.5, "block": 0.4, "throw": 0.1}
        elif self.style_name == "Muay Thai":
            weights = {"strike": 0.6, "block": 0.3, "throw": 0.1}
        elif self.style_name == "Judo":
            if opponent_down:
                weights = {"strike": 0.45, "block": 0.1, "throw": 0.45}
            else:
                weights = {"strike": 0.1, "block": 0.4, "throw": 0.5}
        elif self.style_name == "Wrestling":
            if opponent_down:
                weights = {"strike": 0.45, "block": 0.1, "throw": 0.45}
            else:
                weights = {"strike": 0.3, "block": 0.3, "throw": 0.4}
        elif self.style_name == "Karate":
            weights = {"strike": 0.5, "block": 0.4, "throw": 0.1}
        elif self.style_name == "Kung Fu":
            weights = {"strike": 0.5, "block": 0.4, "throw": 0.1}
        elif self.style_name == "Taekwondo":
            weights = {"strike": 0.6, "block": 0.4, "throw": 0.0}

        # Partial Tell adjustment: if opponent is NOT taking a color, adjust weights
        if eliminate_opponent_color:
            if eliminate_opponent_color == "block":
                # Opponent is striking or throwing -> favor block (beats strike) or strike (beats throw)
                weights["throw"] = 0.0
            elif eliminate_opponent_color == "strike":
                # Opponent is blocking or throwing -> favor throw (beats block) or strike (beats throw)
                weights["block"] = 0.0
            elif eliminate_opponent_color == "throw":
                # Opponent is striking or blocking -> favor block (beats strike) or throw (beats block)
                weights["strike"] = 0.0
            
            total_w = sum(weights.values())
            if total_w > 0:
                for k in weights: weights[k] /= total_w

        if self.prone or self.pinned:
            weights["strike"] = 0.0
            if self.pinned:
                if self.attrs["agility"] >= self.attrs["power"]:
                    weights["block"], weights["throw"] = 0.6, 0.4
                else:
                    weights["block"], weights["throw"] = 0.4, 0.6
            else:
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

        sub = self._pick_technique(color, opponent_down)
        return color, sub

    def _pick_technique(self, color, opponent_down=False):
        if not self.style_name:
            if color == "strike": return "jab"
            if color == "block": return "high guard"
            return "clinch"
            
        style_key = self.style_name.split(" / ")[0] if " / " in self.style_name else self.style_name
        style = STYLES[style_key]
        
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
            moves = list(style["Throws"])
            if not opponent_down and "submission hold" in moves:
                moves.remove("submission hold")
            if not moves: return "clinch"
            favored = [m for m in moves if self.masteries.get(m, 0) > 0]
            if favored and random.random() < 0.7:
                return random.choice(favored)
            return random.choice(moves)

    def roll_dice(self, num_dice, keep_highest=True):
        rolls = [random.randint(1, 10) for _ in range(num_dice)]
        rolls.sort()
        if keep_highest and num_dice > 2:
            kept = rolls[-2:]
        elif not keep_highest and num_dice > 2:
            kept = rolls[:2]
        else:
            kept = rolls
        is_nat20 = kept.count(10) >= 2
        return sum(kept), is_nat20

    def calculate_check(self, action, technique, rps_advantage, opponent_action=None):
        attr_name = "reaction"
        
        if technique in ["jab", "cross", "hook", "parry", "clinch"]:
            attr_name = "reaction"
        elif technique in ["body kick", "high kick"]:
            attr_name = "stamina"
        elif technique in ["low kick", "push kick", "trip", "dodge", "stand up"]:
            attr_name = "agility"
        elif technique in ["uppercut", "high guard", "low guard", "hip throw", "takedown", "ground & pound", "submission hold"]:
            attr_name = "power"
        elif technique == "taunt":
            attr_name = "cool"

        attr_val = self.attrs[attr_name]
        
        mastery_rank = self.masteries.get(technique, 0)
        mastery_bonus = 0
        if mastery_rank == 1:
            mastery_bonus = 3
        elif mastery_rank == 2:
            mastery_bonus = 5
            
        num_dice = 2
        has_slip_adv = (action == "strike" and getattr(self, "slip_adv", False))
        if rps_advantage or has_slip_adv:
            num_dice = 3
            if has_slip_adv:
                self.slip_adv = False
            
        keep_highest = True
        is_escape = (self.prone and technique == "stand up") or (self.pinned and action in ["block", "throw"])
        has_disadv = (
            ((self.prone or self.pinned) and not is_escape) or 
            self.staggered or 
            (self.hobbled > 0 and attr_name == "agility") or 
            (self.winded and attr_name in ["stamina", "power"]) or 
            (self.shaken and attr_name == "reaction")
        )
        if has_disadv:
            keep_highest = False
            if num_dice == 2:
                num_dice = 3

        dice_sum, is_nat20 = self.roll_dice(num_dice, keep_highest=keep_highest)
        
        flat_mod = attr_val + mastery_bonus
        
        # Kung Fu Chain Strike: +2 bonus if landed a strike last round
        chain_bonus = 0
        if self.style_name == "Kung Fu" and self.last_round_struck and action == "strike":
            chain_bonus = 2
            flat_mod += chain_bonus
            
        # Wrestling Shooter: +2 bonus when shooting a Double Leg Takedown against a Strike
        shooter_bonus = 0
        if self.style_name == "Wrestling" and technique == "takedown" and opponent_action == "strike":
            shooter_bonus = 2
            flat_mod += shooter_bonus
            
        if flat_mod > 10:
            flat_mod = 10
        
        total = dice_sum + flat_mod
        
        adv_text = "ADV" if rps_advantage else "Normal"
        if not keep_highest:
            adv_text = "DISADV"
            
        roll_log = f"{total} ({dice_sum} on dice + {attr_val} {attr_name.upper()} + {mastery_bonus} Mastery"
        if chain_bonus > 0:
            roll_log += f" + {chain_bonus} Chain Strike"
        if shooter_bonus > 0:
            roll_log += f" + {shooter_bonus} Shooter"
        roll_log += f", {adv_text})"
        if is_nat20:
            roll_log += f" [NATURAL 20!]"
        
        return total, roll_log, attr_name, is_nat20

def run_fight(p1, p2, should_write=False):
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
            "damage_dealt": {"reaction": 0, "power": 0, "agility": 0, "stamina": 0, "cool": 0},
            "damage_taken": {"reaction": 0, "power": 0, "agility": 0, "stamina": 0, "cool": 0},
            "reads_won": 0,
            "crits": 0
        },
        "p2": {
            "name": p2.name,
            "style": p2.style_name or "Brawler",
            "strikes": 0,
            "blocks": 0,
            "throws": 0,
            "damage_dealt": {"reaction": 0, "power": 0, "agility": 0, "stamina": 0, "cool": 0},
            "damage_taken": {"reaction": 0, "power": 0, "agility": 0, "stamina": 0, "cool": 0},
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
        p1_read_level = "none" # "none", "partial", or "perfect"
        p2_read_level = "none"
        
        if not p1.stunned and not p2.stunned:
            p1_roll = p1.roll_dice(2)[0] + max(p1.attrs["reaction"], p1.attrs["cool"])
            p2_roll = p2.roll_dice(2)[0] + max(p2.attrs["reaction"], p2.attrs["cool"])
            
            diff = p1_roll - p2_roll
            margin = abs(diff)
            
            if diff >= 4:
                metrics["p1"]["reads_won"] += 1
                if margin >= 7:
                    p1_read_level = "perfect"
                    log_print(f"-> {C_GREEN}{p1.name} gets a PERFECT READ on {p2.name}'s stance!{C_RESET} (Roll: {p1_roll} vs {p2_roll}, Margin: {margin})")
                else:
                    p1_read_level = "partial"
                    log_print(f"-> {C_GREEN}{p1.name} spots a PARTIAL TELL on {p2.name}'s stance!{C_RESET} (Roll: {p1_roll} vs {p2_roll}, Margin: {margin})")
            elif diff <= -4:
                metrics["p2"]["reads_won"] += 1
                if margin >= 7:
                    p2_read_level = "perfect"
                    log_print(f"-> {C_GREEN}{p2.name} gets a PERFECT READ on {p1.name}'s stance!{C_RESET} (Roll: {p2_roll} vs {p1_roll}, Margin: {margin})")
                else:
                    p2_read_level = "partial"
                    log_print(f"-> {C_GREEN}{p2.name} spots a PARTIAL TELL on {p1.name}'s stance!{C_RESET} (Roll: {p2_roll} vs {p1_roll}, Margin: {margin})")
            else:
                log_print(f"-> Body language unreadable (Roll: {p1_roll} vs {p2_roll}, Margin: {margin})")
        
        # --- PHASE 2: COMMIT & REVEAL ---
        p1_color, p1_sub = None, None
        p2_color, p2_sub = None, None
        
        p1_down = p1.prone or p1.pinned
        p2_down = p2.prone or p2.pinned

        if p1_read_level == "perfect":
            p2_color, p2_sub = p2.select_action(opponent_down=p1_down)
            p1_color, p1_sub = p1.select_action(read_opponent_color=p2_color, opponent_down=p2_down)
        elif p2_read_level == "perfect":
            p1_color, p1_sub = p1.select_action(opponent_down=p2_down)
            p2_color, p2_sub = p2.select_action(read_opponent_color=p1_color, opponent_down=p1_down)
        elif p1_read_level == "partial":
            p2_color, p2_sub = p2.select_action(opponent_down=p1_down)
            other_colors = [c for c in ["strike", "block", "throw"] if c != p2_color]
            p1_elim = random.choice(other_colors)
            log_print(f"   -> {p1.name} deduces {p2.name} is NOT choosing {p1_elim.upper()}.")
            p1_color, p1_sub = p1.select_action(eliminate_opponent_color=p1_elim, opponent_down=p2_down)
        elif p2_read_level == "partial":
            p1_color, p1_sub = p1.select_action(opponent_down=p2_down)
            other_colors = [c for c in ["strike", "block", "throw"] if c != p1_color]
            p2_elim = random.choice(other_colors)
            log_print(f"   -> {p2.name} deduces {p1.name} is NOT choosing {p2_elim.upper()}.")
            p2_color, p2_sub = p2.select_action(eliminate_opponent_color=p2_elim, opponent_down=p1_down)
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

        # --- PHASE 3: ADVANTAGE CHECK ---
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
        p1_total, p1_log, p1_attr, p1_nat20 = p1.calculate_check(p1_color, p1_sub, p1_advantage, opponent_action=p2_color)
        p2_total, p2_log, p2_attr, p2_nat20 = p2.calculate_check(p2_color, p2_sub, p2_advantage, opponent_action=p1_color)
        
        log_print(f"  {p1.name} rolls: {p1_log}")
        log_print(f"  {p2.name} rolls: {p2_log}")
        
        # Reset one-turn conditions at start of check resolution
        p1.staggered = False
        p2.staggered = False
        
        p1.hobbled = 0
        p2.hobbled = 0
        p1.winded = False
        p2.winded = False
        
        # Track Kung Fu Chain Strike: record whether each fighter landed a strike this round
        p1_struck_this_round = False
        p2_struck_this_round = False

        # Apply Momentum Surge for Nat 20s
        for ftr, nat in [(p1, p1_nat20), (p2, p2_nat20)]:
            if nat:
                log_print(f"   {C_RED}{C_BOLD}*** OVERKILL! {ftr.name} ROLLED A NATURAL 20! ***{C_RESET}")
                if ftr.attrs["stamina"] < ftr.max_attrs["stamina"]:
                    ftr.attrs["stamina"] = min(ftr.max_attrs["stamina"], ftr.attrs["stamina"] + 1)
                    log_print(f"   -> Momentum Surge! {ftr.name} recovered +1 Stamina!")
                elif ftr.attrs["cool"] < ftr.max_attrs["cool"]:
                    ftr.attrs["cool"] = min(ftr.max_attrs["cool"], ftr.attrs["cool"] + 1)
                    log_print(f"   -> Momentum Surge! {ftr.name} recovered +1 Cool!")

        if p1_color == "strike" and p2_color == "strike":
            log_print(f"\n{C_BOLD}{C_YELLOW}--> STRIKE TRADE! Both fighters throw strikes!{C_RESET}")
            if p1_total >= p2_total:
                first, first_sub, first_tot, first_nat, first_key = p1, p1_sub, p1_total, p1_nat20, "p1"
                second, second_sub, second_tot, second_nat, second_key = p2, p2_sub, p2_total, p2_nat20, "p2"
            else:
                first, first_sub, first_tot, first_nat, first_key = p2, p2_sub, p2_total, p2_nat20, "p2"
                second, second_sub, second_tot, second_nat, second_key = p1, p1_sub, p1_total, p1_nat20, "p1"

            first_dmg = 1 if first_sub in ["jab", "taunt"] else (3 if first_sub in ["uppercut", "high kick", "body kick"] else 2)
            first_crit = first_nat or ((first_tot - second_tot) >= 5)
            if first_crit:
                first_dmg += 1
                # Karate Ikken Hissatsu: extra +1 on crits
                if first.style_name == "Karate":
                    first_dmg += 1
                    log_print(f"   {C_RED}[Karate Ikken Hissatsu]{C_RESET} Extra +1 damage on critical!")
                metrics[first_key]["crits"] += 1
                log_print(f"   {C_RED}{C_BOLD}*** {first.name} LANDS A CRITICAL STRIKE! ***{C_RESET}")

            resolve_hit(first, first_sub, second, first_dmg, first_crit, metrics, first_key, second_key)

            # Check if second fighter was KO'd before their strike lands
            if second.is_defeated():
                log_print(f"   -> {second.name} was knocked out before their strike could land!")
            else:
                second_dmg = 1 if second_sub in ["jab", "taunt"] else (3 if second_sub in ["uppercut", "high kick", "body kick"] else 2)
                second_crit = second_nat or ((second_tot - first_tot) >= 5)
                if second_crit:
                    second_dmg += 1
                    # Karate Ikken Hissatsu: extra +1 on crits
                    if second.style_name == "Karate":
                        second_dmg += 1
                        log_print(f"   {C_RED}[Karate Ikken Hissatsu]{C_RESET} Extra +1 damage on critical!")
                    metrics[second_key]["crits"] += 1
                    log_print(f"   {C_RED}{C_BOLD}*** {second.name} LANDS A CRITICAL STRIKE! ***{C_RESET}")

                resolve_hit(second, second_sub, first, second_dmg, second_crit, metrics, second_key, first_key)
            
            # Track strike landing for both fighters in a trade
            if first == p1:
                p1_struck_this_round = True
                if not second.is_defeated(): p2_struck_this_round = True
            else:
                p2_struck_this_round = True
                if not second.is_defeated(): p1_struck_this_round = True

            continue

        winner, loser = None, None
        w_total, l_total = 0, 0
        w_color, l_color = "", ""
        w_sub, l_sub = "", ""
        w_nat20 = False
        
        if p1_total > p2_total or p1_nat20:
            winner, loser = p1, p2
            w_total, l_total = p1_total, p2_total
            w_color, l_color = p1_color, p2_color
            w_sub, l_sub = p1_sub, p2_sub
            w_key, l_key = "p1", "p2"
            w_nat20 = p1_nat20
        elif p2_total > p1_total or p2_nat20:
            winner, loser = p2, p1
            w_total, l_total = p2_total, p1_total
            w_color, l_color = p2_color, p1_color
            w_sub, l_sub = p2_sub, p1_sub
            w_key, l_key = "p2", "p1"
            w_nat20 = p2_nat20
        else:
            # TIE! Roll standoff or Clash rules
            metrics["clashes"] += 1
            log_print(f"\n{C_BOLD}{C_YELLOW}--> CLASH RESOLUTION (Tied rolls: {p1_total} vs {p2_total}){C_RESET}")
            if p1_color == "strike" and p2_color == "block":
                log_print(f"  -> {p2.name}'s block holds, but they are STAGGERED next turn.")
                p2.staggered = True
                if p2_sub == "stand up" and p2.prone:
                    p2.prone = False
                    log_print(f"  -> {p2.name} stands back up.")
            elif p2_color == "strike" and p1_color == "block":
                log_print(f"  -> {p1.name}'s block holds, but they are STAGGERED next turn.")
                p1.staggered = True
                if p1_sub == "stand up" and p1.prone:
                    p1.prone = False
                    log_print(f"  -> {p1.name} stands back up.")
            else:
                if p1_sub == "stand up" and p1.prone:
                    p1.prone = False
                    log_print(f"  -> {p1.name} stands back up.")
                if p2_sub == "stand up" and p2.prone:
                    p2.prone = False
                    log_print(f"  -> {p2.name} stands back up.")
                log_print("  -> Standoff! Fighters reset to neutral.")

            if p1.pinned:
                p1.pinned = False
                log_print(f"  -> [Partial Break!] {p1.name} breaks the pin down to Prone.")
            if p2.pinned:
                p2.pinned = False
                log_print(f"  -> [Partial Break!] {p2.name} breaks the pin down to Prone.")
            continue

        # Winner-take-all resolution
        margin = w_total - l_total
        crit = w_nat20 or (margin >= 5)
        log_print(f"\n-> {C_GREEN}{C_BOLD}{winner.name} wins the exchange!{C_RESET} (Margin: {margin})")
        if winner.pinned:
            winner.pinned = False
            winner.prone = False
            log_print(f"   {C_GREEN}[Clean Break!]{C_RESET} {winner.name} breaks the pin and stands right back up to their feet!")
        if crit:
            metrics[w_key]["crits"] += 1
            if not w_nat20:
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
                # Karate Ikken Hissatsu: extra +1 on crits
                if winner.style_name == "Karate":
                    base_dmg += 1
                    log_print(f"   {C_RED}[Karate Ikken Hissatsu]{C_RESET} Extra +1 damage on critical!")
                
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
            
            # Track strike landing for Chain Strike
            if winner == p1: p1_struck_this_round = True
            else: p2_struck_this_round = True
            
            # Karate Kiai Shout: once-per-fight contested Cool check after landing a strike
            if winner.style_name == "Karate" and not winner.kiai_used and not loser.is_defeated():
                winner.kiai_used = True
                w_kiai, _ = winner.roll_dice(2)
                l_kiai, _ = loser.roll_dice(2)
                w_kiai_tot = w_kiai + winner.attrs["cool"]
                l_kiai_tot = l_kiai + loser.attrs["cool"]
                log_print(f"   {C_YELLOW}[Karate Kiai Shout]{C_RESET} {winner.name} lets out a battle cry! (Contested Cool: {winner.name} {w_kiai_tot} vs {loser.name} {l_kiai_tot})")
                if w_kiai_tot > l_kiai_tot:
                    loser.attrs["cool"] = max(0, loser.attrs["cool"] - 1)
                    loser.staggered = True
                    metrics[w_key]["damage_dealt"]["cool"] += 1
                    metrics[l_key]["damage_taken"]["cool"] += 1
                    log_print(f"   -> {winner.name} wins the clash of wills! {loser.name} suffers 1 COOL damage AND is STAGGERED! (Cool: {loser.attrs['cool']})")
                else:
                    log_print(f"   -> {loser.name} keeps their composure and resists the Kiai Shout.")

        # 2. Resolve Block (Parry/Dodge)
        elif w_color == "block":
            log_print(f"   {winner.name} successfully defends using {w_sub}.")
            if w_sub == "parry" and winner.style_name == "Judo" and l_color == "strike":
                log_print(f"   {C_GREEN}[Judo Kuzushi]{C_RESET} {winner.name} attempts a Sweeping Reversal!")
                t_roll = winner.roll_dice(2)[0] + winner.attrs["agility"]
                d_roll = loser.roll_dice(2)[0] + loser.attrs["agility"]
                if t_roll > d_roll:
                    log_print(f"   -> Reversal success! {loser.name} is swept off their feet!")
                    loser.prone = True
                    sweep_dmg = 2
                    loser.attrs["agility"] = max(0, loser.attrs["agility"] - sweep_dmg)
                    metrics[w_key]["damage_dealt"]["agility"] += sweep_dmg
                    metrics[l_key]["damage_taken"]["agility"] += sweep_dmg
                else:
                    log_print(f"   -> {loser.name} keeps their balance.")
            
            if w_sub == "dodge" and winner.style_name == "Boxing" and l_color == "strike":
                winner.slip_adv = True
                log_print(f"   {C_GREEN}[Boxing Slip & Counter]{C_RESET} {winner.name} dodged! Next Strike has Advantage.")
            
            # Kung Fu Flowing Redirect: Parry a strike -> Trapping hands (Stagger target + Advantage on next Strike)
            if w_sub == "parry" and winner.style_name == "Kung Fu" and l_color == "strike":
                loser.staggered = True
                winner.slip_adv = True
                log_print(f"   {C_GREEN}[Kung Fu Flowing Redirect]{C_RESET} {winner.name} trapped opponent's limbs! {loser.name} is STAGGERED and next Strike gains Advantage.")
                
            if w_sub == "stand up" and winner.prone:
                log_print(f"   {winner.name} stands back up.")
                winner.prone = False

        # 3. Resolve Throw
        elif w_color == "throw":
            if w_sub == "clinch":
                log_print(f"   {winner.name} locks {loser.name} in a Clinch/Grab.")
                winner.range = "grapple"
                loser.range = "grapple"
            elif w_sub == "trip":
                log_print(f"   {winner.name} sweeps {loser.name}'s legs!")
                loser.prone = True
                dmg = 2
                if crit: dmg += 1
                loser.attrs["agility"] = max(0, loser.attrs["agility"] - dmg)
                metrics[w_key]["damage_dealt"]["agility"] += dmg
                metrics[l_key]["damage_taken"]["agility"] += dmg
                log_print(f"   {loser.name} takes {dmg} AGILITY damage.")
            elif w_sub == "hip throw":
                log_print(f"   {winner.name} throws {loser.name} over their shoulder!")
                loser.prone = True
                dmg = 3
                if crit: dmg += 1
                loser.attrs["power"] = max(0, loser.attrs["power"] - dmg)
                metrics[w_key]["damage_dealt"]["power"] += dmg
                metrics[l_key]["damage_taken"]["power"] += dmg
                log_print(f"   {loser.name} takes {dmg} POWER damage.")
                if crit:
                    log_print(f"   {loser.name} is STUNNED by the impact!")
                    loser.stunned = True
            elif w_sub == "takedown":
                log_print(f"   {winner.name} drives through with a Double Leg Takedown!")
                loser.prone = True
                dmg = 3
                if crit: dmg += 1
                loser.attrs["power"] = max(0, loser.attrs["power"] - dmg)
                metrics[w_key]["damage_dealt"]["power"] += dmg
                metrics[l_key]["damage_taken"]["power"] += dmg
                log_print(f"   {loser.name} takes {dmg} POWER damage.")
                if winner.style_name == "Wrestling":
                    log_print(f"   {C_GREEN}[Wrestling Ground Control]{C_RESET} opponent is PINNED on the canvas!")
                    loser.pinned = True
            elif w_sub == "submission hold":
                log_print(f"   {winner.name} locks {loser.name} in a Submission Hold!")
                dmg = 3
                if crit: dmg += 1
                loser.attrs["stamina"] = max(0, loser.attrs["stamina"] - dmg)
                metrics[w_key]["damage_dealt"]["stamina"] += dmg
                metrics[l_key]["damage_taken"]["stamina"] += dmg
                log_print(f"   {loser.name} takes {dmg} STAMINA damage from choke/joint pressure!")

        # Clear stun duration
        if p1.stunned and winner == p1: p1.stunned = False
        if p2.stunned and winner == p2: p2.stunned = False
        
        # Update Kung Fu Chain Strike tracking for next round
        p1.last_round_struck = p1_struck_this_round
        p2.last_round_struck = p2_struck_this_round
        
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
    write_metrics_report(p1, p2, metrics, match_result, should_write=should_write)

def resolve_hit(attacker, move, target, damage, crit, metrics, att_key, def_key):
    target_attr = "reaction"
    if move in ["jab", "cross", "high kick"]:
        target_attr = "reaction"
    elif move == "hook":
        target_attr = "stamina" if target.attrs["stamina"] <= target.attrs["power"] else "power"
    elif move == "uppercut":
        target_attr = "power"
    elif move in ["body kick", "push kick"]:
        target_attr = "stamina"
    elif move == "low kick":
        target_attr = "agility"
    elif move == "taunt":
        target_attr = "cool"
    elif move == "ground & pound":
        target_attr = "power" if target.attrs["power"] <= target.attrs["stamina"] else "stamina"

    # Deal damage
    target.attrs[target_attr] = max(0, target.attrs[target_attr] - damage)
    metrics[att_key]["damage_dealt"][target_attr] += damage
    metrics[def_key]["damage_taken"][target_attr] += damage
    
    log_print(f"   {attacker.name}'s {move.upper()} hits {target.name} for {C_RED}{damage} {target_attr.upper()} damage!{C_RESET} (New: {target.attrs[target_attr]})")
    
    if move == "low kick":
        penalty = 2 if attacker.style_name == "Muay Thai" else 1
        target.hobbled = penalty
        log_print(f"   -> {target.name} is HOBBLED (-{penalty} Agility rolls next round)")
    elif move == "body kick":
        target.winded = True
        log_print(f"   -> {target.name} is WINDED (-1 Stamina rolls next round)")
    elif move == "taunt":
        if target.attrs["cool"] <= 0:
            target.shaken = True
            log_print(f"   -> {target.name} is SHAKEN! (Cool reduced to 0. Reactions suffer -2; perks suspended)")

    if crit and move == "high kick":
        log_print(f"   -> {target.name} is STUNNED by the massive blow!")
        target.stunned = True

def write_metrics_report(p1, p2, metrics, match_result, should_write=False):
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
    log_print(f"  Damage Dealt: R:{p1_stats['damage_dealt']['reaction']} P:{p1_stats['damage_dealt']['power']} A:{p1_stats['damage_dealt']['agility']} S:{p1_stats['damage_dealt']['stamina']} C:{p1_stats['damage_dealt']['cool']}")
    
    log_print(f"\n{C_BOLD}Fighter: {p2.name} ({p2.style_name or 'Brawler'}){C_RESET}")
    log_print(f"  Actions:  {p2_stats['strikes']} Strikes | {p2_stats['blocks']} Blocks | {p2_stats['throws']} Throws")
    log_print(f"  Reads:    {p2_stats['reads_won']} Stance Reads Won")
    log_print(f"  Crits:    {p2_stats['crits']} Critical Hits Landed")
    log_print(f"  Damage Dealt: R:{p2_stats['damage_dealt']['reaction']} P:{p2_stats['damage_dealt']['power']} A:{p2_stats['damage_dealt']['agility']} S:{p2_stats['damage_dealt']['stamina']} C:{p2_stats['damage_dealt']['cool']}")
    
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
    md.append(f"| **Reaction Damage Dealt** | {p1_stats['damage_dealt']['reaction']} | {p2_stats['damage_dealt']['reaction']} |")
    md.append(f"| **Power Damage Dealt** | {p1_stats['damage_dealt']['power']} | {p2_stats['damage_dealt']['power']} |")
    md.append(f"| **Agility Damage Dealt** | {p1_stats['damage_dealt']['agility']} | {p2_stats['damage_dealt']['agility']} |")
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
    
    if should_write:
        with open(report_path, "w") as f:
            f.write(report_content)
        print(f"\nDetailed markdown combat log written to: {report_path}")

def main():
    should_write = "-w" in sys.argv or "--write" in sys.argv
    args = [a for a in sys.argv if a not in ["-w", "--write"]]

    if len(args) > 1 and args[1] in ["-h", "--help"]:
        print("Saturday Night Street Fight — 1v1 Duel Simulator")
        print("Usage:")
        print("  ./duel_simulator.py          : Launch 1v1 Street Fight Duel Simulator")
        print("  Options:")
        print("    -w, --write              : Save detailed markdown combat log (duel_report.md)")
        print("    -h, --help               : Show this help menu")
        sys.exit(0)

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
        interactive_generation(should_write=should_write)
        print("\nNow let's load that character or roll a random brawler for the duel...")
        name, style_name, arch_name, attrs, masteries, xp = generate_random_character()
    else:
        name, style_name, arch_name, attrs, masteries, xp = generate_random_character()

    p1 = Combatant(name, "PC", attrs, masteries, style_name)

    print("\nSelect Opponent (NPC):")
    print("  1. Tier 1 Punk / Lookout")
    print("  2. Tier 2 Standard Thug")
    print("  3. Tier 3 Syndicate Boss")
    print("  4. Tier 4 Syndicate Warlord (Master)")
    print("  5. Tier 4+ Supreme Syndicate Overlord (Grandmaster)")
    try:
        opp_choice = input("Select opponent tier (1-5, default 2): ").strip()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

    if opp_choice == "1":
        npc_data = generate_punk()
    elif opp_choice == "3":
        npc_data = generate_boss()
    elif opp_choice == "4":
        npc_data = generate_warlord()
    elif opp_choice == "5":
        npc_data = generate_overlord()
    else:
        npc_data = generate_thug()

    p2 = Combatant(
        npc_data["name"].split(" (")[0].replace("'", ""), 
        npc_data["tier"], 
        npc_data["attrs"], 
        npc_data["masteries"], 
        npc_data.get("style", None)
    )

    run_fight(p1, p2, should_write=should_write)

if __name__ == "__main__":
    main()
