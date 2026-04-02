  // Matrix Rain Effect
    const canvas = document.getElementById('matrix-bg');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
    const matrixArray = matrix.split("");
    
    const fontSize = 10;
    const columns = canvas.width / fontSize;
    
    const drops = [];
    for(let x = 0; x < columns; x++) {
        drops[x] = 1;
    }
    
    function drawMatrix() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        
        for(let i = 0; i < drops.length; i++) {
            const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(drawMatrix, 35);
    
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    // Pricing Toggle
    let currentPeriod = 'yearly';
    
    function updatePrices(period) {
        const yearlyPrices = document.querySelectorAll('.yearly-price');
        const monthlyPrices = document.querySelectorAll('.monthly-price');
        const lifetimePrices = document.querySelectorAll('.lifetime-price');
        
        if(period === 'yearly') {
            yearlyPrices.forEach(price => price.style.display = 'block');
            monthlyPrices.forEach(price => price.style.display = 'none');
            lifetimePrices.forEach(price => price.style.display = 'none');
        } else if(period === 'monthly') {
            yearlyPrices.forEach(price => price.style.display = 'none');
            monthlyPrices.forEach(price => price.style.display = 'block');
            lifetimePrices.forEach(price => price.style.display = 'none');
        } else {
            yearlyPrices.forEach(price => price.style.display = 'none');
            monthlyPrices.forEach(price => price.style.display = 'none');
            lifetimePrices.forEach(price => price.style.display = 'block');
        }
    }
    
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentPeriod = btn.dataset.period;
            updatePrices(currentPeriod);
        });
    });

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            item.classList.toggle('active');
            const icon = question.querySelector('i:last-child');
            if(item.classList.contains('active')) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            } else {
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        });
    });

    // Payment Modal Function
    function showPayment(plan, price) {
        const periodText = currentPeriod === 'yearly' ? 'year' : (currentPeriod === 'monthly' ? 'month' : 'lifetime');
        const actualPrice = currentPeriod === 'yearly' ? price : (currentPeriod === 'monthly' ? Math.round(price / 12) : (plan === 'Basic' ? 0 : (plan === 'Enhanced' ? 149 : (plan === 'Advanced' ? 299 : (plan === 'Extreme' ? 599 : (plan === 'Military' ? 899 : 1499))))));
        
        alert(`💳 Payment Process\n\nPlan: ${plan} (${currentPeriod.toUpperCase()})\nPrice: $${actualPrice}/${periodText}\n\nIn a real implementation, this would redirect to a secure payment gateway.\n\nPayment methods accepted: Credit Card, PayPal, Crypto`);
        
        // In production, this would redirect to payment gateway
        // window.location.href = `/checkout?plan=${plan.toLowerCase()}&period=${currentPeriod}`;
    }

    // Animate on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.pricing-card, .discount-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });

    // Console warning
    console.log("%c⚠️ PHANTOM FUD BUILDER v9.0 PRICING ⚠️", "color: #00ff00; font-size: 16px; font-weight: bold;");
    console.log("%cChoose the protection level that fits your needs", "color: #00ffff; font-size: 12px;");
    console.log("%c30-Day Money-Back Guarantee on all paid plans", "color: #00ff00; font-size: 12px;");