#!/data/data/com.termux/files/usr/bin/bash
set -e
REPO="caliofmarian-ai/Practical-Beekeeping-Handbook"
create_issue(){
gh issue create --repo "$REPO" --title "$1" --body "$2" >/dev/null || true
}
create_issue "Repository Structure" "Create and organize the complete repository structure."
create_issue "Project README" "Create the main README with project description."
create_issue "Book Outline" "Finalize the complete table of contents."
create_issue "Writing Standards" "Define writing, formatting and citation standards."
create_issue "Illustration Style Guide" "Define illustration and diagram style."
for i in $(seq 6 110); do
 create_issue "Book Task #$i" "Placeholder task. Replace later with the detailed description."
done
echo "Done: https://github.com/$REPO/issues"
