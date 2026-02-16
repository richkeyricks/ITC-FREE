import re
import subprocess
import sys
import os

def parse_release_notes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by separator
    blocks = content.split('---')
    releases = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # Extract title and version
        # Format: # 🚀 Title vX.X.X (Date)
        title_match = re.search(r'^# (.*v(\d+\.\d+\.\d+).*)', block, re.MULTILINE)
        if title_match:
            full_title = title_match.group(1).strip()
            version_tag = "v" + title_match.group(2).strip()
            
            # The body is everything after the title line
            body = block.replace(f"# {full_title}", "", 1).strip()
            
            releases.append({
                'tag': version_tag,
                'title': full_title,
                'body': body
            })
    
    # Sort by version (simple string sort might fail for 4.10 vs 4.9, but here we have standard formatting)
    # Better to sort by version components
    def version_key(r):
        v = r['tag'].lstrip('v')
        return [int(x) for x in v.split('.')]

    releases.sort(key=version_key)
    return releases

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python publish_releases.py <path_to_notes.md>")
        sys.exit(1)

    notes_path = sys.argv[1]
    releases = parse_release_notes(notes_path)

    print(f"Found {len(releases)} releases to publish.")

    cwd = os.getcwd()
    
    # Create temp directory for notes
    temp_dir = "temp_release_notes"
    os.makedirs(temp_dir, exist_ok=True)

    for release in releases:
        tag = release['tag']
        title = release['title']
        body = release['body']
        
        print(f"\nProcessing {tag}...")

        # 1. Create/Update Git Tag (local)
        print(f"Force updating git tag {tag}...")
        # Always force tag to current HEAD to fix any history/secret issues
        if run_command(f"git tag -f {tag}", cwd) is None:
            continue
            
        # 2. Push Tag
        print(f"Pushing tag {tag} to itc-free...")
        if run_command(f"git push itc-free {tag}", cwd) is None:
            print(f"Failed to push tag {tag}. Skipping release.")
            continue

        # 3. Create Release
        # write body to temp file to avoid CLI escaping issues
        note_file = os.path.join(temp_dir, f"{tag}.md")
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(body)
        
        print(f"Creating GitHub release for {tag} on richkeyricks/ITC-FREE...")
        # Check if release exists
        check_release = run_command(f"gh release view {tag} -R richkeyricks/ITC-FREE", cwd)
        if check_release: # Release exists
             print(f"Release {tag} already exists on ITC-FREE. Skipping.")
        else:
            cmd = f'gh release create {tag} -R richkeyricks/ITC-FREE --title "{title}" --notes-file "{note_file}"'
            if run_command(cmd, cwd) is None:
                print(f"Failed to create release {tag}.")
            else:
                print(f"Successfully published {tag}!")

    # Cleanup
    # import shutil
    # shutil.rmtree(temp_dir)
    print("\nDone!")

if __name__ == "__main__":
    main()
