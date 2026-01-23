#!/bin/bash
# convert_with_links.sh - Convert MD to HTML with cross-document linking
# Strips edit logs, converts [DOC:X] and [TERM:X] to hyperlinks

set -e

BASE_DIR="/home/user/CCASH/Series Docs"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted/HTML"
TEMP_DIR="$BASE_DIR/OUTPUT/.temp_convert"

# Clean and create directories
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo "=== CCASH Document Conversion with Cross-Linking ==="
echo ""

# Document code to path mapping
declare -A DOC_PATHS=(
    ["A1"]="Company/Formation/A1_Articles_of_Organization"
    ["A2"]="Client_Series/Formation/A2_Exhibit_A_Series_List"
    ["A3"]="Client_Series/Formation/A3_Exhibit_B_Series_Operating_Agreements"
    ["B1"]="Company/Governance/B1_Master_Operating_Agreement"
    ["B2"]="Company/Governance/B2_Officer_Appointment_Resolution"
    ["B3"]="Company/Governance/B3_Officer_Rotation_Succession_Policy"
    ["B4"]="Company/Compliance/B4_Record_Keeping_Policy"
    ["B5"]="Company/Compliance/B5_BSA_AML_Program"
    ["B6"]="Company/Compliance/B6_IT_Security_Incident_BCP_DRP"
    ["B7"]="Company/Compliance/B7_Acceptable_Client_Use_Policy"
    ["B8"]="Company/Compliance/B8_Privacy_Data_Protection_Policy"
    ["B9"]="Company/Compliance/B9_Fit_and_Proper_Screening_Policy"
    ["B10"]="Company/Governance/B10_Insurance_and_Capital_Policy"
    ["B11"]="Client_Series/Client/B11_Client_Services_and_Licensing_Framework"
    ["B12"]="Company/Compliance/B12_Partner_Due_Diligence_Standard"
    ["C1"]="Internal/Registration/C1_ABN_Registration_CCASH"
    ["C2"]="Internal/Registration/C2_ABN_Template_Client_Series"
    ["C3"]="Internal/Registration/C3_Pricing_and_Routing_Schedule"
    ["D1"]="Client_Series/Formation/D1_Articles_of_Amendment_Add_Series"
    ["E1"]="Internal/Checklist/E1_Filing_Checklist_and_Instructions"
    ["E2"]="Internal/Checklist/E2_Securities_and_MTL_Checklist"
    ["F1"]="Client_Series/Client/F1_Client_Services_Agreement"
    ["F2"]="Client_Series/Client/F2_End_Customer_Terms_Template"
    ["N1"]="Client_Series/Schedule/N1_Partner_MSB_Agreement"
    ["N3"]="Client_Series/Schedule/N3_Approved_States_Schedule"
    ["N4"]="Client_Series/Schedule/N4_Partner_MSB_Directory"
    ["N5"]="Client_Series/Schedule/N5_Client_FinCEN_Filing_Guide"
    ["00_README"]="Company/Overview/00_README"
    ["00_Business_Model"]="Company/Overview/00_Business_Model"
)

# Document titles
declare -A DOC_TITLES=(
    ["A1"]="Articles of Organization"
    ["A2"]="Exhibit A — Series List"
    ["A3"]="Exhibit B — Series Operating Agreements"
    ["B1"]="Master Operating Agreement"
    ["B2"]="Officer Appointment Resolution"
    ["B3"]="Officer Rotation & Succession Policy"
    ["B4"]="Record Keeping Policy"
    ["B5"]="BSA/AML Program"
    ["B6"]="IT Security / BCP / DRP"
    ["B7"]="Acceptable Client Use Policy"
    ["B8"]="Privacy & Data Protection Policy"
    ["B9"]="Fit & Proper Screening Policy"
    ["B10"]="Insurance & Capital Policy"
    ["B11"]="Client Services Framework"
    ["B12"]="Partner Due Diligence Standard"
    ["C1"]="ABN Registration (CCASH)"
    ["C2"]="ABN Template (Client Series)"
    ["C3"]="Pricing & Routing Schedule"
    ["D1"]="Articles of Amendment"
    ["E1"]="Filing Checklist"
    ["E2"]="Securities & MTL Checklist"
    ["F1"]="Client Services Agreement"
    ["F2"]="End Customer Terms"
    ["N1"]="Partner MSB Agreement"
    ["N3"]="Approved States Schedule"
    ["N4"]="Partner MSB Directory"
    ["N5"]="FinCEN Filing Guide"
    ["00_README"]="Document Overview"
    ["00_Business_Model"]="Business Model"
)

# Version log file
VERSION_LOG="$TEMP_DIR/version_log.md"
echo "# Version History Log" > "$VERSION_LOG"
echo "" >> "$VERSION_LOG"
echo "Generated: $(date '+%Y-%m-%d %H:%M')" >> "$VERSION_LOG"
echo "" >> "$VERSION_LOG"
echo "| Document | Version | Last Updated | Git Hash |" >> "$VERSION_LOG"
echo "|----------|---------|--------------|----------|" >> "$VERSION_LOG"

# Process each document
process_document() {
    local src="$1"
    local doccode="$2"
    local outpath="${DOC_PATHS[$doccode]}"
    
    if [[ -z "$outpath" ]]; then
        echo "  WARNING: No path mapping for $doccode"
        return
    fi
    
    local outdir="$OUTPUT_DIR/$(dirname "$outpath")"
    local outfile="$OUTPUT_DIR/${outpath}.html"
    local tempmd="$TEMP_DIR/${doccode}.md"
    
    mkdir -p "$outdir"
    
    # Get git info
    local git_hash=$(cd "$BASE_DIR" && git log -1 --format="%h" -- "$src" 2>/dev/null || echo "N/A")
    local git_date=$(cd "$BASE_DIR" && git log -1 --format="%cs" -- "$src" 2>/dev/null || echo "N/A")
    
    # Extract version from file
    local version=$(grep -oP 'Version[:\s]+\K[0-9]+\.[0-9]+' "$src" 2>/dev/null | head -1 || echo "1.0")
    
    # Add to version log
    echo "| $doccode | $version | $git_date | $git_hash |" >> "$VERSION_LOG"
    
    # Copy and clean the markdown
    cp "$src" "$tempmd"
    
    # Remove VERSION HISTORY sections (everything from "VERSION HISTORY" or "Version History" to next ##)
    sed -i '/^##\s*VERSION HISTORY/,/^##[^#]/{ /^##[^#]/!d; }' "$tempmd"
    sed -i '/^##\s*Version History/,/^##[^#]/{ /^##[^#]/!d; }' "$tempmd"
    
    # Remove schema comments
    sed -i '/^<!--.*schema:/d' "$tempmd"
    sed -i '/^<!--.*Cross-references:/d' "$tempmd"
    sed -i '/^<!--.*\[FLOW:/d' "$tempmd"
    sed -i '/^<!--.*REMEDIATED/d' "$tempmd"
    
    # Remove CHANGELOG/Edit sections at end of file
    sed -i '/^##\s*CHANGELOG/,$d' "$tempmd"
    sed -i '/^##\s*Edit Log/,$d' "$tempmd"
    sed -i '/^##\s*Revision History/,$d' "$tempmd"
    
    # Calculate relative path depth for this document
    local depth=$(echo "$outpath" | tr -cd '/' | wc -c)
    local prefix=""
    for ((i=0; i<depth; i++)); do prefix="../$prefix"; done
    
    # Convert [DOC:X] markers to links
    for code in "${!DOC_PATHS[@]}"; do
        local target_path="${DOC_PATHS[$code]}"
        local title="${DOC_TITLES[$code]}"
        # Replace [DOC:X] with linked version
        sed -i "s|\[DOC:${code}\]|[${code}](${prefix}${target_path}.html \"${title}\")|g" "$tempmd"
    done
    
    # Convert [TERM:X] markers - just strip the marker syntax, keep the text
    sed -i 's/\[TERM:\([^]]*\)\]/\1/g' "$tempmd"
    
    # Convert [OBL:X] markers - strip
    sed -i 's/\[OBL:\([^]]*\)\]/\1/g' "$tempmd"
    
    # Convert [FLOW:X] markers - strip  
    sed -i 's/\[FLOW:\([^]]*\)\]/\1/g' "$tempmd"
    
    # Convert to HTML with pandoc
    pandoc "$tempmd" \
        -f markdown \
        -t html5 \
        --standalone \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --metadata title="${DOC_TITLES[$doccode]:-$doccode}" \
        -o "$outfile"
    
    echo "  ✓ $doccode → $(basename "$outfile")"
}

# Find and process all documents
echo "Converting documents..."
echo ""

cd "$BASE_DIR"

# Company documents
for f in Company/Overview/*.md Company/Formation/*.md Company/Governance/*.md Company/Compliance/*.md; do
    [[ -f "$f" ]] || continue
    basename_noext=$(basename "$f" .md)
    # Handle 00_ prefix files specially
    if [[ "$basename_noext" == 00_* ]]; then
        code="$basename_noext"
    else
        code=$(echo "$basename_noext" | sed 's/_.*$//')
    fi
    process_document "$f" "$code"
done

# Client Series documents  
for f in Client_Series/Client/*.md Client_Series/Formation/*.md Client_Series/Schedule/*.md; do
    [[ -f "$f" ]] || continue
    code=$(basename "$f" .md | sed 's/_.*$//')
    process_document "$f" "$code"
done

# Internal documents
for f in Internal/Checklist/*.md Internal/Registration/*.md; do
    [[ -f "$f" ]] || continue
    code=$(basename "$f" .md | sed 's/_.*$//')
    process_document "$f" "$code"
done

echo ""
echo "=== Conversion Complete ==="
echo "Output: $OUTPUT_DIR"

# Cleanup temp
rm -rf "$TEMP_DIR"
