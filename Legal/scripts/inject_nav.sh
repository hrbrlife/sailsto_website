#!/bin/bash
# inject_nav.sh - Inject navigation sidebar into all HTML documents

HTML_DIR="/home/user/CCASH/Series Docs/OUTPUT/Converted/HTML"
cd "$HTML_DIR"

echo "=== Injecting Navigation Sidebar ==="

# Navigation HTML template (we'll calculate relative paths per file)
generate_nav() {
    local depth=$1
    local prefix=""
    for ((i=0; i<depth; i++)); do prefix="../$prefix"; done
    
    cat << NAVEOF
<nav class="nav-sidebar">
  <div class="nav-header">
    <a href="${prefix}index.html">📋 CCASH Legal Docs</a>
  </div>

  <div class="nav-section">
    <div class="nav-section-title">🏢 Company</div>
    
    <div class="nav-group">
      <div class="nav-group-title">Overview</div>
      <a class="nav-link" href="${prefix}Company/Overview/00_README.html"><span class="doc-code">README</span>Overview</a>
      <a class="nav-link" href="${prefix}Company/Overview/00_Business_Model.html"><span class="doc-code">BMODEL</span>Business Model</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Formation</div>
      <a class="nav-link" href="${prefix}Company/Formation/A1_Articles_of_Organization.html"><span class="doc-code">A1</span>Articles of Org</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Governance</div>
      <a class="nav-link" href="${prefix}Company/Governance/B1_Master_Operating_Agreement.html"><span class="doc-code">B1</span>Master Op Agree</a>
      <a class="nav-link" href="${prefix}Company/Governance/B2_Officer_Appointment_Resolution.html"><span class="doc-code">B2</span>Officer Appt</a>
      <a class="nav-link" href="${prefix}Company/Governance/B3_Officer_Rotation_Succession_Policy.html"><span class="doc-code">B3</span>Rotation Policy</a>
      <a class="nav-link" href="${prefix}Company/Governance/B10_Insurance_and_Capital_Policy.html"><span class="doc-code">B10</span>Insurance/Capital</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Compliance</div>
      <a class="nav-link" href="${prefix}Company/Compliance/B4_Record_Keeping_Policy.html"><span class="doc-code">B4</span>Record Keeping</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B5_BSA_AML_Program.html"><span class="doc-code">B5</span>BSA/AML</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B6_IT_Security_Incident_BCP_DRP.html"><span class="doc-code">B6</span>IT/BCP/DRP</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B7_Acceptable_Client_Use_Policy.html"><span class="doc-code">B7</span>Client Use</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B8_Privacy_Data_Protection_Policy.html"><span class="doc-code">B8</span>Privacy</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B9_Fit_and_Proper_Screening_Policy.html"><span class="doc-code">B9</span>Screening</a>
      <a class="nav-link" href="${prefix}Company/Compliance/B12_Partner_Due_Diligence_Standard.html"><span class="doc-code">B12</span>Partner DD</a>
    </div>
  </div>

  <div class="nav-section">
    <div class="nav-section-title">👥 Client Series</div>
    
    <div class="nav-group">
      <div class="nav-group-title">Formation</div>
      <a class="nav-link" href="${prefix}Client_Series/Formation/A2_Exhibit_A_Series_List.html"><span class="doc-code">A2</span>Series List</a>
      <a class="nav-link" href="${prefix}Client_Series/Formation/A3_Exhibit_B_Series_Operating_Agreements.html"><span class="doc-code">A3</span>Series Op Agree</a>
      <a class="nav-link" href="${prefix}Client_Series/Formation/D1_Articles_of_Amendment_Add_Series.html"><span class="doc-code">D1</span>Amend Series</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Client</div>
      <a class="nav-link" href="${prefix}Client_Series/Client/B11_Client_Services_and_Licensing_Framework.html"><span class="doc-code">B11</span>Client Framework</a>
      <a class="nav-link" href="${prefix}Client_Series/Client/F1_Client_Services_Agreement.html"><span class="doc-code">F1</span>Client Agree</a>
      <a class="nav-link" href="${prefix}Client_Series/Client/F2_End_Customer_Terms_Template.html"><span class="doc-code">F2</span>End Customer</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Schedules</div>
      <a class="nav-link" href="${prefix}Client_Series/Schedule/N1_Partner_MSB_Agreement.html"><span class="doc-code">N1</span>Partner MSB</a>
      <a class="nav-link" href="${prefix}Client_Series/Schedule/N3_Approved_States_Schedule.html"><span class="doc-code">N3</span>States Schedule</a>
      <a class="nav-link" href="${prefix}Client_Series/Schedule/N4_Partner_MSB_Directory.html"><span class="doc-code">N4</span>Partner Directory</a>
      <a class="nav-link" href="${prefix}Client_Series/Schedule/N5_Client_FinCEN_Filing_Guide.html"><span class="doc-code">N5</span>FinCEN Guide</a>
    </div>
  </div>

  <div class="nav-section">
    <div class="nav-section-title">🔒 Internal</div>
    
    <div class="nav-group">
      <div class="nav-group-title">Checklists</div>
      <a class="nav-link" href="${prefix}Internal/Checklist/E1_Filing_Checklist_and_Instructions.html"><span class="doc-code">E1</span>Filing Checklist</a>
      <a class="nav-link" href="${prefix}Internal/Checklist/E2_Securities_and_MTL_Checklist.html"><span class="doc-code">E2</span>Securities/MTL</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Registration</div>
      <a class="nav-link" href="${prefix}Internal/Registration/C1_ABN_Registration_CCASH.html"><span class="doc-code">C1</span>ABN CCASH</a>
      <a class="nav-link" href="${prefix}Internal/Registration/C2_ABN_Template_Client_Series.html"><span class="doc-code">C2</span>ABN Template</a>
      <a class="nav-link" href="${prefix}Internal/Registration/C3_Pricing_and_Routing_Schedule.html"><span class="doc-code">C3</span>Pricing/Routing</a>
    </div>
  </div>
</nav>
NAVEOF
}

# Process each HTML file
find . -name "*.html" ! -name "index.html" | while read file; do
    # Calculate depth (number of directories from root)
    depth=$(echo "$file" | tr -cd '/' | wc -c)
    depth=$((depth - 1))  # Subtract 1 for the leading ./
    
    echo "Processing: $file (depth: $depth)"
    
    # Generate navigation with correct relative paths
    nav_html=$(generate_nav $depth)
    
    # Get the filename for highlighting
    filename=$(basename "$file")
    
    # Create a temp file
    tmpfile=$(mktemp)
    
    # Read the file and inject navigation
    {
        # Read until <body>
        while IFS= read -r line; do
            echo "$line"
            if [[ "$line" == *"<body>"* ]]; then
                break
            fi
        done
        
        # Insert navigation
        echo "$nav_html"
        echo '<div class="main-content">'
        
        # Read rest of file
        while IFS= read -r line; do
            if [[ "$line" == *"</body>"* ]]; then
                echo '</div>'
                echo "$line"
            else
                echo "$line"
            fi
        done
    } < "$file" > "$tmpfile"
    
    # Replace stylesheet reference
    prefix=""
    for ((i=0; i<depth; i++)); do prefix="../$prefix"; done
    sed -i "s|href=\"style.css\"|href=\"${prefix}nav-style.css\"|g" "$tmpfile"
    
    # Highlight current page in nav
    sed -i "s|href=\"[^\"]*${filename}\"|href=\"${prefix}$(echo $file | sed 's|^\./||')\" class=\"nav-link active\"|g" "$tmpfile"
    
    # Move temp file back
    mv "$tmpfile" "$file"
done

echo ""
echo "=== Navigation Injection Complete ==="
echo "Open index.html to browse all documents"
