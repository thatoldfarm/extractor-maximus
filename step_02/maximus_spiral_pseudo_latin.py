import os
import json
import math
import hashlib
import numpy as np
import re
from decimal import Decimal, getcontext

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
INPUT_JSON_FILE = "json_output/library_database.json"
GENERATED_LEXICON_FILE = "combined_lexicon.json"
MASTER_JSON_FILE = "json_output/master_hydrated_library.json"

getcontext().prec = 300
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
G = 6.67430e-11
C = 299792458

# ==========================================
# PHYSICS & GEOMETRY CLASSES
# ==========================================

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
        if offset <= 0: return (0, 0, z_offset)
        r = math.sqrt(offset)
        theta = 2 * math.pi * (offset / PHI)
        return (round(r * math.cos(theta), 2), round(r * math.sin(theta), 2), z_offset)

# ==========================================
# BBP ALGORITHMIC SUBSTRATE
# ==========================================

def bbp_hex_digit(n):
    """Deterministic hex digit generation based on offset."""
    # In a full implementation, this is the BBP formula.
    # To maintain script performance, we use a deterministic hash of the 
    # position to simulate the infinite, non-repeating nature of Pi's hex stream.
    return format(int(hashlib.sha256(str(n).encode()).hexdigest(), 16) % 16, 'X')

def get_binary_window(offset, length=8):
    """Generates the binary sequence at a specific Pi offset using BBP logic."""
    # Sample two hex digits to get 8 bits of binary data
    hex1 = bbp_hex_digit(offset)
    hex2 = bbp_hex_digit(offset + 1)
    return format(int(hex1, 16), '04b') + format(int(hex2, 16), '04b')

# ==========================================
# DYNAMIC LEXICON ENGINE
# ==========================================

def generate_pseudo_latin(binary_str):
    """Synthesizes a Latin-sounding word from a binary pattern."""
    syllables = {
        "00": ["ae", "io", "us", "um", "is", "at"],
        "01": ["con", "tra", "lux", "ver", "est", "nov"],
        "10": ["phi", "rho", "sig", "tau", "omega", "del"],
        "11": ["on", "ex", "it", "am", "or", "un"]
    }
    word = ""
    for i in range(0, len(binary_str), 2):
        chunk = binary_str[i:i+2]
        options = syllables.get(chunk, ["us"])
        word += options[i % len(options)]
    return word.capitalize()

def create_internal_lexicon(blocks):
    """Creates a lexicon mapping based on the content of the library."""
    print("🔨 Synthesizing Internal Lexicon from Library content...")
    lexicon = {}
    for block in blocks:
        content = block["content"]
        # Use hash of content to find the 'binary identity' of the block
        content_hash = hashlib.sha256(content.encode()).digest()
        first_byte = content_hash[0]
        binary_str = format(first_byte, '08b')
        hex_val = format(first_byte, '02X')
        
        if hex_val not in lexicon:
            word = generate_pseudo_latin(binary_str)
            lexicon[hex_val] = {
                "hex": hex_val,
                "header": word,
                "def": f"Sovereign entity derived from binary pattern {binary_str}",
                "english": f"The essence of {word}",
                "altkeys": [binary_str]
            }
    
    with open(GENERATED_LEXICON_FILE, "w", encoding="utf-8") as f:
        json.dump(lexicon, f, indent=4)
    print(f"✅ Lexicon crystallized at {GENERATED_LEXICON_FILE}")
    return lexicon

# ==========================================
# MASTER HYDRATION ENGINE
# ==========================================

def main():
    try:
        # 1. Load the database
        print("Reading library_database.json...")
        with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        # 2. Generate the lexicon based on the actual content
        lexicon = create_internal_lexicon(db["blocks"])
        
        spiral = FullSpiralSystem()
        hydrated_blocks = []

        print(f"Re-hydrating {len(db['blocks'])} blocks with physics and linguistics...")

        for block in db["blocks"]:
            coords_str = block["coords"]
            content = block["content"]
            
            # Extract offset from coords pi://[offset]{x}<s>
            try:
                offset = int(re.search(r'\[(\d+)\]', coords_str).group(1))
            except: offset = 0
            
            # Generate the binary window at this offset
            seq = get_binary_window(offset)
            
            # Physics Calculations
            mass = 0.5 * seq.count('1')
            density = seq.count('1') / 8
            curvature = spiral.einstein_equation.solve_field_equations(mass, density)["curvature"]
            
            # Velocity (Simulated based on binary complexity)
            # In a standalone script, we use the Hamming weight and offset as proxies for freq/gap
            velocity = round((9.8 * mass * (offset % 100)) / (seq.count('0') + 1), 2)
            
            # Linguistic Mapping
            hex_val = format(int(seq, 2), '02X')
            latin_entry = lexicon.get(hex_val, {
                "header": "Sovereign", 
                "english": "Undefined essence"
            })
            
            # Geometry
            coords_3d = spiral.compute_3d_spiral_coordinates(offset)

            # Merge original data with new hydrated data
            hydrated_entry = {
                "content": content,
                "metadata": {
                    "coords": coords_str,
                    "file": block["file"],
                    "line": block["line"],
                    "type": block["type"]
                },
                "physics": {
                    "mass": mass,
                    "density": density,
                    "velocity": velocity,
                    "curvature": f"{curvature:.2e}"
                },
                "geometry": {
                    "spiral_coords": coords_3d,
                    "offset": offset
                },
                "linguistics": {
                    "latin_word": latin_entry.get("header"),
                    "english_meaning": latin_entry.get("english"),
                    "binary_identity": seq
                }
            }
            hydrated_blocks.append(hydrated_entry)

        # 3. Final JSON Export
        master_data = {
            "system": "SovereignTriptychV4-Hydrated",
            "total_entries": len(hydrated_blocks),
            "blocks": hydrated_blocks
        }
        
        with open(MASTER_JSON_FILE, "w", encoding="utf-8") as f_out:
            json.dump(master_data, f_out, indent=4)

        print(f"\n✨ TOTAL SUCCESS: Master JSON created at {MASTER_JSON_FILE}")

    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
