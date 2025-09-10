// Professional Enterprise Website with Whimsical UX Elements
// DigiConsult - Enhanced User Experience

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initNavigation();
    initHeroAnimations();
    initServiceCards();
    initContactForm();
    initScrollAnimations();
    initWhimsicalElements();
    initLoadingStates();
    
    // Professional navigation with smooth interactions
    function initNavigation() {
        const navbar = document.querySelector('.navbar');
        const navLinks = document.querySelectorAll('.nav-link');
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        // Navbar scroll effect with smooth transition
        let isScrolling = false;
        window.addEventListener('scroll', () => {
            if (!isScrolling) {
                window.requestAnimationFrame(() => {
                    if (window.scrollY > 50) {
                        navbar.classList.add('scrolled');
                    } else {
                        navbar.classList.remove('scrolled');
                    }
                    isScrolling = false;
                });
                isScrolling = true;
            }
        });
        
        // Smooth scroll with whimsical easing
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    // Add whimsical "preparing to scroll" animation
                    this.style.transform = 'scale(0.95)';
                    this.style.transition = 'transform 0.1s ease';
                    
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                        
                        const offsetTop = targetSection.offsetTop - 70;
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                        
                        // Close mobile menu with animation
                        if (navMenu.classList.contains('active')) {
                            navMenu.style.opacity = '0';
                            setTimeout(() => {
                                navMenu.classList.remove('active');
                                navMenu.style.opacity = '1';
                            }, 200);
                        }
                    }, 100);
                }
            });
        });
        
        // Mobile toggle with satisfying animation
        if (navToggle) {
            navToggle.addEventListener('click', function() {
                this.style.transform = 'scale(0.9) rotate(180deg)';
                this.style.transition = 'transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                
                setTimeout(() => {
                    navMenu.classList.toggle('active');
                    this.style.transform = 'scale(1) rotate(0deg)';
                }, 150);
            });
        }
    }
    
    // Hero section with delightful animations
    function initHeroAnimations() {
        const heroTitle = document.querySelector('.hero-content h1');
        const tagline = document.querySelector('.tagline');
        const heroButtons = document.querySelectorAll('.hero-actions .btn');
        const serviceNodes = document.querySelectorAll('.service-node');
        
        // Staggered entrance animations
        if (heroTitle) {
            setTimeout(() => {
                heroTitle.style.opacity = '1';
                heroTitle.style.transform = 'translateY(0)';
            }, 300);
        }
        
        if (tagline) {
            setTimeout(() => {
                tagline.style.opacity = '1';
                tagline.style.transform = 'translateY(0)';
            }, 100);
        }
        
        // Animated service nodes with pulse effect
        serviceNodes.forEach((node, index) => {
            setTimeout(() => {
                node.style.opacity = '1';
                node.style.transform = 'scale(1)';
                
                // Add continuous subtle pulse
                setInterval(() => {
                    if (!node.matches(':hover')) {
                        node.style.transform = 'scale(1.02)';
                        setTimeout(() => {
                            node.style.transform = 'scale(1)';
                        }, 300);
                    }
                }, 3000 + (index * 500));
            }, 600 + (index * 200));
        });
        
        // Hero buttons with delightful hover effects
        heroButtons.forEach((btn, index) => {
            setTimeout(() => {
                btn.style.opacity = '1';
                btn.style.transform = 'translateY(0)';
            }, 800 + (index * 100));
            
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.02)';
                this.style.transition = 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
            
            // Click animation with satisfying feedback
            btn.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.classList.add('btn-ripple');
                this.appendChild(ripple);
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // Service cards with whimsical interactions
    function initServiceCards() {
        const serviceCards = document.querySelectorAll('.service-card, .tool-card, .module-card');
        
        serviceCards.forEach(card => {
            // Mouse enter with spring animation
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
                this.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
                
                // Icon bounce effect
                const icon = this.querySelector('.service-icon i, .tool-header i');
                if (icon) {
                    icon.style.transform = 'scale(1.2) rotate(5deg)';
                    icon.style.transition = 'transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                }
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                
                const icon = this.querySelector('.service-icon i, .tool-header i');
                if (icon) {
                    icon.style.transform = 'scale(1) rotate(0deg)';
                }
            });
            
            // Click feedback with celebration
            card.addEventListener('click', function(e) {
                if (!e.target.closest('a')) {
                    createConfetti(this);
                }
            });
        });
        
        // Feature tags with delightful hover
        const featureTags = document.querySelectorAll('.feature-tag, .feature, .feature-badge');
        featureTags.forEach(tag => {
            tag.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.1) rotate(2deg)';
                this.style.transition = 'transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            });
            
            tag.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) rotate(0deg)';
            });
        });
    }
    
    // Enhanced contact form with progressive feedback
    function initContactForm() {
        const contactForm = document.getElementById('contactForm');
        const formInputs = contactForm.querySelectorAll('input, select, textarea');
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        
        // Progressive form validation with encouraging feedback
        formInputs.forEach(input => {
            let hasBeenFocused = false;
            
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
                
                if (!hasBeenFocused) {
                    this.style.transform = 'scale(1.02)';
                    this.style.transition = 'transform 0.2s ease';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 200);
                    hasBeenFocused = true;
                }
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                if (this.value) {
                    this.parentElement.classList.add('completed');
                    showFieldSuccess(this);
                } else {
                    this.parentElement.classList.remove('completed');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.style.borderColor = '#16A085';
                } else {
                    this.style.borderColor = '';
                }
            });
        });
        
        // Form submission with delightful loading states
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate form with encouraging messages
            const formData = new FormData(contactForm);
            const name = formData.get('name');
            const email = formData.get('email');
            const service = formData.get('service');
            const message = formData.get('message');
            
            if (!name || !email || !service || !message) {
                showNotification('Please fill in all fields to help us assist you better! 😊', 'warning');
                return;
            }
            
            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address so we can reach you! 📧', 'warning');
                return;
            }
            
            // Create mailto link with form data
            const subject = `${service} - Consultation Request from ${name}`;
            const body = `Name: ${name}\nEmail: ${email}\nService Interest: ${service}\n\nMessage:\n${message}`;
            const mailtoLink = `mailto:ck@digiconsult.ca?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            
            // Delightful submission animation
            submitBtn.innerHTML = '<i class="fas fa-rocket"></i> Launching...';
            submitBtn.style.transform = 'scale(0.95)';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Opening Email...';
                submitBtn.style.background = '#16A085';
                
                setTimeout(() => {
                    window.location.href = mailtoLink;
                    
                    setTimeout(() => {
                        showNotification('Your email client should now be open! We look forward to hearing from you! 🚀', 'success');
                        contactForm.reset();
                        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Request Consultation';
                        submitBtn.style.background = '';
                        submitBtn.style.transform = 'scale(1)';
                        submitBtn.disabled = false;
                        
                        // Celebration animation
                        createConfetti(submitBtn);
                    }, 1000);
                }, 1000);
            }, 500);
        });
    }
    
    // Scroll animations with intersection observer
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Special animation for stat numbers
                    if (entry.target.classList.contains('stat-number') || 
                        entry.target.classList.contains('achievement-number')) {
                        animateCounter(entry.target);
                    }
                }
            });
        }, observerOptions);
        
        // Observe all animatable elements
        const animateElements = document.querySelectorAll(
            '.service-card, .tool-card, .module-card, .step, .trend-item, .stat-number, .achievement-number'
        );
        
        animateElements.forEach(el => {
            observer.observe(el);
        });
    }
    
    // Whimsical UI elements and micro-interactions
    function initWhimsicalElements() {
        // Custom cursor effects for interactive elements
        const interactiveElements = document.querySelectorAll('a, button, .service-card, .tool-card');
        
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                document.body.style.cursor = 'pointer';
            });
            
            element.addEventListener('mouseleave', function() {
                document.body.style.cursor = 'default';
            });
        });
        
        // Status badges with breathing animation
        const statusBadges = document.querySelectorAll('.status-badge.online');
        statusBadges.forEach(badge => {
            setInterval(() => {
                badge.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    badge.style.transform = 'scale(1)';
                }, 500);
            }, 2000);
        });
        
        // Tool links with satisfying hover
        const toolLinks = document.querySelectorAll('.tool-link');
        toolLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px)';
                this.style.transition = 'transform 0.2s ease';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
        });
        
        // Easter egg: Konami code for special animation
        let konamiCode = [];
        const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
        
        document.addEventListener('keydown', function(e) {
            konamiCode.push(e.keyCode);
            if (konamiCode.length > 10) {
                konamiCode.shift();
            }
            
            if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
                activateSecretMode();
                konamiCode = [];
            }
        });
    }
    
    // Loading states and progress indicators
    function initLoadingStates() {
        // Simulate loading for external tool links
        const externalLinks = document.querySelectorAll('a[target="_blank"]');
        
        externalLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (this.href.includes('digiconsult.ca')) {
                    const loadingOverlay = createLoadingOverlay('Connecting to AI Infrastructure...');
                    document.body.appendChild(loadingOverlay);
                    
                    setTimeout(() => {
                        loadingOverlay.remove();
                    }, 2000);
                }
            });
        });
    }
    
    // Utility functions for whimsical effects
    function showFieldSuccess(field) {
        const checkmark = document.createElement('div');
        checkmark.innerHTML = '✓';
        checkmark.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%) scale(0);
            color: #16A085;
            font-weight: bold;
            transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        `;
        
        field.parentElement.style.position = 'relative';
        field.parentElement.appendChild(checkmark);
        
        setTimeout(() => {
            checkmark.style.transform = 'translateY(-50%) scale(1)';
        }, 100);
        
        setTimeout(() => {
            checkmark.remove();
        }, 2000);
    }
    
    function createConfetti(element) {
        const colors = ['#E53E3E', '#16A085', '#3498DB', '#F39C12', '#9B59B6'];
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < 12; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top + rect.height / 2}px;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                animation: confetti-fall 1s ease-out forwards;
            `;
            
            const angle = (Math.PI * 2 * i) / 12;
            const velocity = 50 + Math.random() * 50;
            confetti.style.setProperty('--dx', Math.cos(angle) * velocity + 'px');
            confetti.style.setProperty('--dy', Math.sin(angle) * velocity + 'px');
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 1000);
        }
    }
    
    function createLoadingOverlay(message) {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            color: white;
            font-family: Inter, sans-serif;
        `;
        
        overlay.innerHTML = `
            <div style="width: 50px; height: 50px; border: 3px solid #333; border-top: 3px solid #E53E3E; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem;"></div>
            <p style="font-size: 1.1rem; font-weight: 500;">${message}</p>
        `;
        
        return overlay;
    }
    
    function animateCounter(element) {
        const target = parseInt(element.textContent.replace(/[^0-9]/g, ''));
        const duration = 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = element.textContent.replace(/\\d+/, target);
                clearInterval(timer);
            } else {
                element.textContent = element.textContent.replace(/\\d+/, Math.floor(current));
            }
        }, 16);
    }
    
    function isValidEmail(email) {
        return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            warning: 'fa-exclamation-triangle',
            error: 'fa-times-circle',
            info: 'fa-info-circle'
        };
        
        const colors = {
            success: { bg: '#D4EDDA', color: '#155724', border: '#C3E6CB' },
            warning: { bg: '#FFF3CD', color: '#856404', border: '#FFEAA7' },
            error: { bg: '#F8D7DA', color: '#721C24', border: '#F5C6CB' },
            info: { bg: '#CCE5FF', color: '#004085', border: '#B3D4FC' }
        };
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <i class="fas ${icons[type]}"></i>
                <span>${message}</span>
            </div>
            <button onclick="this.parentElement.remove()" style="position: absolute; top: 0.5rem; right: 0.5rem; background: none; border: none; cursor: pointer; opacity: 0.7;">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            max-width: 400px;
            padding: 1rem;
            border-radius: 0.5rem;
            background: ${colors[type].bg};
            color: ${colors[type].color};
            border: 1px solid ${colors[type].border};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            font-family: Inter, sans-serif;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    function activateSecretMode() {
        showNotification('🎉 Secret mode activated! DigiConsult appreciates curious minds!', 'success');
        
        // Add rainbow animation to logo
        const logos = document.querySelectorAll('.nav-brand img');
        logos.forEach(logo => {
            logo.style.filter = 'hue-rotate(0deg)';
            logo.style.animation = 'rainbow 3s linear infinite';
        });
        
        // Add floating animation to service nodes
        const serviceNodes = document.querySelectorAll('.service-node');
        serviceNodes.forEach((node, index) => {
            setTimeout(() => {
                node.style.animation = `float 2s ease-in-out infinite ${index * 0.5}s`;
            }, index * 200);
        });
    }
});

// CSS Animations injected via JavaScript
const style = document.createElement('style');
style.textContent = `
    @keyframes confetti-fall {
        to {
            transform: translate(var(--dx), var(--dy)) rotate(720deg);
            opacity: 0;
        }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes rainbow {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(180deg); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .btn-ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .form-group.focused input,
    .form-group.focused select,
    .form-group.focused textarea {
        border-color: #E53E3E !important;
        box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1) !important;
    }
    
    .form-group.completed input,
    .form-group.completed select,
    .form-group.completed textarea {
        border-color: #16A085 !important;
    }
    
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    .hero-content h1,
    .tagline,
    .hero-actions .btn,
    .service-node {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .service-node {
        transform: scale(0.8);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .service-card,
    .tool-card,
    .module-card,
    .step,
    .trend-item {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
`;

document.head.appendChild(style);