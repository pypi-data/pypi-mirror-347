import argparse
import os
import yaml
from jinja2 import Template

def render_jinja_to_yaml(jinja_file, yaml_file, output_file=None):
    try:
        # Load YAML variables
        with open(yaml_file) as file:
            variables = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: YAML file '{yaml_file}' does not exist.")
        return 1  # Error code 1: YAML file not found

    # Check if jinja_file is a directory
    if os.path.isdir(jinja_file):
        if "template" in variables:
            template_name = f"{variables['template']}.yaml.j2"
            found_template = None
            # Search for the template in the directory and subdirectories
            for root, _, files in os.walk(jinja_file):
                if template_name in files:
                    found_template = os.path.join(root, template_name)
                    break
            if found_template:
                jinja_file = found_template
            else:
                print(f"Error: Template '{template_name}' not found in directory '{jinja_file}' or its subdirectories.")
                return 2  # Error code 2: Template not found in directory
        else:
            print(f"Error: 'template' key not found in YAML file. Cannot determine template file from directory '{jinja_file}'.")
            return 3  # Error code 3: 'template' key missing in YAML file

    try:
        # Load Jinja2 template
        with open(jinja_file) as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: Jinja2 file '{jinja_file}' does not exist.")
        return 4  # Error code 4: Jinja2 file not found

    if output_file:
        print(f"* rendering '{jinja_file}' with YAML file '{yaml_file}' into '{output_file}'")

    try:
        # Render template with variables
        template = Template(template_content)
        rendered_content = template.render(variables)
    except Exception as e:
        print(f"Error: Failed to render template '{jinja_file}' with variables from '{yaml_file}': {e}")
        return 5  # Error code 5: Template rendering failed

    # Output to file or stdout
    if output_file:
        try:
            # Get the file permissions of the Jinja file
            jinja_permissions = os.stat(jinja_file).st_mode

            # Write the rendered content to the output file
            with open(output_file, 'w') as file:
                file.write(rendered_content)
            
            # Apply the same permissions as the Jinja file to the output file
            os.chmod(output_file, jinja_permissions)
            
            print(f"* rendered {jinja_file} -> {output_file} using {yaml_file}")
        except Exception as e:
            print(f"Error writing to output file '{output_file}': {e}")
            return 6  # Error code 6: Failed to write to output file
    else:
        print(rendered_content)

    return 0  # Success

def main():
    parser = argparse.ArgumentParser(description="Render a Jinja2 file with YAML variables.")
    parser.add_argument("jinja_file", help="Path to the Jinja2 template file or directory where to find 'template'.")
    parser.add_argument("yaml_file", help="Path to the YAML file with variables.")
    parser.add_argument("--output", "-o", help="File to write rendered output. Prints to stdout if not specified.")
    
    args = parser.parse_args()
    exit_code = render_jinja_to_yaml(args.jinja_file, args.yaml_file, args.output)
    exit(exit_code)  # Exit with the appropriate error code
    
if __name__ == "__main__":
    main()
