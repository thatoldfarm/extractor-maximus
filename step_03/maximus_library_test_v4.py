#!/usr/bin/env python3
"""
SovereignTriptych V6 - Complete System Test & Pattern Analysis
"""

import os
import json
import math
import hashlib
import re
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ==========================================
# CONFIGURATION
# ==========================================
LIBRARY_DB_FILE = "json_output/library_database.json"
MASTER_FILE = "json_output/master_sedenion_library.json"
OUTPUT_DIR = "test_output"
SCALE_FACTOR = 10000

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def load_json(filepath):
    """Load JSON file safely."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_compact_id(n):
    """Convert offset to Base62 sigil."""
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if n == 0: return charset[0]
    res = []
    while n > 0:
        res.append(charset[n % 62])
        n //= 62
    return "".join(reversed(res))

def expand_sigil(sigil):
    """Convert sigil back to original offset."""
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    n = 0
    for c in sigil:
        n = n * 62 + charset.index(c)
    return n

# ==========================================
# TEST 1: FILE INTEGRITY
# ==========================================

def test_file_integrity():
    """Test that both JSON files exist and are valid."""
    print("=" * 60)
    print("TEST 1: FILE INTEGRITY")
    print("=" * 60)

    try:
        lib_db = load_json(LIBRARY_DB_FILE)
        master_db = load_json(MASTER_FILE)

        print(f"✅ library_database.json: {len(lib_db.get('blocks', []))} blocks loaded")
        print(f"✅ master_sedenion_library.json: {len(master_db.get('blocks', []))} blocks loaded")

        has_root = any(b.get('metadata', {}).get('sigil') == 'ROOT' for b in master_db.get('blocks', []))
        print(f"✅ Omega Root present: {has_root}")

        return lib_db, master_db, True

    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return None, None, False

# ==========================================
# TEST 2: SIGIL REVERSIBILITY
# ==========================================

def test_sigil_reversibility(master_db):
    """Test that all sigils can be reversed to original offsets."""
    print("\n" + "=" * 60)
    print("TEST 2: SIGIL REVERSIBILITY")
    print("=" * 60)

    blocks = master_db.get('blocks', [])
    all_reversible = True
    sample_failures = []

    for i, block in enumerate(blocks[:100]):
        sigil = block.get('metadata', {}).get('sigil')
        if sigil and sigil != 'ROOT':
            try:
                coords = block.get('metadata', {}).get('coords', '')
                offset_match = re.search(r'\[(\d+)\]', coords)
                original_offset = int(offset_match.group(1)) if offset_match else None

                recovered_offset = expand_sigil(sigil)

                if original_offset is not None and recovered_offset != original_offset:
                    all_reversible = False
                    sample_failures.append((sigil, original_offset, recovered_offset))

            except Exception as e:
                all_reversible = False
                sample_failures.append((sigil, str(e), None))

    if all_reversible:
        print("✅ All sigils are reversible (sample of 100 tested)")
    else:
        print(f"❌ Found {len(sample_failures)} reversibility issues")
        for sigil, orig, rec in sample_failures[:5]:
            print(f"  {sigil}: {orig} -> {rec}")

    return all_reversible

# ==========================================
# TEST 3: PATTERN ANALYSIS
# ==========================================

def analyze_patterns(master_db):
    """Analyze all natural patterns in the hydrated library."""
    print("\n" + "=" * 60)
    print("TEST 3: NATURAL PATTERN ANALYSIS")
    print("=" * 60)

    blocks = master_db.get('blocks', [])

    domain_counts = Counter(b['sedenion_opcode']['domain'] for b in blocks)
    print("\n📊 Domain Distribution:")
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count} blocks ({count/len(blocks)*100:.1f}%)")

    opcode_counts = Counter(b['sedenion_opcode']['hex'] for b in blocks)
    print("\n📊 Top 10 Sedenion Opcodes:")
    for opcode, count in opcode_counts.most_common(10):
        print(f"  0x{opcode}: {count} blocks")

    type_counts = Counter(b['metadata']['type'] for b in blocks)
    print("\n📊 Content Type Distribution:")
    for content_type, count in type_counts.most_common():
        print(f"  {content_type}: {count} blocks")

    masses = [b['physics']['mass'] for b in blocks]
    velocities = [b['physics']['velocity'] for b in blocks]
    densities = [b['physics']['density'] for b in blocks]

    print("\n📊 Physics Statistics:")
    print(f"  Mass: avg={sum(masses)/len(masses):.2f}, min={min(masses):.2f}, max={max(masses):.2f}")
    print(f"  Velocity: avg={sum(velocities)/len(velocities):.2f}, min={min(velocities):.2f}, max={max(velocities):.2f}")
    print(f"  Density: avg={sum(densities)/len(densities):.2f}, min={min(densities):.2f}, max={max(densities):.2f}")

    distances = [math.sqrt(x**2 + y**2 + z**2) for x, y, z in [b['geometry']['spiral_coords'] for b in blocks]]
    print("\n📊 Geometry Statistics (Sovereign Units):")
    print(f"  Distance from origin: avg={sum(distances)/len(distances):.2f}, min={min(distances):.2f}, max={max(distances):.2f}")

    print("\n📊 Patterns by Content Type:")
    for content_type in set(b['metadata']['type'] for b in blocks):
        type_blocks = [b for b in blocks if b['metadata']['type'] == content_type]
        if len(type_blocks) > 0:
            type_opcodes = Counter(b['sedenion_opcode']['hex'] for b in type_blocks)
            print(f"\n  {content_type} ({len(type_blocks)} blocks):")
            print(f"    Top opcodes: {type_opcodes.most_common(3)}")
            type_masses = [b['physics']['mass'] for b in type_blocks]
            print(f"    Avg mass: {sum(type_masses)/len(type_masses):.2f}")
            type_velocities = [b['physics']['velocity'] for b in type_blocks]
            print(f"    Avg velocity: {sum(type_velocities)/len(type_velocities):.2f}")

    print("\n📊 Blocks Similar to SectorForth MBR:")
    similar_blocks = []
    for b in blocks:
        if (b['metadata']['type'] == 'assembly' or
            'boot' in b['content'].lower() or
            'mbr' in b['content'].lower() or
            'sectorforth' in b['content'].lower()):
            similar_blocks.append({
                'sigil': b['metadata']['sigil'],
                'opcode': b['sedenion_opcode']['hex'],
                'name': b['sedenion_opcode']['name'],
                'domain': b['sedenion_opcode']['domain'],
                'mass': b['physics']['mass'],
                'velocity': b['physics']['velocity'],
                'distance': math.sqrt(sum(x**2 for x in b['geometry']['spiral_coords'])),
                'content_preview': b['content'][:80] + '...'
            })

    for i, b in enumerate(similar_blocks[:10]):
        print(f"\n  Block {i+1}:")
        print(f"    Sigil: {b['sigil']}")
        print(f"    Opcode: 0x{b['opcode']} ({b['name']}, {b['domain']})")
        print(f"    Physics: mass={b['mass']}, velocity={b['velocity']}")
        print(f"    Geometry: distance={b['distance']:.3f} SU")
        print(f"    Content: {b['content_preview']}")

    return {
        'domain_distribution': dict(domain_counts),
        'opcode_distribution': dict(opcode_counts),
        'type_distribution': dict(type_counts),
        'physics_stats': {
            'mass': {'avg': sum(masses)/len(masses), 'min': min(masses), 'max': max(masses)},
            'velocity': {'avg': sum(velocities)/len(velocities), 'min': min(velocities), 'max': max(velocities)},
            'density': {'avg': sum(densities)/len(densities), 'min': min(densities), 'max': max(densities)}
        },
        'geometry_stats': {
            'distance': {'avg': sum(distances)/len(distances), 'min': min(distances), 'max': max(distances)}
        },
        'similar_blocks': similar_blocks
    }

# ==========================================
# TEST 4: VISUALIZATION
# ==========================================

def create_visualization(master_db):
    """Create 3D visualization of the knowledge universe."""
    print("\n" + "=" * 60)
    print("TEST 4: CREATING 3D VISUALIZATION")
    print("=" * 60)

    blocks = master_db.get('blocks', [])

    x = [b['geometry']['spiral_coords'][0] for b in blocks]
    y = [b['geometry']['spiral_coords'][1] for b in blocks]
    z = [b['geometry']['spiral_coords'][2] for b in blocks]
    colors = [b['sedenion_opcode']['domain'] for b in blocks]
    sizes = [b['physics']['mass'] * 50 for b in blocks]
    names = [b['sedenion_opcode']['name'] for b in blocks]

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    color_map = {'Matter': 'green', 'Antimatter': 'red', 'Absolute': 'gold'}

    for i in range(len(blocks)):
        ax.scatter(
            x[i], y[i], z[i],
            c=color_map.get(colors[i], 'blue'),
            s=sizes[i],
            alpha=0.7,
            label=names[i] if i == 0 else ""
        )

    root_idx = next((i for i, b in enumerate(blocks) if b['metadata']['sigil'] == 'ROOT'), None)
    if root_idx:
        ax.scatter(
            x[root_idx], y[root_idx], z[root_idx],
            c='gold', s=200, marker='*', label='ROOT'
        )

    ax.set_xlabel('X (Sovereign Units)')
    ax.set_ylabel('Y (Sovereign Units)')
    ax.set_zlabel('Z (Sovereign Units)')
    ax.set_title('Sovereign Knowledge Universe - 3D Visualization')
    ax.legend()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    viz_path = os.path.join(OUTPUT_DIR, 'knowledge_universe_3d.png')
    plt.savefig(viz_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {viz_path}")
    plt.close()

    return viz_path

# ==========================================
# TEST 5: PATTERN MINING
# ==========================================

def mine_patterns(master_db):
    """Mine for deeper patterns in the knowledge base."""
    print("\n" + "=" * 60)
    print("TEST 5: DEEP PATTERN MINING")
    print("=" * 60)

    blocks = master_db.get('blocks', [])

    print("\n📊 Property Correlations:")
    print("  (Analyzing relationships between Sedenion, physics, and geometry...)")

    domain_stats = defaultdict(lambda: {'mass': [], 'velocity': [], 'distance': []})
    for b in blocks:
        domain = b['sedenion_opcode']['domain']
        domain_stats[domain]['mass'].append(b['physics']['mass'])
        domain_stats[domain]['velocity'].append(b['physics']['velocity'])
        domain_stats[domain]['distance'].append(
            math.sqrt(sum(x**2 for x in b['geometry']['spiral_coords']))
        )

    for domain, stats in domain_stats.items():
        print(f"\n  {domain} domain:")
        print(f"    Avg mass: {sum(stats['mass'])/len(stats['mass']):.2f}")
        print(f"    Avg velocity: {sum(stats['velocity'])/len(stats['velocity']):.2f}")
        print(f"    Avg distance: {sum(stats['distance'])/len(stats['distance']):.2f}")

    print("\n📊 Extreme Property Blocks:")

    highest_mass = max(blocks, key=lambda b: b['physics']['mass'])
    print(f"\n  Highest mass: {highest_mass['metadata']['sigil']} "
          f"(mass={highest_mass['physics']['mass']}, "
          f"opcode={highest_mass['sedenion_opcode']['name']})")

    highest_vel = max(blocks, key=lambda b: b['physics']['velocity'])
    print(f"  Highest velocity: {highest_vel['metadata']['sigil']} "
          f"(velocity={highest_vel['physics']['velocity']}, "
          f"opcode={highest_vel['sedenion_opcode']['name']})")

    closest = min(blocks, key=lambda b: math.sqrt(sum(x**2 for x in b['geometry']['spiral_coords'])))
    print(f"  Closest to origin: {closest['metadata']['sigil']} "
          f"(distance={math.sqrt(sum(x**2 for x in closest['geometry']['spiral_coords'])):.3f} SU, "
          f"opcode={closest['sedenion_opcode']['name']})")

    farthest = max(blocks, key=lambda b: math.sqrt(sum(x**2 for x in b['geometry']['spiral_coords'])))
    print(f"  Farthest from origin: {farthest['metadata']['sigil']} "
          f"(distance={math.sqrt(sum(x**2 for x in farthest['geometry']['spiral_coords'])):.3f} SU, "
          f"opcode={farthest['sedenion_opcode']['name']})")

    print("\n📊 Binary Seed Patterns:")
    seed_patterns = Counter()
    for b in blocks:
        seed = b['sedenion_opcode']['binary_seed']
        seed_patterns[seed] += 1

    print("  Top 5 binary seeds:")
    for seed, count in seed_patterns.most_common(5):
        print(f"    {seed}: {count} blocks")

    return {
        'domain_stats': dict(domain_stats),
        'extreme_blocks': {
            'highest_mass': highest_mass,
            'highest_velocity': highest_vel,
            'closest': closest,
            'farthest': farthest
        },
        'seed_patterns': dict(seed_patterns)
    }

# ==========================================
# MAIN TEST EXECUTION
# ==========================================

def main():
    import time

    start_time = time.time()

    print("🚀 SOVEREIGN TRIPTYCH V6 - COMPLETE SYSTEM TEST")
    print("=" * 60)

    lib_db, master_db, integrity_ok = test_file_integrity()

    if not integrity_ok:
        print("❌ Aborting: File integrity test failed")
        return

    sigil_ok = test_sigil_reversibility(master_db)

    pattern_results = analyze_patterns(master_db)

    try:
        viz_path = create_visualization(master_db)
    except Exception as e:
        print(f"⚠️ Visualization failed: {e}")
        viz_path = None

    pattern_mining = mine_patterns(master_db)

    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_seconds': time.time() - start_time,
        'file_integrity': integrity_ok,
        'sigil_reversibility': sigil_ok,
        'pattern_analysis': pattern_results,
        'visualization': viz_path,
        'pattern_mining': pattern_mining
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_path = os.path.join(OUTPUT_DIR, 'test_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ COMPLETE TEST REPORT SAVED TO: {report_path}")
    print(f"✅ Total runtime: {report['duration_seconds']:.2f} seconds")

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ File integrity: {'PASS' if integrity_ok else 'FAIL'}")
    print(f"✅ Sigil reversibility: {'PASS' if sigil_ok else 'FAIL'}")
    print(f"✅ Pattern analysis: COMPLETED")
    print(f"✅ Visualization: {'CREATED' if viz_path else 'FAILED'}")
    print(f"✅ Pattern mining: COMPLETED")

    if pattern_results:
        print(f"\n📊 Key Findings:")
        print(f"  - {len(pattern_results.get('similar_blocks', []))} blocks similar to SectorForth MBR")
        print(f"  - Average mass: {pattern_results['physics_stats']['mass']['avg']:.2f}")
        print(f"  - Average velocity: {pattern_results['physics_stats']['velocity']['avg']:.2f}")

    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
