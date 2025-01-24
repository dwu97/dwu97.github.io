import markdown
import os
from pathlib import Path
import shutil

# Global HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="layout-menu">
        <ul>
            {menu_items}
        </ul>
    </div>
    <div id="layout-content">
        {content}
    </div>
</body>
</html>"""

def convert_md_to_html(md_content, title, menu_items):
    """Convert markdown content to HTML with template"""
    html_content = markdown.markdown(md_content)
    # Replace single '-' with <br> for line breaks
    html_content = '\n'.join(
        f'<br>{line[1:]}' if line.startswith('-') else line
        for line in html_content.split('\n')
    )
    return HTML_TEMPLATE.format(
        title=title,
        menu_items=menu_items,
        content=html_content
    )

def generate_menu_items(pages):
    """Generate menu items for all pages"""
    menu_items = []
    for page in pages:
        name = os.path.splitext(page)[0]
        display_name = "Home" if name == "index" else name.capitalize()
        menu_items.append(
            f'<li><a href="{name}.html">{display_name}</a></li>'
        )
    return '\n'.join(menu_items)

def process_md_files():
    """Process all markdown files in ./md directory"""
    md_dir = Path('./src/md')
    output_dir = Path('./src/html')  # Changed back to html directory
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Get all markdown files
    md_files = list(md_dir.glob('*.md'))
    if not md_files:
        print("No markdown files found in ./md directory")
        return
    
    # Generate menu items for all pages
    pages = [f.stem for f in md_files]
    menu_items = generate_menu_items(pages)
    
    # Process each markdown file
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert to HTML
            html_file = output_dir / f"{md_file.stem}.html"
            html_content = convert_md_to_html(
                md_content,
                md_file.stem.capitalize(),
                menu_items
            )
            
            # Write HTML file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Converted {md_file} to {html_file}")
            
        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")
    
    # Copy styles.css to output directory
    css_file = output_dir / 'styles.css'
    if not css_file.exists():
        try:
            shutil.copy('styles.css', css_file)
            print("Copied styles.css to output directory")
        except Exception as e:
            print(f"Error copying styles.css: {str(e)}")

if __name__ == "__main__":
    process_md_files()

# How to use this script:
# 1. Create a directory named 'md' in the same folder as this script
# 2. Place your markdown files (.md) in the 'md' directory
#    - The first file should be named 'index.md' (this will be your homepage)
#    - Other files can be named anything (e.g., about.md, projects.md)
# 3. Run the script:
#    python mdtohtml.py
# 4. The script will:
#    - Convert all markdown files to HTML in the html directory
#    - Create a navigation menu linking all pages
#    - Copy styles.css to the html directory
# 5. Open the generated HTML files in your browser:
#    - Start with index.html
#    - Use the menu to navigate between pages
# 6. To add new pages:
#    - Add new markdown files to the 'md' directory
#    - Re-run the script
#    - The new pages will automatically appear in the menu
