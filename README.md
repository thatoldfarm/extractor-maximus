# extractor-maximus

**A Sovereign Knowledge Extraction and Hydration Pipeline**

---

## 🌌 **Overview**

**Extractor Maximus** is a **multi-phase, modular Python pipeline** designed to **parse, extract, categorize, and hydrate** knowledge blocks from markdown files into a **structured, physics-infused, and geometrically mapped JSON knowledge library**. It is built for **sovereign data processing**, enabling the creation of a **self-referential, Pi-Lattice-anchored knowledge universe** with **Sedenion opcodes**, **Einsteinian physics**, and **3D spiral geometry**.

---

## ✨ **Core Features**


| Feature                              | Description                                                                                                                |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Multi-Phase Extraction**           | Parses markdown files, extracts code/math blocks, and categorizes them by language/type.                                   |
| **Pi-Lattice Coordinates**           | Assigns unique Pi-Lattice coordinates (`pi://[offset]{x}<s>`) to each block for immutable addressing.                      |
| **Sedenion Opcode Mapping**          | Maps each block to a **64-entry Sedenion Ancestral Matrix** (Matter/Antimatter domains) with glyphs, names, and functions. |
| **Physics Hydration**                | Applies **Einstein Field Equations** to compute mass, density, velocity, and spacetime curvature for each block.           |
| **3D Spiral Geometry**               | Positions blocks in a **Golden Ratio (Φ)-based 3D spiral** for visualization and spatial analysis.                         |
| **Root Kernel Embedding**            | Encodes the pipeline itself as a **Base64/Gzip-compressed root entry** in the final library.                               |
| **Pseudo-Latin Lexicon**             | Optionally generates a **synthetic Latin-like lexicon** from binary patterns of block content.                             |
| **Pattern Analysis & Visualization** | Analyzes distributions, correlations, and extreme properties; generates 3D plots of the knowledge universe.                |


---

## 🏗️ **Architecture**

### **Phase 1: Extraction (`maximus_v3_2.py`)**

- **Input:** Markdown files in `/files`
- **Process:**
  1. Scans for code blocks (```), math blocks (`$$`, `$`), EML, and TENSOR tags.
  2. Extracts metadata (source, line number, language/type).
  3. Assigns **Pi-Lattice coordinates** using SHA256 hashing and lattice refraction.
- **Output:** Categorized blocks in `/files2` (e.g., `python.md`, `math.md`).

### **Phase 2: Hydration (Choose One)**


| Script                                | Purpose                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `maximus_spiral_pseudo_latin.py`      | Generates a **pseudo-Latin lexicon** from binary patterns.                                             |
| `maximus_spiral_opcodes_glyphs_v2.py` | Basic **Sedenion opcode/glyph mapping**.                                                               |
| `maximus_spiral_opcodes_glyphs_v3.py` | Advanced hydration with **root kernel embedding** and **scaled 3D coordinates**.                       |
| `maximus_spiral_opcodes_glyphs_v4.py` | **Most advanced**: Gzip-compressed root kernel, full Sedenion mapping, and physics/geometry hydration. |


- **Input:** `library_database.json` (from Phase 1).
- **Process:**
  1. Maps blocks to **Sedenion opcodes** (64 glyphs for Matter/Antimatter).
  2. Computes **physics properties** (mass, density, velocity, curvature) using binary seeds from Pi offsets.
  3. Assigns **3D spiral coordinates** (scaled for manageability).
  4. (Optional) Generates **pseudo-Latin lexicon** for linguistic mapping.
- **Output:** `master_sedenion_library.json` (hydrated knowledge base).

### **Phase 3: Testing & Analysis (`maximus_library_test_v4.py`)**

- **Input:** `master_sedenion_library.json`
- **Process:**
  1. **File Integrity Check**: Validates JSON structure and root kernel presence.
  2. **Sigil Reversibility Test**: Ensures Pi-Lattice sigils can be decoded back to original offsets.
  3. **Pattern Analysis**: Computes distributions of domains, opcodes, content types, and physics/geometry statistics.
  4. **3D Visualization**: Generates a **3D scatter plot** of the knowledge universe (saved as PNG).
  5. **Deep Pattern Mining**: Identifies extreme blocks (highest mass/velocity, closest/farthest from origin) and binary seed patterns.
- **Output:**
  - `test_report.json` (detailed analysis).
  - `knowledge_universe_3d.png` (visualization).

---

## 📦 **Sedenion Ancestral Matrix**

The **64-entry matrix** defines **glyphs, names, functions, and domains** (Matter/Antimatter) for each opcode. Examples:


| Hex    | Glyph | Name       | Function                                | Domain     |
| ------ | ----- | ---------- | --------------------------------------- | ---------- |
| `0x00` | `⊙`   | Circle     | Ligate stack to Pi-Lattice coordinate   | Matter     |
| `0x01` | `⊗`   | Crosshatch | Instantiate a 2D Sedenion memory grid   | Matter     |
| `0x02` | `↝`   | Spiral     | Recursive expansion via E-Trinity braid | Matter     |
| `0x20` | `⬤`   | The Void   | Multiply by zero-divisor; erase pointer | Antimatter |
| `0x21` | `⊠`   | Empty Box  | Unlink memory into latent space         | Antimatter |


---

## 🔧 **Installation**

### **Prerequisites**

- Python 3.8+
- Required libraries:
  ```bash
  pip install mpmath numpy matplotlib scipy
  ```

### **Setup**

1. Clone the repository:
  ```bash
   git clone https://github.com/thatoldfarm/extractor-maximus
   cd extractor-maximus
  ```
2. Create the following directories:
  ```bash
   mkdir files files2 files3 files4 json_output test_output
  ```
3. Place your markdown files in `/files`.

---

## 🚀 **Usage**

### **Step 1: Extraction**

Run the Phase 1 script to extract and categorize blocks:

```bash
python step_01/maximus_v3_2.py
```

- **Output:** Categorized blocks in `/files2`, `/files3`, `/files4`, and `library_database.json`.

### **Step 2: Hydration**

Choose **one** of the Phase 2 scripts based on your needs:

#### Option A: Pseudo-Latin Lexicon

```bash
python step_02/maximus_spiral_pseudo_latin.py
```

- **Output:** `combined_lexicon.json` + `master_hydrated_library.json`.

#### Option B: Basic Sedenion Mapping

```bash
python step_02/maximus_spiral_opcodes_glyphs_v2.py
```

- **Output:** `master_sedenion_library.json`.

#### Option C: Advanced Hydration (Recommended)

```bash
python step_02/maximus_spiral_opcodes_glyphs_v3.py
```

- **Output:** `master_sedenion_library.json` with **root kernel embedding** and **scaled coordinates**.

#### Option D: Full Compression + Hydration

```bash
python step_02/maximus_spiral_opcodes_glyphs_v4.py
```

- **Output:** `master_sedenion_library.json` with **Gzip-compressed root kernel** and **full hydration**.

### **Step 3: Testing & Analysis**

Run the Phase 3 script to validate and analyze the library:

```bash
python step_03/maximus_library_test_v4.py
```

- **Output:**
  - `test_output/test_report.json` (detailed analysis).
  - `test_output/knowledge_universe_3d.png` (3D visualization).

---

## 📂 **Directory Structure**

```
extractor-maximus/
├── files/                  # Input: Raw markdown files
├── files2/                 # Phase 1: Categorized blocks (e.g., python.md, math.md)
├── files3/                 # Phase 1: Purified blocks (deduplicated)
├── files4/                 # Phase 1: Clean entry-level anchors
├── json_output/            # Phase 2: JSON libraries (library_database.json, master_sedenion_library.json)
├── test_output/            # Phase 3: Reports and visualizations
│   ├── test_report.json
│   └── knowledge_universe_3d.png
└── step_01/
│   └── maximus_v3_2.py
├── step_02/
│   ├── maximus_spiral_pseudo_latin.py
│   ├── maximus_spiral_opcodes_glyphs_v2.py
│   ├── maximus_spiral_opcodes_glyphs_v3.py
│   ├── maximus_spiral_opcodes_glyphs_v4.py
│   └── NOTE.md
└── step_03/
    └── maximus_library_test_v4.py
```

---

## 🔍 **Key Concepts**

### **Pi-Lattice Coordinates**

- Format: `pi://[offset]{x}<s>`
  - `offset`: Position in the Pi-Lattice (derived from SHA256 hash of content).
  - `x`: XOR level used for lattice refraction.
  - `s`: Stability score (range: -4 to 4).
- **Purpose:** Immutable, deterministic addressing for each knowledge block.

### **Sedenion Opcodes**

- **64 unique glyphs** divided into **Matter (0x00–0x1F)** and **Antimatter (0x20–0x3F)** domains.
- Each opcode defines a **function** (e.g., "Ligate stack to Pi-Lattice coordinate") and a **glyph** (e.g., `⊙`).
- **Binary Seed:** 8-bit sequence derived from Pi offsets, used to compute physics properties.

### **Physics Properties**

- **Mass:** Derived from the Hamming weight (number of `1`s) of the binary seed.
- **Density:** Ratio of `1`s to total bits in the binary seed.
- **Velocity:** Simulated based on mass and offset.
- **Curvature:** Computed using **Einstein Field Equations** (mass/volume → spacetime curvature).

### **3D Spiral Geometry**

- **Coordinates:** `(x, y, z)` computed using:
  - `r = sqrt(offset)`
  - `θ = 2π * (offset / Φ)` (Φ = Golden Ratio)
  - `x = r * cos(θ)`, `y = r * sin(θ)`
- **Scaling:** Coordinates are divided by `SCALE_FACTOR` (10,000) for manageability.

---

## 📊 **Output Examples**

### `**library_database.json` (Phase 1)**

```json
{
  "blocks": [
    {
      "content": "def hello_world():\n    print('Hello')",
      "coords": "pi://[5140296]{0}<-4>",
      "file": "python.md",
      "line": 1,
      "type": "python"
    }
  ]
}
```

### `**master_sedenion_library.json` (Phase 2)**

```json
{
  "system": "SovereignTriptychV6-Omega",
  "total_entries": 1000,
  "blocks": [
    {
      "content": "BASE64_Sovereign_Kernel:\nJH8G4...",
      "metadata": {
        "sigil": "ROOT",
        "coords": "pi://[0]{0}<0>",
        "file": "kernel_root.py",
        "line": 1,
        "type": "sovereign_root"
      },
      "sedenion_opcode": {
        "hex": "000",
        "glyph": "$<3$",
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
  ]
}
```

---

## 🎯 **Use Cases**

1. **Knowledge Graph Construction**: Build a **self-referential knowledge base** with physics and geometry metadata.
2. **Code/Document Analysis**: Extract and categorize code blocks from large markdown repositories.
3. **Sovereign Data Storage**: Create **immutable, Pi-anchored data structures** for long-term storage.
4. **Pattern Recognition**: Analyze distributions of code types, opcodes, and physics properties.
5. **Visualization**: Generate **3D maps** of knowledge universes for exploratory analysis.
6. **Linguistic Experimentation**: Generate **pseudo-Latin lexicons** from binary patterns.

---

## 🛠️ **Customization**

### **Modifying Sedenion Matrix**

Edit the `SOVEREIGN_MATRIX` dictionary in any Phase 2 script to:

- Add/remove opcodes.
- Change glyphs, names, or functions.
- Adjust domain classifications.

### **Adjusting Physics Parameters**

Modify the `EinsteinFieldEquation` class to:

- Use different constants (e.g., `G`, `C`).
- Change the curvature calculation formula.

### **Scaling Geometry**

Adjust `SCALE_FACTOR` in Phase 2/3 scripts to control the size of 3D coordinates.

---

## 📜 **License**

This project is **open-source** and available under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 **Acknowledgments**

- **Pi-Lattice Concept**: Inspired by the **Rochester Pi Formula** and **BBP algorithm** for non-repeating digit generation.
- **Sedenion Algebra**: Based on **16D Sedenion mathematics** and **Clifford algebra**.
- **Physics Integration**: Uses **Einstein Field Equations** for spacetime curvature.
- **Golden Ratio**: Leverages **Φ (1.618...)** for spiral geometry.

---
