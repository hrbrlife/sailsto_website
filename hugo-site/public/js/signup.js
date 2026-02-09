// Signup form handling with two-step flow and multi-select interest checkboxes

document.addEventListener('DOMContentLoaded', function() {
    
    // Track selected interests
    let selectedInterests = new Set();
    let userEmail = '';
    
    // DOM elements
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const formSuccess = document.getElementById('form-success');
    const skipStep2Link = document.getElementById('skip-step-2');
    
    // Show a specific step
    function showStep(stepId) {
        document.querySelectorAll('.form-step').forEach(step => {
            step.classList.remove('active');
        });
        if (formSuccess) formSuccess.classList.remove('show');
        
        const targetStep = document.getElementById(stepId);
        if (targetStep) {
            targetStep.classList.add('active');
            targetStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    // Update which conditional sections are visible (for step 2)
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
        });
    });
    
    // Handle clicks on the entire interest card - make whole card clickable
    document.querySelectorAll('.interest-checkbox').forEach(label => {
        label.addEventListener('click', (e) => {
            // Always handle the click ourselves to ensure consistent behavior
            e.preventDefault();
            
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
        }
    }
    
    // ========================================
    // SLIDESHOW FUNCTIONALITY
    // ========================================
    
    const slides = document.querySelectorAll('.signup-slide');
    const dots = document.querySelectorAll('.slideshow-dots .dot');
    let currentSlide = 0;
    
    // Map slide types to indices
    const slideTypeMap = {
        'issuer': 0,
        'investor': 1,
        'broker': 2,
        'institution': 3,
        'introducer': 4,
        'trustee': 5
    };
    
    function showSlide(index) {
        // Clamp index
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;
        
        currentSlide = index;
        
        // Update slides
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        
        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    // Initialize slideshow if slides exist
    if (slides.length > 0) {
        // Determine starting slide based on URL param
        let startIndex = 0;
        if (preselectedType && slideTypeMap.hasOwnProperty(preselectedType)) {
            startIndex = slideTypeMap[preselectedType];
        }
        
        // Show initial slide
        showSlide(startIndex);
        
        // Dot click handlers
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
            });
        });
        
        // Interest checkbox hover and click handlers - update slideshow
        document.querySelectorAll('.interest-checkbox').forEach(label => {
            const checkbox = label.querySelector('input[type="checkbox"]');
            if (checkbox) {
                const interestType = checkbox.value;
                const slideIndex = slideTypeMap[interestType];
                
                if (slideIndex !== undefined) {
                    // Hover: show corresponding slide
                    label.addEventListener('mouseenter', () => {
                        showSlide(slideIndex);
                    });
                    
                    // Click/select: show corresponding slide
                    checkbox.addEventListener('change', () => {
                        if (checkbox.checked) {
                            showSlide(slideIndex);
                        }
                    });
                }
            }
        });
    }
    
    // ========================================
    // END SLIDESHOW
    // ========================================
    
    // ========================================
    // STICKY LEFT CONTENT
    // ========================================
    
    const signupContent = document.querySelector('.signup-content');
    const signupContentWrapper = document.querySelector('.signup-content-wrapper');
    const signupContainer = document.querySelector('.signup-container');
    const signupSection = document.querySelector('.signup-section');
    
    if (signupContent && signupContentWrapper && signupContainer && signupSection) {
        const stickyTop = 120;
        let contentOriginalTop = null;
        let contentHeight = null;
        let contentWidth = null;
        let contentLeft = null;
        let containerBottom = null;
        
        function measurePositions() {
            // Temporarily remove sticky to measure natural position
            signupContent.classList.remove('is-sticky');
            signupContent.style.transform = '';
            signupContent.style.width = '';
            signupContent.style.left = '';
            
            // Force reflow
            signupContent.offsetHeight;
            
            const wrapperRect = signupContentWrapper.getBoundingClientRect();
            const contentRect = signupContent.getBoundingClientRect();
            const containerRect = signupContainer.getBoundingClientRect();
            
            contentOriginalTop = contentRect.top + window.scrollY;
            contentHeight = contentRect.height;
            contentWidth = wrapperRect.width; // Use wrapper width for consistency
            contentLeft = wrapperRect.left;
            containerBottom = containerRect.bottom + window.scrollY;
            
            // Set wrapper min-height to prevent collapse
            signupContentWrapper.style.minHeight = contentHeight + 'px';
        }
        
        function handleScroll() {
            const scrollY = window.scrollY;
            const startSticky = contentOriginalTop - stickyTop;
            const endSticky = containerBottom - contentHeight - stickyTop;
            
            if (scrollY > startSticky && scrollY < endSticky) {
                // In sticky zone
                signupContent.classList.add('is-sticky');
                signupContent.style.width = contentWidth + 'px';
                signupContent.style.left = contentLeft + 'px';
                signupContent.style.transform = '';
            } else if (scrollY >= endSticky) {
                // Past sticky zone - pin at bottom
                signupContent.classList.remove('is-sticky');
                signupContent.style.width = '';
                signupContent.style.left = '';
                signupContent.style.transform = `translateY(${endSticky - startSticky}px)`;
            } else {
                // Before sticky zone
                signupContent.classList.remove('is-sticky');
                signupContent.style.width = '';
                signupContent.style.left = '';
                signupContent.style.transform = '';
            }
        }
        
        // Initial measure
        measurePositions();
        handleScroll();
        
        // Update on scroll
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Remeasure on resize
        window.addEventListener('resize', () => {
            measurePositions();
            handleScroll();
        });
    }
    
    // ========================================
    // END STICKY
    // ========================================
    
    // Set source page metadata
    const sourcePageInput = document.getElementById('source-page-input');
    if (sourcePageInput) {
        sourcePageInput.value = document.referrer || window.location.href;
    }
    
    // Marketing checkbox burst effect
    const marketingCheckbox = document.getElementById('marketing');
    const marketingBox = document.getElementById('marketing-box');
    if (marketingCheckbox && marketingBox) {
        marketingCheckbox.addEventListener('change', () => {
            if (marketingCheckbox.checked) {
                marketingBox.classList.add('checked', 'burst');
                // Remove burst class after animation completes
                setTimeout(() => {
                    marketingBox.classList.remove('burst');
                }, 700);
            } else {
                marketingBox.classList.remove('checked');
            }
        });
    }
    
    // STEP 1 FORM SUBMISSION
    const step1Form = document.getElementById('signup-form-step1');
    if (step1Form) {
        step1Form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Validate at least one interest selected
            if (selectedInterests.size === 0) {
                alert('Please select at least one area of interest.');
                return;
            }
            
            const submitBtn = step1Form.querySelector('.form-submit');
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
            
            // Store email for step 2
            userEmail = document.getElementById('email').value;
            
            // Mock submission for testing - always succeed
            await new Promise(resolve => setTimeout(resolve, 500));
            
            // Set hidden fields for step 2
            const step2Email = document.getElementById('step2-email');
            const step2Interests = document.getElementById('step2-interests');
            if (step2Email) step2Email.value = userEmail;
            if (step2Interests) step2Interests.value = Array.from(selectedInterests).join(',');
            
            // Go directly to step 2 with form fields
            showStep('step-2');
            updateVisibleSections();
        });
    }
    
    // SKIP STEP 2
    if (skipStep2Link) {
        skipStep2Link.addEventListener('click', (e) => {
            e.preventDefault();
            if (formSuccess) {
                document.querySelectorAll('.form-step').forEach(step => {
                    step.classList.remove('active');
                });
                formSuccess.classList.add('show');
                document.getElementById('success-message').textContent = 
                    "You're on the list! We'll be in touch within 24 hours.";
                formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }
    
    // STEP 2 FORM SUBMISSION
    const step2Form = document.getElementById('signup-form-step2');
    if (step2Form) {
        step2Form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = step2Form.querySelector('.form-submit');
            const submitText = submitBtn.querySelector('.submit-text');
            const submitLoading = submitBtn.querySelector('.submit-loading');
            
            submitBtn.disabled = true;
            if (submitText) submitText.style.display = 'none';
            if (submitLoading) submitLoading.style.display = 'inline';
            
            // Mock submission for testing - always succeed
            await new Promise(resolve => setTimeout(resolve, 500));
            document.querySelectorAll('.form-step').forEach(step => {
                step.classList.remove('active');
            });
            if (formSuccess) {
                formSuccess.classList.add('show');
                formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }
    
    // Conditional field handlers (for step 2)
    
    // Investor type change listener for accreditation field
    const investorTypeSelect = document.getElementById('investor-type');
    if (investorTypeSelect) {
        investorTypeSelect.addEventListener('change', () => {
            const accreditationGroup = document.getElementById('accreditation-method-group');
            if (accreditationGroup) {
                const isIndividual = investorTypeSelect.value?.includes('individual');
                if (isIndividual && investorTypeSelect.value === 'individual-accredited') {
                    accreditationGroup.style.display = 'block';
                } else {
                    accreditationGroup.style.display = 'none';
                }
            }
        });
    }
    
    // Industry "Other" field visibility
    const industrySectorSelect = document.getElementById('industry');
    const industryOtherGroup = document.getElementById('industry-other-group');
    if (industrySectorSelect && industryOtherGroup) {
        industrySectorSelect.addEventListener('change', () => {
            if (industrySectorSelect.value === 'other') {
                industryOtherGroup.style.display = 'block';
            } else {
                industryOtherGroup.style.display = 'none';
            }
        });
    }
    
    // Institution type "Other" field visibility
    const institutionTypeSelect = document.getElementById('institution-type');
    const institutionTypeOtherGroup = document.getElementById('institution-type-other-group');
    if (institutionTypeSelect && institutionTypeOtherGroup) {
        institutionTypeSelect.addEventListener('change', () => {
            if (institutionTypeSelect.value === 'other') {
                institutionTypeOtherGroup.style.display = 'block';
            } else {
                institutionTypeOtherGroup.style.display = 'none';
            }
        });
    }
});
