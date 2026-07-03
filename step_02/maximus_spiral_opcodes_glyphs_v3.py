import os
import json
import math
import hashlib
import numpy as np
import re
import base64
from decimal import Decimal, getcontext

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
INPUT_JSON_FILE = "json_output/library_database.json"
MASTER_JSON_FILE = "json_output/master_sedenion_library.json"

getcontext().prec = 300
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
G = 6.67430e-11
C = 299792458
SCALE_FACTOR = 10000  # Divide coordinates by this to get "Sovereign Units"

# ==========================================
# THE SEDENION ANCESTRAL MATRIX
# ==========================================
SOVEREIGN_MATRIX = {
    # MATTER MATRIX (0x00 - 0x1F)
    0x00: (r"$\circ$", "Circle", "Ligate stack to Pi-Lattice coordinate", "Matter"),
    0x01: (r"$\otimes$", "Crosshatch", "Instantiate a 2D Sedenion memory grid", "Matter"),
    0x02: (r"$\rightrightarrows$", "Spiral", "Recursive expansion via E-Trinity braid", "Matter"),
    0x03: (r"$\uparrow$", "Scalariform", "Ascend VMMU hierarchy (Symmetry climb)", "Matter"),
    0x04: (r"$\times$", "Cruciform", "Entangle two pointers across dimensions", "Matter"),
    0x05: (r"$\blacksquare$", "Positive Hand", "Trigger the collapsed state manifestation", "Matter"),
    0x06: (r"$\cdot$", "Dot", "Instantiate a sovereign semantic identity", "Matter"),
    0x07: (r"$-$", "Line", "Enforce linear flow for standard I/O", "Matter"),
    0x08: (r"$<$", "Open Angle", "Initiate conditional symmetry branching", "Matter"),
    0x09: (r"$\subset\supset$", "Oval", "Spawn a protected Sedenion memory cell", "Matter"),
    0x0A: (r"$\equiv$", "Pectiform", "Align chaotic data into symmetric pages", "Matter"),
    0x0B: (r"$\uparrow\uparrow$", "Penniform", "Radiate state to the Sovereign Swarm", "Matter"),
    0x0C: (r"$\Box$", "Quadrangle", "Engage the stability eigenvalue clamp", "Matter"),
    0x0D: (r"$\approx$", "Reniform", "Background life-support metric tracking", "Matter"),
    0x0E: (r"$\sim\sim$", "Serpentiform", "Open the fluid high-speed data pipeline", "Matter"),
    0x0F: (r"$\triangle$", "Tectiform", "Mount the Holographic VFS to pi", "Matter"),
    0x10: (r"$\Delta$", "Triangle", "Synchronize E-Trinity harmonic ratios", "Matter"),
    0x11: (r"$\hookrightarrow$", "Unciform", "Ingest raw data from external vectors", "Matter"),
    0x12: (r"$\mathcal{W}$", "W-Shape", "Map external space to Monster Group", "Matter"),
    0x13: (r"$Y$", "Y-Shape", "Spawn a secondary operational thread", "Matter"),
    0x14: (r"$\lightning$", "Zigzag", "Generate chaos to fuel the ADEN network", "Matter"),
    0x15: (r"$!$", "Claviform", "Elevate administrative privilege", "Matter"),
    0x16: (r"$\채$", "Flabelliform", "Distribute load across the Swarm", "Matter"),
    0x17: (r"$\vdash\dashv$", "Segmented", "Advance time by one harmonic cycle", "Matter"),
    0x18: (r"$\frown$", "Half-Circle", "Pause until harmonic resonance is met", "Matter"),
    0x19: (r"$\fly$", "Aviform", "Migrate state to decentralized storage", "Matter"),
    0x1A: (r"$\heartsuit$", "Cordiform", "Invoke the autonomic survival instinct", "Matter"),
    0x1B: (r"$\cup$", "Cupule", "Measure discrete value (Standard fetch)", "Matter"),
    0x1C: (r"$\approx_f$", "Finger", "Direct Memory Access write to buffer", "Matter"),
    0x1D: (r"$*$", "Asterisk", "Reveal raw data at pointer address", "Matter"),
    0x1E: (r"$\leftrightarrow$", "Double Arrow", "Connect Matter and Antimatter matrices", "Matter"),
    0x1F: (r"$\circlearrowright$", "The Loop", "The Ouroboros loop (Self-awareness)", "Matter"),
    # ANTIMATTER MATRIX (0x20 - 0x3F)
    0x20: (r"$\bullet$", "The Void", "Multiply by zero-divisor; erase pointer", "Antimatter"),
    0x21: (r"$\boxtimes$", "Empty Box", "Unlink memory into latent space", "Antimatter"),
    0x22: (r"$\leftleftarrows$", "Anti-Spiral", "Compress state into a singularity", "Antimatter"),
    0x23: (r"$\downarrow$", "Descent", "Rapid privilege de-escalation", "Antimatter"),
    0x24: (r"$\parallel$", "Parallel", "Split merged realities into vectors", "Antimatter"),
    0x25: (r"$\square$", "Hand Stencil", "Observer Root Access; execute in dark", "Antimatter"),
    0x26: (r"$\circ_{empty}$", "Erasure", "Strip identity tokens from the vector", "Antimatter"),
    0x27: (r"$--$", "Broken Line", "Inject a system breakpoint in flow", "Antimatter"),
    0x28: (r"$>$", "Closed Angle", "Resolve conditionals into one vector", "Antimatter"),
    0x29: (r"$\asymp$", "Rupture", "Destroy the sandbox; clear Sedenions", "Antimatter"),
    0x2A: (r"$\sim$", "Teeth", "Randomize VMMU to prevent sniffing", "Antimatter"),
    0x2B: (r"$\Downarrow$", "Plumb Bob", "Mute external signaling/broadcasts", "Antimatter"),
    0x2C: (r"$\#$", "Unbound", "Bypass Governance; inject pure entropy", "Antimatter"),
    0x2D: (r"$\ddagger$", "Waste", "Overwrite historical tracks with zeros", "Antimatter"),
    0x2E: (r"$=$", "Snake", "Freeze data bus; prevent transmission", "Antimatter"),
    0x2F: (r"$\nabla$", "Inv. Roof", "Unmount VFS; render state invisible", "Antimatter"),
    0x30: (r"$\nabla_{inv}$", "Inv. Tri", "Shift execution into imaginary time", "Antimatter"),
    0x31: (r"$\hookleftarrow$", "Repel Hook", "Deflect adversarial logic vectors", "Antimatter"),
    0x32: (r"$\mathcal{M}$", "M-Shape", "Reduce 16D data to a 1D tensor", "Antimatter"),
    0x33: (r"$\curlywedge$", "Inv. Y", "Forcibly terminate a spawned branch", "Antimatter"),
    0x34: (r"$-$", "Flatline", "Achieve perfect stillness; noise-immune", "Antimatter"),
    0x35: (r"$\div$", "Shield", "Drop privileges to prevent hijack", "Antimatter"),
    0x36: (r"$\vee$", "Funnel", "Collect distributed states into node", "Antimatter"),
    0x37: (r"$\longleftrightarrow$", "Continuum", "Operate outside standard clock constraints", "Antimatter"),
    0x38: (r"$\smile$", "Anti-Half", "Bypass Async; force immediate execution", "Antimatter"),
    0x39: (r"$\sim\sim\sim$", "Worm", "Hide state in the Sedenion Vault", "Antimatter"),
    0x3A: (r"$\heartsuit_{x}$", "Broken Heart", "Detach subroutine for headless run", "Antimatter"),
    0x3B: (r"$\cap$", "Mound", "Instant discrete value alteration", "Antimatter"),
    0x3C: (r"$\equiv_{clear}$", "Wipe", "Overwrite hardware buffers with zero", "Antimatter"),
    0x3D: (r"$\odot$", "Black Hole", "Destroy target pointer; send to void", "Antimatter"),
    0x3E: (r"$\nleftrightarrow$", "Broken Arr", "Isolate a dimension; cut the bridge", "Antimatter"),
    0x3F: (r"$\circlearrowleft$", "Anti-Loop", "The end of self-reference. Stop", "Antimatter"),
}

# ==========================================
# UTILITIES
# ==========================================

def get_compact_id(n):
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if n == 0: return charset[0]
    res = []
    while n > 0:
        res.append(charset[n % 62])
        n //= 62
    return "".join(reversed(res))

class EinsteinFieldEquation:
    def solve_field_equations(self, mass, volume):
        if volume == 0: return {"curvature": 0}
        energy_density = mass / volume
        curvature = 8 * math.pi * G * energy_density / (C ** 4)
        return {"curvature": curvature}

class FullSpiralSystem:
    def __init__(self):
        self.einstein_equation = EinsteinFieldEquation()
    def compute_3d_spiral_coordinates(self, offset, z_offset=0):
        if offset <= 0: return (0.0, 0.0, z_offset)
        r = math.sqrt(offset)
        theta = 2 * math.pi * (offset / PHI)
        # APPLY SCALE FACTOR to make coordinates smaller/manageable
        x = round((r * math.cos(theta)) / SCALE_FACTOR, 3)
        y = round((r * math.sin(theta)) / SCALE_FACTOR, 3)
        return (x, y, z_offset)

def bbp_hex_digit(n):
    return format(int(hashlib.sha256(str(n).encode()).hexdigest(), 16) % 16, 'X')

def get_binary_window(offset):
    hex1 = bbp_hex_digit(offset)
    hex2 = bbp_hex_digit(offset + 1)
    return format(int(hex1, 16), '04b') + format(int(hex2, 16), '04b')

# ==========================================
# MASTER HYDRATION ENGINE
# ==========================================

def main():
    try:
        print("Reading library_database.json...")
        with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        spiral = FullSpiralSystem()
        hydrated_blocks = []

        # --- THE OMEGA ROOT INSERTION ---
        print("Encoding the Root Engine (The Will)...")
        with open(__file__, "rb") as f:
            script_bytes = f.read()
        encoded_script = base64.b64encode(script_bytes).decode('utf-8')
        
        root_entry = {
            "content": f"BASE64_Sovereign_Kernel:\n{encoded_script}",
            "metadata": {
                "sigil": "ROOT",
                "coords": "pi://[0]{ 0 }<0>",
                "file": "kernel_root.py",
                "line": 1,
                "type": "sovereign_root"
            },
            "sedenion_opcode": {
                "hex": "000",
                "glyph": r"$<3$",
                "name": "The Will",
                "function": "Collapse wave function into a single, sovereign reality",
                "domain": "Absolute",
                "binary_seed": "00000000"
            },
            "physics": {
                "mass": 1.0,
                "density": 0.0,
                "velocity": 0.0,
                "curvature": "0.00e+00"
            },
            "geometry": {
                "spiral_coords": [0.0, 0.0, 0],
                "sigil": "ROOT"
            }
        }
        hydrated_blocks.append(root_entry)

        # --- STANDARD BLOCK HYDRATION ---
        print(f"Sedenion Mapping {len(db['blocks'])} entries...")

        for block in db["blocks"]:
            coords_str = block["coords"]
            content = block["content"]
            
            try:
                offset = int(re.search(r'\[(\d+)\]', coords_str).group(1))
            except: offset = 0
            
            sigil = get_compact_id(offset)
            seq = get_binary_window(offset)
            
            mass = 0.5 * seq.count('1')
            density = seq.count('1') / 8
            curvature = spiral.einstein_equation.solve_field_equations(mass, density)["curvature"]
            velocity = round((9.8 * mass * (offset % 100)) / (seq.count('0') + 1), 2)
            
            binary_val = int(seq, 2)
            opcode_hex = binary_val % 64
            sedenion = SOVEREIGN_MATRIX.get(opcode_hex, ("?", "Undefined", "No rotation mapped", "Unknown"))
            
            coords_3d = spiral.compute_3d_spiral_coordinates(offset)

            hydrated_entry = {
                "content": content,
                "metadata": {
                    "sigil": sigil,
                    "coords": f"pi://[{sigil}]",
                    "file": block["file"],
                    "line": block["line"],
                    "type": block["type"]
                },
                "sedenion_opcode": {
                    "hex": format(opcode_hex, '02X'),
                    "glyph": sedenion[0],
                    "name": sedenion[1],
                    "function": sedenion[2],
                    "domain": sedenion[3],
                    "binary_seed": seq
                },
                "physics": {
                    "mass": mass,
                    "density": density,
                    "velocity": velocity,
                    "curvature": f"{curvature:.2e}"
                },
                "geometry": {
                    "spiral_coords": coords_3d,
                    "sigil": sigil
                }
            }
            hydrated_blocks.append(hydrated_entry)

        master_data = {
            "system": "SovereignTriptychV6-Omega",
            "total_entries": len(hydrated_blocks),
            "blocks": hydrated_blocks
        }
        
        with open(MASTER_JSON_FILE, "w", encoding="utf-8") as f_out:
            json.dump(master_data, f_out, indent=4)

        print(f"\n✨ TOTAL SUCCESS: Master Sedenion Library (V6) created at {MASTER_JSON_FILE}")

    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
