// Signup form handling with conditional fields per user type

document.addEventListener('DOMContentLoaded', function() {
    
    // Form title/subtitle text per user type
    const formTitles = {
        issuer: {
            title: "Start Your Capital Raise",
            subtitle: "Tell us about your project and we'll guide you through the process"
        },
        investor: {
            title: "Access Investment Opportunities",
            subtitle: "Join our network of professional investors in compliant tokenized securities"
        },
        broker: {
            title: "Partner With Us",
            subtitle: "Expand your offerings with compliant CrossSecurities for your clients"
        },
        institution: {
            title: "Institutional Solutions",
            subtitle: "White-label tokenization, custody, and distribution infrastructure"
        },
        introducer: {
            title: "Become an Introducer",
            subtitle: "Earn referral fees by connecting issuers with our platform"
        },
        default: {
            title: "Join the Waitlist",
            subtitle: "Tell us about yourself and we'll be in touch within 24 hours"
        }
    };
    
    // Success messages per user type
    const successMessages = {
        issuer: "Your capital raise inquiry has been received. A member of our issuer relations team will contact you within 24 hours to discuss your project and next steps.",
        investor: "Your investor application has been received. We'll be in touch within 24 hours with information about current and upcoming offerings that match your criteria.",
        broker: "Your partnership inquiry has been received. Our broker relations team will contact you within 24 hours to discuss integration and onboarding.",
        institution: "Your institutional inquiry has been received. A senior member of our team will contact you within 24 hours to discuss enterprise solutions.",
        introducer: "Your introducer application has been received. We'll be in touch within 24 hours with details about our referral program and commission structure.",
        default: "Your application has been received. A member of our team will be in touch within 24 hours."
    };
    
    // Update form UI based on selected user type
    function updateFormUI(type) {
        // Update title and subtitle
        const titleEl = document.getElementById('form-title');
        const subtitleEl = document.getElementById('form-subtitle');
        const config = formTitles[type] || formTitles.default;
        
        if (titleEl) titleEl.textContent = config.title;
        if (subtitleEl) subtitleEl.textContent = config.subtitle;
        
        // Show/hide conditional fields
        document.querySelectorAll('.conditional-fields').forEach(section => {
            const showFor = section.dataset.showFor;
            if (showFor === type) {
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        });
    }
    
    // Handle country change for investor accreditation field
    function handleCountryChange() {
        const countrySelect = document.getElementById('country');
        const accreditationGroup = document.getElementById('accreditation-method-group');
        const investorTypeSelect = document.getElementById('investor-type');
        
        if (countrySelect && accreditationGroup) {
            const isUS = countrySelect.value === 'US';
            const isInvestor = document.getElementById('user-type-input')?.value === 'investor';
            const isIndividual = investorTypeSelect?.value?.includes('individual');
            
            // Show accreditation method only for US individual investors
            if (isUS && isInvestor && isIndividual) {
                accreditationGroup.style.display = 'block';
            } else {
                accreditationGroup.style.display = 'none';
            }
        }
    }
    
    // User type selection
    document.querySelectorAll('.user-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.user-type-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            const type = btn.dataset.type;
            document.getElementById('user-type-input').value = type;
            updateFormUI(type);
            handleCountryChange(); // Re-evaluate accreditation visibility
        });
    });
    
    // Check URL params for pre-selection
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedType = urlParams.get('type');
    if (preselectedType) {
        const btn = document.querySelector(`.user-type-btn[data-type="${preselectedType}"]`);
        if (btn) {
            btn.classList.add('selected');
            document.getElementById('user-type-input').value = preselectedType;
            updateFormUI(preselectedType);
        }
    }
    
    // Set source page metadata
    const sourcePageInput = document.getElementById('source-page-input');
    if (sourcePageInput) {
        sourcePageInput.value = document.referrer || window.location.href;
    }
    
    // Country change listener
    const countrySelect = document.getElementById('country');
    if (countrySelect) {
        countrySelect.addEventListener('change', handleCountryChange);
    }
    
    // Investor type change listener
    const investorTypeSelect = document.getElementById('investor-type');
    if (investorTypeSelect) {
        investorTypeSelect.addEventListener('change', handleCountryChange);
    }
    
    // Form submission handling
    const form = document.getElementById('signup-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
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
            
            // Get selected type for success message
            const selectedType = document.getElementById('user-type-input').value;
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'Accept': 'application/json' }
                });
                
                if (response.ok) {
                    // Update success message based on type
                    const successMsgEl = document.getElementById('success-message');
                    if (successMsgEl) {
                        successMsgEl.textContent = successMessages[selectedType] || successMessages.default;
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
    
    // Initial call to handle any pre-selected values
    handleCountryChange();
});