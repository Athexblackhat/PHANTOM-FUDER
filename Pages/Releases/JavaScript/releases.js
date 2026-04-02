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

    // Animate numbers
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const originalText = stat.innerText;
        const number = parseFloat(originalText.replace(/[^0-9.-]/g, ''));
        if(!isNaN(number)) {
            let current = 0;
            const increment = number / 50;
            const timer = setInterval(() => {
                current += increment;
                if(current >= number) {
                    stat.innerText = originalText;
                    clearInterval(timer);
                } else {
                    stat.innerText = Math.floor(current) + (originalText.includes('+') ? '+' : '');
                }
            }, 20);
        }
    });

    // Console warning
    console.log("%c⚠️ PHANTOM FUD BUILDER v9.0 VERSION HISTORY ⚠️", "color: #00ff00; font-size: 16px; font-weight: bold;");
    console.log("%cFrom v5.0 to v9.0 - The evolution of ultimate Android protection", "color: #00ffff; font-size: 12px;");
    console.log("%cCurrent stable: v9.0 Phantom Edition | 0.1% Detection Rate", "color: #00ff00; font-size: 12px;");