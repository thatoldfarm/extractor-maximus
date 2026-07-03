import os
import hashlib
import math
import re
import json
from collections import defaultdict

try:
    from mpmath import mp
except ImportError:
    print("❌ ERROR: 'mpmath' library not found. Please run: pip install mpmath")
    exit(1)

class SovereignTriptychV3:
    def __init__(self):
        # Directory Structure
        self.input_dir = "files"
        self.stage_dir = "files2"
        self.final_dir = "files3"
        self.ultimate_dir = "files4"
        self.json_dir = "json_output"
        
        print("⚙️ Initializing Pi-Lattice Substrate V3.2...")
        mp.dps = 10**6 + 10
        self.pi_digits = mp.nstr(mp.pi, 10**6 + 1, strip_zeros=False)[2:2 + 10**6]
        self.lattice = bytearray([int((abs(math.sin(i)) * 10**8) % 256) for i in range(5 * 10**6)])
        
        self.lang_map = {
            "py": "python", "python": "python",
            "js": "javascript", "javascript": "javascript", 
            "ts": "typescript", "typescript": "typescript",
            "asm": "assembly", "assembly": "assembly",
            "fth": "forth", "forth": "forth",
            "sh": "bash", "bash": "bash",
            "md": "markdown", "markdown": "markdown",
            "txt": "text", "text": "text", "plaintext": "text",
            "math": "math", "equation": "equation",
            "eml": "eml", "tensor": "tensor",
            "latex": "latex", "tex": "latex"
        }

    def generate_pi_anchor(self, data):
        try:
            p = int(hashlib.sha256(data).hexdigest(), 16) % len(self.pi_digits)
            x, s = 0, 0
            if len(data) >= 3:
                mid = len(data) // 2
                codon = data[mid:mid+3]
                for xor_level in range(256):
                    refracted = bytearray([b ^ xor_level for b in codon])
                    pos = self.lattice.find(refracted)
                    if pos != -1:
                        x, s = xor_level, (xor_level % 9) - 4
                        break
            return f"pi://[{p}]{{ {x} }}<{s}>"
        except Exception as e:
            return f"pi://[ERR]{{0}}<0> ({str(e)})"

    def get_file_coords(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return self.generate_pi_anchor(f.read())
        except Exception as e:
            return f"pi://[ERR]{{0}}<0> ({str(e)})"

    def clean_math_expression(self, expr):
        if not expr: return expr
        expr = expr.replace('\\$', '$')
        expr = re.sub(r'\\text\{([^}]*)\}', lambda m: f'\\text{{{m.group(1).replace("_", chr(92) + "_")}}}', expr)
        return expr.strip()

    def extract_all_blocks(self, content):
        blocks = []
        lines = content.splitlines()
        
        sources = []
        for idx, line in enumerate(lines):
            for match in re.finditer(r'<!--\s*Source\s*:(.*?)\s*-->', line):
                sources.append((idx, match.group(1).strip()))
        
        code_blocks = []
        inside_code = False
        temp_source = "Unknown Source"
        temp_lang = "text"
        code_start_line = 0
        
        for idx, line in enumerate(lines):
            if not inside_code and line.strip().startswith("<!-- Source:"):
                temp_source = line.strip()
            
            if line.strip().startswith("```"):
                if not inside_code:
                    inside_code = True
                    code_start_line = idx
                    tag = line.strip()[3:].strip().lower()
                    temp_lang = self.lang_map.get(tag, tag if tag else "text")
                else:
                    inside_code = False
                    code_blocks.append((code_start_line, idx, temp_source, temp_lang))

        def resolve_source_and_line(line_idx):
            applicable = [s for idx, s in sources if idx < line_idx]
            if not applicable: return "Unknown Source", 0
            src_text = applicable[-1]
            src_line = next(idx for idx, s in sources if s == src_text)
            return src_text, src_line

        full_text = "\n".join(lines)
        patterns = [
            (r'\$\$(.*?)\$\$', "display_math", re.DOTALL),
            (r'(?<!\\)\$(?!\\$)(.*?)(?<!\\$)\$(?!\\)', "inline_math", 0),
            (r'\\\[(.*?)\\\]', "latex_display", re.DOTALL),
            (r'\\\((.*?)\\\)', "latex_inline", 0),
            (r'\[EML\](.*?)\s*\[/EML\]', "eml_block", re.DOTALL),
            (r'\[TENSOR\](.*?)\s*\[/TENSOR\]', "tensor_block", re.DOTALL),
        ]

        for pattern, block_type, flags in patterns:
            for match in re.finditer(pattern, full_text, flags=flags):
                math_content = self.clean_math_expression(match.group(1))
                if math_content:
                    line_num = full_text.count('\n', 0, match.start()) + 1
                    source, s_line = resolve_source_and_line(line_num)
                    blocks.append((source, block_type, math_content, line_num))

        for start, end, src, lang in code_blocks:
            block_text = "\n".join(lines[start+1:end])
            source, s_line = resolve_source_and_line(start)
            blocks.append((source, lang, block_text, start + 1))

        return blocks

    def run_phase_1(self):
        if not os.path.exists(self.input_dir): return False
        print(f"🚀 Phase 1: Extracting to {self.stage_dir}...")
        if not os.path.exists(self.stage_dir): os.makedirs(self.stage_dir)
        
        all_files = []
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith(".md"): all_files.append(os.path.join(root, file))
        all_files.sort()
        
        for full_path in all_files:
            file_name = os.path.basename(full_path)
            coords = self.get_file_coords(full_path)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                all_blocks = self.extract_all_blocks(content)
                for source_val, block_type, block_content, line_num in all_blocks:
                    if not block_content.strip(): continue
                    
                    if block_type in ["display_math", "inline_math", "latex_display", "latex_inline"]:
                        out_lang, wrapper = "math", f"${block_content}$"
                    elif block_type == "eml_block":
                        out_lang, wrapper = "eml", f"[EML]\n{block_content}\n[/EML]"
                    elif block_type == "tensor_block":
                        out_lang, wrapper = "tensor", f"[TENSOR]\n{block_content}\n[/TENSOR]"
                    else:
                        out_lang, wrapper = block_type, f"```{block_type}\n{block_content}\n```"
                    
                    out_path = os.path.join(self.stage_dir, f"{out_lang}.md")
                    source_tag = f"<!-- Source: {source_val if source_val else 'Unknown'} | Line: {line_num} | {coords}/{file_name} -->"
                    with open(out_path, 'a', encoding='utf-8') as f_out:
                        f_out.write(f"{source_tag}\n{wrapper}\n\n")
            except Exception as e: print(f"  ⚠️ Error {file_name}: {e}")
        return True

    def run_phase_2(self):
        print(f"💎 Phase 2: Purifying to {self.final_dir}...")
        if not os.path.exists(self.final_dir): os.makedirs(self.final_dir)
        
        for lang_file in sorted(os.listdir(self.stage_dir)):
            if not lang_file.endswith(".md"): continue
            lang = lang_file.replace(".md", "")
            with open(os.path.join(self.stage_dir, lang_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = content.split('\n\n')
            seen_hashes, unique_blocks = set(), []
            for chunk in chunks:
                lines = chunk.splitlines()
                if len(lines) >= 2:
                    source, block_content = lines[0], "\n".join(lines[1:])
                    clean_content = block_content.strip().strip('`').strip('$').strip('[EML]').strip('[/EML]').strip('[TENSOR]').strip('[/TENSOR]')
                    block_hash = hashlib.sha256(clean_content.encode()).hexdigest()
                    if block_hash not in seen_hashes:
                        unique_blocks.append((source, block_content))
                        seen_hashes.add(block_hash)
            
            with open(os.path.join(self.final_dir, f"{lang}.md"), 'w', encoding='utf-8') as f_final:
                for source, block in unique_blocks:
                    f_final.write(f"{source}\n{block}\n\n")

    def run_phase_3(self):
        """
        PHASE 3: CLEAN ENTRY-LEVEL ADDRESSING.
        Replaces recursive paths with clean type references (e.g., math.md).
        """
        print(f"🌌 Phase 3: Creating Clean Anchors in {self.ultimate_dir}...")
        if not os.path.exists(self.ultimate_dir): os.makedirs(self.ultimate_dir)

        for lang_file in sorted(os.listdir(self.final_dir)):
            if not lang_file.endswith(".md"): continue
            with open(os.path.join(self.final_dir, lang_file), 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = content.split('\n\n')
            ultimate_entries = []

            for chunk in chunks:
                lines = chunk.splitlines()
                if len(lines) >= 2:
                    old_source = lines[0]
                    block_content = "\n".join(lines[1:])
                    entry_coords = self.generate_pi_anchor(block_content.encode('utf-8'))
                    
                    # EXTRACT LINE NUMBER from old_source to preserve it for JSON
                    line_match = re.search(r'Line: (\d+)', old_source)
                    line_info = f" (Line: {line_match.group(1)})" if line_match else ""
                    
                    # CLEAN REFERENCE: Only Use EntryCoord and the current filename (type)
                    new_source_tag = f"<!-- Source: {entry_coords} | {lang_file}{line_info} -->"
                    ultimate_entries.append(f"{new_source_tag}\n{block_content}\n\n")

            with open(os.path.join(self.ultimate_dir, lang_file), 'w', encoding='utf-8') as f_ult:
                f_ult.writelines(ultimate_entries)

    def export_to_json(self, output_dir="json_output"):
        print(f"📦 Exporting to JSON in {output_dir}...")
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        
        all_data = {"blocks": []}
        if not os.path.exists(self.ultimate_dir): return

        for lang_file in sorted(os.listdir(self.ultimate_dir)):
            if not lang_file.endswith(".md"): continue
            lang = lang_file.replace(".md", "")
            
            with open(os.path.join(self.ultimate_dir, lang_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = content.split('\n\n')
            for chunk in chunks:
                lines = chunk.splitlines()
                if len(lines) >= 2:
                    tag_line = lines[0]
                    block_content = "\n".join(lines[1:])
                    
                    # Updated Regex for Clean tags
                    entry_coord_match = re.search(r'(pi://\[\d+\]\{ \d+ \}<\-?\d+>)', tag_line)
                    line_match = re.search(r'Line: (\d+)', tag_line)
                    
                    # The 'file' is now the lang_file (e.g., math.md)
                    all_data["blocks"].append({
                        "content": block_content,
                        "coords": entry_coord_match.group(1) if entry_coord_match else "N/A",
                        "file": lang_file,
                        "line": int(line_match.group(1)) if line_match else 0,
                        "type": lang
                    })

        output_path = os.path.join(output_dir, "library_database.json")
        with open(output_path, "w", encoding="utf-8") as f_json:
            json.dump(all_data, f_json, indent=4)
        print(f"✅ JSON database exported to {output_path}")

    def execute(self):
        if self.run_phase_1():
            self.run_phase_2()
            self.run_phase_3()
            self.export_to_json()
            print("\n✨ TOTAL SUCCESS: Clean Entry-Level Crystallization complete.")
        else:
            print("\n❌ PIPELINE ABORTED.")

if __name__ == "__main__":
    engine = SovereignTriptychV3()
    engine.execute()
