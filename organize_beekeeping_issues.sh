#!/data/data/com.termux/files/usr/bin/bash
set -u

REPO="caliofmarian-ai/Practical-Beekeeping-Handbook"

echo "Checking GitHub authentication..."
gh auth status >/dev/null || {
  echo "ERROR: GitHub CLI is not authenticated."
  exit 1
}

echo "Creating/updating labels..."

create_label() {
  gh label create "$1" \
    --repo "$REPO" \
    --description "$2" \
    --color "$3" \
    --force >/dev/null
}

create_label "foundation" "Repository planning, standards and project setup" "5319E7"
create_label "chapter" "Writing task belonging to a handbook chapter" "1D76DB"
create_label "biology" "Honey bee biology and colony organization" "0E8A16"
create_label "apiary-management" "Apiary planning and seasonal colony management" "2CBE4E"
create_label "equipment" "Hive systems, equipment and tools" "FBCA04"
create_label "queen-management" "Queen selection, introduction, replacement and rearing" "D93F0B"
create_label "nutrition" "Forage, pollen, water and supplemental feeding" "C2E0C6"
create_label "hive-products" "Honey, comb honey, wax and other hive products" "F9D0C4"
create_label "bee-health" "Diseases, pests, monitoring and treatments" "B60205"
create_label "food-safety" "Honey processing, hygiene and quality control" "E99695"
create_label "business" "Beekeeping business, costs, marketing and sales" "7057FF"
create_label "sustainability" "Organic practice, biodiversity and pollinator conservation" "006B75"
create_label "research" "Scientific evidence and future technologies" "BFDADC"
create_label "publishing" "Editorial, illustration, formatting and release production" "D4C5F9"
create_label "illustration" "Requires an original illustration or visual asset" "F4B400"
create_label "diagram" "Requires a process diagram, schematic or decision tree" "A2EEEF"
create_label "table" "Requires one or more structured tables" "D876E3"
create_label "checklist" "Requires a practical checklist or field procedure" "C5DEF5"
create_label "references" "Requires verified scientific or regulatory references" "EDEDED"
create_label "review-required" "Requires technical or editorial review" "FF7F50"

echo "Labels ready."

OWNER="${REPO%%/*}"
NAME="${REPO##*/}"

create_milestone() {
  local title="$1"
  local description="$2"

  local existing
  existing=$(gh api \
    --paginate \
    -H "Accept: application/vnd.github+json" \
    "/repos/$REPO/milestones?state=all&per_page=100" \
    --jq ".[] | select(.title == \"$title\") | .number" | head -n 1)

  if [ -n "$existing" ]; then
    echo "MILESTONE EXISTS: $title"
  else
    gh api \
      --method POST \
      -H "Accept: application/vnd.github+json" \
      "/repos/$REPO/milestones" \
      -f title="$title" \
      -f description="$description" >/dev/null
    echo "MILESTONE CREATED: $title"
  fi
}

echo "Creating milestones..."

create_milestone "01 — Project Foundation" "Repository setup, handbook outline, standards and visual direction."
create_milestone "02 — Foundations of Beekeeping" "Introduction, history, importance, products and modern practice."
create_milestone "03 — Bee Biology and Colony Organization" "Bee anatomy, castes, communication, behaviour and colony development."
create_milestone "04 — Apiary Planning and Equipment" "Apiary location, forage, layout, hive systems and essential equipment."
create_milestone "05 — Starting and Managing Colonies" "Obtaining bees, inspections and seasonal colony management."
create_milestone "06 — Queen Management and Nutrition" "Queen work, nectar, pollen, feeding and water."
create_milestone "07 — Honey and Hive Products" "Honey production, comb honey, wax and specialist hive products."
create_milestone "08 — Bee Health and Pest Management" "Diseases, pests, monitoring and integrated treatment strategies."
create_milestone "09 — Processing and Food Safety" "Honey hygiene, moisture, crystallization and quality control."
create_milestone "10 — Beekeeping Business" "Business planning, costs, branding, marketing and sales."
create_milestone "11 — Sustainability and Research" "Organic systems, biodiversity, pollinator conservation and future research."
create_milestone "12 — Final Production and Release" "Glossary, bibliography, visuals, editing, formats and Version 1.0."

echo "Milestones ready."

get_issue_number() {
  local title="$1"
  gh issue list \
    --repo "$REPO" \
    --state all \
    --limit 1000 \
    --json number,title \
    --jq ".[] | select(.title == \"$title\") | .number" | head -n 1
}

apply_issue() {
  local title="$1"
  local milestone="$2"
  local labels="$3"
  local number

  number=$(get_issue_number "$title")

  if [ -z "$number" ]; then
    echo "NOT FOUND: $title"
    return
  fi

  echo "UPDATE #$number: $title"

  local args=(issue edit "$number" --repo "$REPO" --milestone "$milestone")
  IFS=',' read -ra label_array <<< "$labels"

  for label in "${label_array[@]}"; do
    [ -n "$label" ] && args+=(--add-label "$label")
  done

  gh "${args[@]}" >/dev/null
}

echo "Assigning milestones and labels..."

apply_issue "Repository Structure" "01 — Project Foundation" "foundation"
apply_issue "Project README" "01 — Project Foundation" "foundation,publishing"
apply_issue "Book Outline" "01 — Project Foundation" "foundation,publishing"
apply_issue "Writing Standards" "01 — Project Foundation" "foundation,publishing,references"
apply_issue "Illustration Style Guide" "01 — Project Foundation" "foundation,publishing,illustration,diagram"

for title in \
"Introduction to Beekeeping" \
"History of Beekeeping" \
"Importance of Honey Bees" \
"Products of the Hive" \
"Modern Beekeeping"
do
  apply_issue "$title" "02 — Foundations of Beekeeping" "chapter,references"
done

for title in \
"Bee Anatomy" \
"Honey Bee Life Cycle" \
"The Queen" \
"Worker Bees" \
"Drones" \
"Communication Inside the Colony" \
"Bee Behaviour" \
"Colony Structure" \
"Seasonal Development" \
"Swarming" \
"Supersedure" \
"Colony Collapse"
do
  apply_issue "$title" "03 — Bee Biology and Colony Organization" "chapter,biology,references,diagram"
done

for title in \
"Choosing the Apiary Location" \
"Climate Considerations" \
"Water Sources" \
"Bee Forage" \
"Apiary Layout"
do
  apply_issue "$title" "04 — Apiary Planning and Equipment" "chapter,apiary-management,checklist"
done

for title in \
"Hive Types" \
"Hive Components" \
"Frames" \
"Foundation" \
"Protective Clothing" \
"Hive Tools" \
"Smokers" \
"Feeders"
do
  apply_issue "$title" "04 — Apiary Planning and Equipment" "chapter,equipment,illustration"
done

for title in \
"Buying Bees" \
"Capturing Swarms" \
"Installing Packages" \
"Nucleus Colonies" \
"First Inspection" \
"Spring Management" \
"Summer Management" \
"Autumn Management" \
"Winter Management"
do
  apply_issue "$title" "05 — Starting and Managing Colonies" "chapter,apiary-management,checklist"
done

for title in \
"Queen Selection" \
"Queen Introduction" \
"Queen Replacement" \
"Queen Rearing"
do
  apply_issue "$title" "06 — Queen Management and Nutrition" "chapter,queen-management,checklist,references"
done

for title in \
"Natural Nectar Sources" \
"Pollen" \
"Supplemental Feeding" \
"Protein Feeding" \
"Water Requirements"
do
  apply_issue "$title" "06 — Queen Management and Nutrition" "chapter,nutrition,references,table"
done

for title in \
"Honey Flow" \
"Honey Harvest" \
"Honey Extraction" \
"Honey Filtering" \
"Storage" \
"Packaging" \
"Natural Comb Production" \
"Cut Comb Honey" \
"Section Honey" \
"Wax Production" \
"Wax Processing" \
"Wax Products" \
"Propolis" \
"Royal Jelly" \
"Bee Pollen" \
"Bee Venom"
do
  apply_issue "$title" "07 — Honey and Hive Products" "chapter,hive-products,checklist"
done

for title in \
"Varroa Destructor" \
"Nosema" \
"American Foulbrood" \
"European Foulbrood" \
"Viruses" \
"Small Hive Beetle" \
"Wax Moths" \
"Monitoring" \
"Treatment Methods" \
"Organic Treatments" \
"Chemical Treatments"
do
  apply_issue "$title" "08 — Bee Health and Pest Management" "chapter,bee-health,references,review-required"
done

for title in \
"Food Safety" \
"Moisture Control" \
"Crystallization" \
"Quality Control"
do
  apply_issue "$title" "09 — Processing and Food Safety" "chapter,food-safety,checklist,references"
done

for title in \
"Starting a Beekeeping Business" \
"Equipment Costs" \
"Marketing" \
"Branding" \
"Online Sales" \
"Farmers Markets"
do
  apply_issue "$title" "10 — Beekeeping Business" "chapter,business,table"
done

for title in \
"Organic Beekeeping" \
"Biodiversity" \
"Pollinator Conservation"
do
  apply_issue "$title" "11 — Sustainability and Research" "chapter,sustainability,references"
done

for title in \
"Recent Scientific Studies" \
"Future of Beekeeping"
do
  apply_issue "$title" "11 — Sustainability and Research" "chapter,research,references,review-required"
done

apply_issue "Glossary" "12 — Final Production and Release" "publishing"
apply_issue "Bibliography" "12 — Final Production and Release" "publishing,references"
apply_issue "Appendices" "12 — Final Production and Release" "publishing,checklist,table"
apply_issue "Tables" "12 — Final Production and Release" "publishing,table"
apply_issue "Illustrations" "12 — Final Production and Release" "publishing,illustration"
apply_issue "Diagrams" "12 — Final Production and Release" "publishing,diagram"
apply_issue "Photographs" "12 — Final Production and Release" "publishing,illustration"
apply_issue "Index" "12 — Final Production and Release" "publishing"
apply_issue "Technical Review" "12 — Final Production and Release" "publishing,review-required"
apply_issue "Language Review" "12 — Final Production and Release" "publishing,review-required"
apply_issue "Formatting" "12 — Final Production and Release" "publishing"
apply_issue "PDF Edition" "12 — Final Production and Release" "publishing"
apply_issue "EPUB Edition" "12 — Final Production and Release" "publishing"
apply_issue "Print Edition" "12 — Final Production and Release" "publishing"
apply_issue "Version 1.0 Release" "12 — Final Production and Release" "publishing,review-required"

echo
echo "=========================================="
echo "Labels, milestones and assignments finished."
echo "Issues: https://github.com/$REPO/issues"
echo "Milestones: https://github.com/$REPO/milestones"
echo "=========================================="
