// Scripts for company/contact.html

// Form submission handling
        document.getElementById('contact-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const form = e.target;
            const submitBtn = form.querySelector('.form-submit');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'Accept': 'application/json' }
                });
                
                if (response.ok) {
                    document.getElementById('contact-form-wrapper').style.display = 'none';
                    document.getElementById('form-success').style.display = 'block';
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                alert('There was an error sending your message. Please try emailing us directly at hello@sails.to');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Send Message';
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