// Image Lightbox functionality for reads.su
(function() {
    'use strict';

    let lightboxImages = [];
    let currentImageIndex = 0;
    let lightboxActive = false;

    function initLightbox() {
        // Get all images in article: cover image + content images
        const coverImage = document.querySelector('.article-cover-image');
        const contentImages = document.querySelectorAll('.article-content img, .markdown-content img');

        // Combine cover image (if exists) with content images
        let allImages = [];
        if (coverImage) {
            allImages.push(coverImage);
        }
        allImages = allImages.concat(Array.from(contentImages));

        // Only initialize if we're on article page with images
        if (allImages.length === 0) {
            return;
        }

        console.log('Initializing lightbox for', allImages.length, 'images (including cover)');
        lightboxImages = allImages;

        // Add click event to each image and style for zoom
        lightboxImages.forEach((img, index) => {
            img.style.cursor = 'zoom-in';
            img.setAttribute('data-lightbox-index', index);
            img.addEventListener('click', handleImageClick);

            // Add zoom indicator wrapper for content images (not cover)
            if (!img.classList.contains('article-cover-image') &&
                !img.parentElement.classList.contains('image-with-zoom')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'image-with-zoom';
                img.parentNode.insertBefore(wrapper, img);
                wrapper.appendChild(img);
            }
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

        // Check if lightbox exists
        if (!lightbox) {
            console.warn('Lightbox element not found');
            return;
        }

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
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                closeLightbox();
            });
        }

        // Navigation buttons
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                navigateLightbox(-1);
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                navigateLightbox(1);
            });
        }

        // Prevent closing when clicking on image
        if (lightboxImage) {
            lightboxImage.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }

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

        // Check if elements exist
        if (!lightbox || !lightboxImage) {
            console.warn('Lightbox elements not found');
            return;
        }

        currentImageIndex = index;
        const img = lightboxImages[currentImageIndex];

        // Set image source
        lightboxImage.src = img.src;
        lightboxImage.alt = img.alt || '';

        // Update navigation visibility
        if (lightboxImages.length > 1) {
            if (lightboxCounter) {
                lightboxCounter.style.display = 'block';
                lightboxCounter.textContent = `${currentImageIndex + 1} / ${lightboxImages.length}`;
            }
            if (lightboxPrev) {
                lightboxPrev.style.display = currentImageIndex > 0 ? 'flex' : 'none';
            }
            if (lightboxNext) {
                lightboxNext.style.display = currentImageIndex < lightboxImages.length - 1 ? 'flex' : 'none';
            }
        } else {
            if (lightboxCounter) lightboxCounter.style.display = 'none';
            if (lightboxPrev) lightboxPrev.style.display = 'none';
            if (lightboxNext) lightboxNext.style.display = 'none';
        }

        // Show lightbox
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
        lightboxActive = true;
    }

    function closeLightbox() {
        const lightbox = document.getElementById('imageLightbox');
        const lightboxImage = document.getElementById('lightboxImage');

        if (!lightbox) return;

        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        lightboxActive = false;

        // Clear image after animation
        if (lightboxImage) {
            setTimeout(() => {
                lightboxImage.src = '';
                lightboxImage.alt = '';
            }, 300);
        }
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