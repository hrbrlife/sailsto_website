// Signup form handling with multi-select interest checkboxes

document.addEventListener('DOMContentLoaded', function() {
    
    // Success messages based on selected interests
    const successMessages = {
        issuer: "issuer capital raise",
        investor: "investment opportunities",
        broker: "brokerage partnership",
        institution: "institutional solutions",
        introducer: "introducer referral program"
    };
    
    // Track selected interests
    let selectedInterests = new Set();
    
    // Update which conditional sections are visible
    function updateVisibleSections() {
        document.querySelectorAll('.conditional-fields').forEach(section => {
            const showFor = section.dataset.showFor;
            if (selectedInterests.has(showFor)) {
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        });
    }
    
    // Update checkbox visual state
    function updateCheckboxVisual(checkbox, isChecked) {
        const label = checkbox.closest('.interest-checkbox');
        if (label) {
            if (isChecked) {
                label.classList.add('selected');
            } else {
                label.classList.remove('selected');
            }
        }
    }
    
    // Handle interest checkbox changes
    const interestCheckboxes = document.querySelectorAll('.interest-checkbox input[type="checkbox"]');
    
    interestCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const interest = e.target.value;
            if (e.target.checked) {
                selectedInterests.add(interest);
            } else {
                selectedInterests.delete(interest);
            }
            updateCheckboxVisual(e.target, e.target.checked);
            updateVisibleSections();
        });
    });
    
    // Also handle clicks on the label container
    document.querySelectorAll('.interest-checkbox').forEach(label => {
        label.addEventListener('click', (e) => {
            // Don't double-trigger if clicking directly on checkbox
            if (e.target.type === 'checkbox') return;
            
            const checkbox = label.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change'));
            }
        });
    });
    
    // Check URL params for pre-selection
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedType = urlParams.get('type');
    
    if (preselectedType) {
        const checkbox = document.querySelector(`.interest-checkbox input[value="${preselectedType}"]`);
        if (checkbox) {
            checkbox.checked = true;
            selectedInterests.add(preselectedType);
            updateCheckboxVisual(checkbox, true);
            updateVisibleSections();
        }
    }
    
    // Set source page metadata
    const sourcePageInput = document.getElementById('source-page-input');
    if (sourcePageInput) {
        sourcePageInput.value = document.referrer || window.location.href;
    }
    
    // Investor type change listener for accreditation field
    const investorTypeSelect = document.getElementById('investor-type');
    if (investorTypeSelect) {
        investorTypeSelect.addEventListener('change', () => {
            const accreditationGroup = document.getElementById('accreditation-method-group');
            if (accreditationGroup) {
                const isIndividual = investorTypeSelect.value?.includes('individual');
                // For US individuals only - simplified for now
                if (isIndividual && investorTypeSelect.value === 'individual-accredited') {
                    accreditationGroup.style.display = 'block';
                } else {
                    accreditationGroup.style.display = 'none';
                }
            }
        });
    }
    
    // Form submission handling
    const form = document.getElementById('signup-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Validate at least one interest selected
            if (selectedInterests.size === 0) {
                alert('Please select at least one area of interest.');
                return;
            }
            
            const submitBtn = form.querySelector('.form-submit');
            const submitText = submitBtn.querySelector('.submit-text');
            const submitLoading = submitBtn.querySelector('.submit-loading');
            
            submitBtn.disabled = true;
            if (submitText) submitText.style.display = 'none';
            if (submitLoading) submitLoading.style.display = 'inline';
            
            // Set submission timestamp
            const timestampInput = document.getElementById('submitted-at-input');
            if (timestampInput) {
                timestampInput.value = new Date().toISOString();
            }
            
            // Build success message from selected interests
            const interestsList = Array.from(selectedInterests).map(i => successMessages[i] || i);
            let successText = "Your inquiry has been received. We'll be in touch within 24 hours regarding ";
            if (interestsList.length === 1) {
                successText += interestsList[0] + ".";
            } else if (interestsList.length === 2) {
                successText += interestsList.join(' and ') + ".";
            } else {
                successText += interestsList.slice(0, -1).join(', ') + ', and ' + interestsList.slice(-1) + ".";
            }
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'Accept': 'application/json' }
                });
                
                if (response.ok) {
                    // Update success message
                    const successMsgEl = document.getElementById('success-message');
                    if (successMsgEl) {
                        successMsgEl.textContent = successText;
                    }
                    
                    document.getElementById('signup-form-wrapper').style.display = 'none';
                    document.getElementById('form-success').classList.add('show');
                    
                    // Scroll success message into view
                    document.getElementById('form-success').scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                alert('There was an error submitting the form. Please try again or contact us directly at hello@sails.to');
                submitBtn.disabled = false;
                if (submitText) submitText.style.display = 'inline';
                if (submitLoading) submitLoading.style.display = 'none';
            }
        });
    }
    
    // Nav scroll behavior
    window.addEventListener('scroll', () => {
        const nav = document.querySelector('nav');
        if (nav && window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else if (nav) {
            nav.classList.remove('scrolled');
        }
    });
});