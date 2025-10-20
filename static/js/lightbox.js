// Image Lightbox functionality for reads.su
(function() {
    'use strict';

    let lightboxImages = [];
    let currentImageIndex = 0;
    let lightboxActive = false;

    function initLightbox() {
        // Get all images ONLY in article content (not on home page)
        const articleImages = document.querySelectorAll('.article-content img, .markdown-content img');

        // Only initialize if we're on article page with images
        if (articleImages.length === 0) {
            return;
        }

        console.log('Initializing lightbox for', articleImages.length, 'images');
        lightboxImages = Array.from(articleImages);

        // Add click event to each image
        lightboxImages.forEach((img, index) => {
            img.style.cursor = 'pointer';
            img.setAttribute('data-lightbox-index', index);
            img.addEventListener('click', handleImageClick);
        });

        // Setup lightbox event listeners
        setupLightboxEvents();
    }

    function handleImageClick(e) {
        e.preventDefault();
        e.stopPropagation();
        const index = parseInt(this.getAttribute('data-lightbox-index'));
        openLightbox(index);
    }

    function setupLightboxEvents() {
        const lightbox = document.getElementById('imageLightbox');
        const closeBtn = lightbox.querySelector('.lightbox-close');
        const prevBtn = document.getElementById('lightboxPrev');
        const nextBtn = document.getElementById('lightboxNext');
        const lightboxImage = document.getElementById('lightboxImage');

        // Click on background to close
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });

        // Close button
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeLightbox();
        });

        // Navigation buttons
        prevBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            navigateLightbox(-1);
        });

        nextBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            navigateLightbox(1);
        });

        // Prevent closing when clicking on image
        lightboxImage.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // Keyboard navigation
        document.addEventListener('keydown', handleKeyPress);
    }

    function handleKeyPress(e) {
        if (!lightboxActive) return;

        switch(e.key) {
            case 'Escape':
                closeLightbox();
                break;
            case 'ArrowLeft':
                navigateLightbox(-1);
                break;
            case 'ArrowRight':
                navigateLightbox(1);
                break;
        }
    }

    function openLightbox(index) {
        const lightbox = document.getElementById('imageLightbox');
        const lightboxImage = document.getElementById('lightboxImage');
        const lightboxCounter = document.getElementById('lightboxCounter');
        const lightboxPrev = document.getElementById('lightboxPrev');
        const lightboxNext = document.getElementById('lightboxNext');

        currentImageIndex = index;
        const img = lightboxImages[currentImageIndex];

        // Set image source
        lightboxImage.src = img.src;
        lightboxImage.alt = img.alt || '';

        // Update navigation visibility
        if (lightboxImages.length > 1) {
            lightboxCounter.style.display = 'block';
            lightboxCounter.textContent = `${currentImageIndex + 1} / ${lightboxImages.length}`;
            lightboxPrev.style.display = currentImageIndex > 0 ? 'flex' : 'none';
            lightboxNext.style.display = currentImageIndex < lightboxImages.length - 1 ? 'flex' : 'none';
        } else {
            lightboxCounter.style.display = 'none';
            lightboxPrev.style.display = 'none';
            lightboxNext.style.display = 'none';
        }

        // Show lightbox
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
        lightboxActive = true;
    }

    function closeLightbox() {
        const lightbox = document.getElementById('imageLightbox');
        const lightboxImage = document.getElementById('lightboxImage');

        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        lightboxActive = false;

        // Clear image after animation
        setTimeout(() => {
            lightboxImage.src = '';
            lightboxImage.alt = '';
        }, 300);
    }

    function navigateLightbox(direction) {
        const newIndex = currentImageIndex + direction;

        if (newIndex >= 0 && newIndex < lightboxImages.length) {
            openLightbox(newIndex);
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLightbox);
    } else {
        initLightbox();
    }

    // Re-initialize after AJAX content loads (if any)
    window.reinitLightbox = initLightbox;
})();