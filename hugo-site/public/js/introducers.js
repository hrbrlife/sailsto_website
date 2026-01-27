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

        // Format input on blur
        document.getElementById('raiseAmount').addEventListener('blur', function() {
            const val = parseAmount(this.value);
            this.value = val.toLocaleString('en-US');
            calculateIntroReward();
        });

        document.getElementById('raiseAmount').addEventListener('input', calculateIntroReward);

        // Initial calculation
        calculateIntroReward();