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

    // Installation tabs
    const tabs = document.querySelectorAll('.install-tab');
    const contents = {
        windows: document.getElementById('windows-install'),
        linux: document.getElementById('linux-install'),
        mac: document.getElementById('mac-install'),
        source: document.getElementById('source-install')
    };

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const os = tab.dataset.os;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active content
            Object.values(contents).forEach(content => {
                content.classList.remove('active');
            });
            contents[os].classList.add('active');
        });
    });

    // FAQ accordion
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

    // Download buttons with animation
    const downloadBtns = document.querySelectorAll('.download-btn');
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Add loading animation
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> PREPARING DOWNLOAD...';
            btn.style.opacity = '0.7';
            
            // Simulate download preparation
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.opacity = '1';
                
                // Show success message
                alert('Download started! If download doesn\'t begin automatically, please check your browser settings.\n\nNote: For actual implementation, this would link to the real download file.');
                
                // In production, this would trigger actual download
                // window.location.href = '/downloads/phantom-fud-windows.exe';
            }, 1500);
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if(href !== '#' && href !== '') {
                const target = document.querySelector(href);
                if(target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Console warning
    console.log("%c⚠️ PHANTOM FUD BUILDER v9.0 ⚠️", "color: #00ff00; font-size: 16px; font-weight: bold;");
    console.log("%cFOR AUTHORIZED SECURITY RESEARCH ONLY", "color: #ff0000; font-size: 14px;");
    console.log("%cUnauthorized use is illegal and punishable by law.", "color: #ff6600; font-size: 12px;");
    console.log("%cDownload verification: Use provided SHA-256 hashes to verify integrity.", "color: #00ff00; font-size: 12px;");

    // Check if running on local file
    if(window.location.protocol === 'file:') {
        console.warn('Running from local file. Some features may not work properly.');
    }