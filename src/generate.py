import os
import shutil
import re
from pathlib import Path
from nodeconversion import *

def clean_dir_content(dir):
    for entry in os.listdir(dir):
        path = os.path.join(dir, entry)
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def tree_copy(source, target):
    copied_files = []
    if not os.path.exists(target):
        os.makedirs(target)
    # no implicit cleaning anymore, will be explicit
    # clean_dir_content(target)
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        target_root = os.path.join(target, rel_path) if rel_path != '.' else target
        if not os.path.exists(target_root):
            os.makedirs(target_root)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)
            copied_files.append(f"(src:{src_file}, target:{dst_file})")
    return copied_files

def extract_title(markdown):
    m = re.search(r"^# (.*?)$", markdown, re.MULTILINE)
    if m is None:
        raise Exception("No header in this file, I can't extract a title from it")
    return m.group(1)

def generate_page(from_path, template_path, dest_path):
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()
    html_markdown = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_out = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html_markdown)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Ensure parent dirs exist
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    return f"Generating page from {from_path} to {dest_path} using {template_path}"

def generate_site(source_dir, template, target_dir):
    log = []
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        target_root = os.path.join(target_dir, rel_path) if rel_path != '.' else target_dir
        if not os.path.exists(target_root):
            os.makedirs(target_root)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, f"{Path(file).stem}.html")
            gen_log = generate_page(src_file, template, dst_file)
            log.append( gen_log )
    return log