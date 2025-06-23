let isDragging = false;
        let startX;
        let currentPage = null;
        let pages = document.querySelectorAll('.page-wrapper');
        let firstPage = pages[0];
        
        pages.forEach((page, index) => {
            page.style.zIndex = pages.length - index;
            page.addEventListener('mousedown', (e) => {
                isDragging = true;
                startX = e.clientX;
                currentPage = page;
                page.style.cursor = 'grabbing';
            });
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging || !currentPage) return;
            let moveX = e.clientX - startX;
            if (moveX < -50) {
                currentPage.classList.add('flipped');
            } else if (moveX > 50) {
                currentPage.classList.remove('flipped');
            }
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            if (currentPage) currentPage.style.cursor = 'grab';
            currentPage = null;
        });

        window.addEventListener('transitionend', () => {
            if (!firstPage.classList.contains('flipped')) {
                firstPage.querySelector('.front').textContent = 'Album Book';
            } else {
                firstPage.querySelector('.front').textContent = '';
            }
        });