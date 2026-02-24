// Scripts for introducers.html

const nav = document.querySelector('nav');
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 60) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });

        // Introduction Reward Calculator
        function formatCurrency(amount) {
            return '$' + amount.toLocaleString('en-US', { maximumFractionDigits: 0 });
        }

        function parseAmount(str) {
            return parseFloat(str.replace(/[^0-9.-]/g, '')) || 0;
        }

        function updateSliderBackground() {
            const slider = document.getElementById('raiseSlider');
            const min = parseFloat(slider.min);
            const max = parseFloat(slider.max);
            const val = parseFloat(slider.value);
            const pct = ((val - min) / (max - min)) * 100;
            slider.style.setProperty('--slider-pct', pct + '%');
        }

        function calculateIntroReward() {
            const raise = parseAmount(document.getElementById('raiseAmount').value);
            
            // Average Sails.to commission ~3.5% (mix of 1% referral and 6% general)
            const avgPlatformRate = 0.035;
            const platformCommission = raise * avgPlatformRate;
            const yourReward = platformCommission * 0.25;

            document.getElementById('introResult').innerHTML = `
                <div class="label">Your Introduction Reward</div>
                <div class="amount">${formatCurrency(yourReward)}</div>
                <div class="breakdown">
                    <span>Raise: ${formatCurrency(raise)}</span>
                    <span>Platform commission (~3.5%): ${formatCurrency(platformCommission)}</span>
                    <span>Your 25% share: <strong>${formatCurrency(yourReward)}</strong></span>
                </div>
            `;
        }

        // Slider controls the input
        document.getElementById('raiseSlider').addEventListener('input', function() {
            const val = parseFloat(this.value);
            document.getElementById('raiseAmount').value = val.toLocaleString('en-US');
            updateSliderBackground();
            calculateIntroReward();
        });

        // Initial calculation and slider position
        updateSliderBackground();
        calculateIntroReward();