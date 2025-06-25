document.addEventListener('DOMContentLoaded', function() {
    const mainVideo = document.getElementById('mainVideo');
    const videoTitle = document.getElementById('videoTitle');
    const videoDescription = document.getElementById('videoDescription');
    const videoThumbnails = document.querySelectorAll('.video-thumbnail');

    function switchVideo(videoSrc, title, description) {
        mainVideo.style.opacity = '0';
        
        setTimeout(() => {
            mainVideo.src = videoSrc;
            videoTitle.textContent = title;
            videoDescription.textContent = description;
            mainVideo.style.opacity = '1';
            mainVideo.play().catch(e => {
                console.log('Video autoplay niet toegestaan:', e);
            });
        }, 300);
    }

    videoThumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const videoSrc = this.getAttribute('data-video');
            const title = this.getAttribute('data-title');
            const description = this.getAttribute('data-description');

            videoThumbnails.forEach(thumb => thumb.classList.remove('active'));
            
            this.classList.add('active');

            switchVideo(videoSrc, title, description);
        });
    });

    mainVideo.addEventListener('loadstart', function() {
        console.log('Video laden gestart');
    });

    mainVideo.addEventListener('canplay', function() {
        console.log('Video kan afgespeeld worden');
    });

    mainVideo.addEventListener('error', function(e) {
        console.error('Video fout:', e);
        videoTitle.textContent = 'Video niet beschikbaar';
        videoDescription.textContent = 'Deze video kon niet geladen worden. Controleer of het bestand bestaat.';
    });

    document.addEventListener('keydown', function(e) {
        const activeThumbnail = document.querySelector('.video-thumbnail.active');
        const currentIndex = Array.from(videoThumbnails).indexOf(activeThumbnail);
        
        switch(e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                const nextIndex = (currentIndex + 1) % videoThumbnails.length;
                videoThumbnails[nextIndex].click();
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                const prevIndex = currentIndex === 0 ? videoThumbnails.length - 1 : currentIndex - 1;
                videoThumbnails[prevIndex].click();
                break;
            case ' ':
                e.preventDefault();
                if (mainVideo.paused) {
                    mainVideo.play();
                } else {
                    mainVideo.pause();
                }
                break;
            case 'z':
            case 'Z':
                e.preventDefault();
                if (videoThumbnails[0]) videoThumbnails[0].click();
                break;
            case 'x':
            case 'X':
                e.preventDefault();
                if (videoThumbnails[1]) videoThumbnails[1].click();
                break;
            case 'c':
            case 'C':
                e.preventDefault();
                if (videoThumbnails[2]) videoThumbnails[2].click();
                break;
        }
    });

    mainVideo.addEventListener('dblclick', function() {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            mainVideo.requestFullscreen().catch(e => {
                console.log('Fullscreen niet toegestaan:', e);
            });
        }
    });
    let autoAdvanceInterval;
    
    function startAutoAdvance() {
        autoAdvanceInterval = setInterval(() => {
            const activeThumbnail = document.querySelector('.video-thumbnail.active');
            const currentIndex = Array.from(videoThumbnails).indexOf(activeThumbnail);
            const nextIndex = (currentIndex + 1) % videoThumbnails.length;
            videoThumbnails[nextIndex].click();
        }, 30000); 
    }
    function stopAutoAdvance() {
        if (autoAdvanceInterval) {
            clearInterval(autoAdvanceInterval);
        }
    }
    let userActivityTimeout;
    
    function resetUserActivity() {
        clearTimeout(userActivityTimeout);
        stopAutoAdvance();
        userActivityTimeout = setTimeout(startAutoAdvance, 10000);
    }

    document.addEventListener('mousemove', resetUserActivity);
    document.addEventListener('click', resetUserActivity);
    document.addEventListener('keydown', resetUserActivity);
    setTimeout(startAutoAdvance, 10000);
    function preloadVideos() {
        videoThumbnails.forEach(thumbnail => {
            const videoSrc = thumbnail.getAttribute('data-video');
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'video';
            link.href = videoSrc;
            document.head.appendChild(link);
        });
    }
    preloadVideos();
    videoThumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const videoContainer = document.querySelector('.video-container');
            videoContainer.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
    console.log('Museum Animatie Site geladen en klaar voor gebruik!');

    // Arcade knop polling via HTTP
    function pollButton() {
        fetch('http://localhost:5000/button') 
            .then(response => response.json())
            .then(data => {
                if (data.button === 'video1') {
                    document.querySelectorAll('.video-thumbnail')[0].click();
                } else if (data.button === 'video2') {
                    document.querySelectorAll('.video-thumbnail')[1].click();
                } else if (data.button === 'video3') {
                    document.querySelectorAll('.video-thumbnail')[2].click();
                }
            })
            .catch(err => {
                // Optioneel: foutafhandeling
            })
            .finally(() => {
                setTimeout(pollButton, 200); // elke 200ms opnieuw vragen
            });
    }
    pollButton();
});
