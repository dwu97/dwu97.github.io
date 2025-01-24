import markdown
import argparse
import os

def convert_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            print(md_content)  # Print inside the with block to ensure content is read
        # Convert markdown to HTML using python-markdown package
        html_content = markdown.markdown(md_content)
        print(html_content)
        
        # Get the directory of the output file
        output_dir = os.path.dirname(output_file)
        css_file = os.path.join(output_dir, 'styles.css')
        
        # Wrap in basic HTML structure with CSS link
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{input_file}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
{html_content}
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(full_html)
            
        # Copy styles.css to output directory if it doesn't exist
        if not os.path.exists(css_file):
            with open('styles.css', 'r') as css_src, open(css_file, 'w') as css_dest:
                css_dest.write(css_src.read())
                
        print(f"Successfully converted {input_file} to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Markdown file to HTML')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('output_file', help='Path to the output HTML file')
    
    args = parser.parse_args()
    
    convert_file(args.input_file, args.output_file)


    # To use this script:
    # 1. Save your markdown content in a .md file (e.g., index.md)
    # 2. Run the script from command line:
    #    python mdtohtml.py input.md output.html
    # 3. The script will:
    #    - Read the input markdown file
    #    - Convert it to HTML
    #    - Wrap it in a basic HTML template
    #    - Save the result to the output file
    # Example usage:
    # python mdtohtml.py index.md index.html

