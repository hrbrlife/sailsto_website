// Scripts for signup.html

// User type selection
        document.querySelectorAll('.user-type-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.user-type-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                document.getElementById('user-type-input').value = btn.dataset.type;
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
            }
        }
        
        // Form submission handling
        document.getElementById('signup-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const form = e.target;
            const submitBtn = form.querySelector('.form-submit');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'Accept': 'application/json' }
                });
                
                if (response.ok) {
                    document.getElementById('signup-form-wrapper').style.display = 'none';
                    document.getElementById('form-success').classList.add('show');
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                alert('There was an error submitting the form. Please try again or contact us directly.');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Application';
            }
        });
        
        // Nav scroll behavior
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });