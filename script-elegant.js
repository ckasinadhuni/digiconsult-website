// Elegant Enterprise Website with Sophisticated Whimsical Elements
// DigiConsult - Professional Excellence with Delightful Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all sophisticated systems
    initSophisticatedNavigation();
    initHeroInteractions();
    initServiceConstellation();
    initElegantScrollAnimations();
    initContactFormEnhancements();
    initAdvancedWhimsicalElements();
    initPerformanceOptimizations();
    
    // Sophisticated Navigation System
    function initSophisticatedNavigation() {
        const navbar = document.getElementById('navbar');
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        const navLinks = document.querySelectorAll('.nav-link, .nav-cta');
        
        let isScrolling = false;
        let lastScrollY = window.scrollY;
        
        // Advanced navbar scroll behavior with momentum
        window.addEventListener('scroll', () => {
            if (!isScrolling) {
                window.requestAnimationFrame(() => {
                    const currentScrollY = window.scrollY;
                    const scrollDirection = currentScrollY > lastScrollY ? 'down' : 'up';
                    
                    if (currentScrollY > 100) {
                        navbar.classList.add('scrolled');
                        
                        // Auto-hide on scroll down, show on scroll up (with momentum detection)
                        if (scrollDirection === 'down' && currentScrollY > 200) {
                            navbar.style.transform = 'translateY(-100%)';
                        } else if (scrollDirection === 'up' || currentScrollY < 200) {
                            navbar.style.transform = 'translateY(0)';
                        }
                    } else {
                        navbar.classList.remove('scrolled');
                        navbar.style.transform = 'translateY(0)';
                    }
                    
                    lastScrollY = currentScrollY;
                    isScrolling = false;
                });
                isScrolling = true;
            }
        });
        
        // Elegant smooth scrolling with easing
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (this.getAttribute('href').startsWith('#')) {
                    e.preventDefault();
                    const targetId = this.getAttribute('href');
                    const targetSection = document.querySelector(targetId);
                    
                    if (targetSection) {
                        // Sophisticated scroll animation with anticipation
                        this.style.transform = 'scale(0.98)';
                        this.style.transition = 'transform 0.1s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                        
                        setTimeout(() => {
                            this.style.transform = 'scale(1)';
                            
                            const offsetTop = targetSection.offsetTop - 80;
                            
                            // Custom smooth scroll with easing
                            smoothScrollTo(offsetTop, 1000);
                            
                            // Close mobile menu with elegance
                            if (navMenu.classList.contains('active')) {
                                navMenu.style.opacity = '0';
                                navMenu.style.transform = 'translateY(-20px)';
                                setTimeout(() => {
                                    navMenu.classList.remove('active');
                                    navMenu.style.opacity = '1';
                                    navMenu.style.transform = 'translateY(0)';
                                }, 300);
                            }
                        }, 100);
                    }
                }
            });
        });
        
        // Mobile navigation with sophisticated animations
        if (navToggle) {
            navToggle.addEventListener('click', function() {
                const isActive = navMenu.classList.contains('active');
                const icon = this.querySelector('i');
                
                // Sophisticated toggle animation
                this.style.transform = 'scale(0.9) rotate(180deg)';
                this.style.transition = 'transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                
                setTimeout(() => {
                    if (!isActive) {
                        navMenu.classList.add('active');
                        icon.className = 'fas fa-times';
                        navMenu.style.opacity = '0';
                        navMenu.style.transform = 'translateY(-20px)';
                        
                        setTimeout(() => {
                            navMenu.style.opacity = '1';
                            navMenu.style.transform = 'translateY(0)';
                        }, 50);
                    } else {
                        navMenu.style.opacity = '0';
                        navMenu.style.transform = 'translateY(-20px)';
                        icon.className = 'fas fa-bars';
                        
                        setTimeout(() => {
                            navMenu.classList.remove('active');
                            navMenu.style.opacity = '1';
                            navMenu.style.transform = 'translateY(0)';
                        }, 200);
                    }
                    
                    this.style.transform = 'scale(1) rotate(0deg)';
                }, 150);
            });
        }
        
        // Active section highlighting with smooth transitions
        const sections = document.querySelectorAll('section[id]');
        const observerOptions = {
            threshold: 0.3,
            rootMargin: '-80px 0px -50% 0px'
        };
        
        const navigationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const activeLink = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
                    
                    // Remove active class from all links
                    navLinks.forEach(link => link.classList.remove('active'));
                    
                    // Add active class with smooth transition
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            });
        }, observerOptions);
        
        sections.forEach(section => navigationObserver.observe(section));
    }
    
    // Hero Section Sophisticated Interactions
    function initHeroInteractions() {
        const heroElements = {
            tagline: document.querySelector('.hero-tagline'),
            title: document.querySelector('.hero-title'),
            description: document.querySelector('.hero-description'),
            actions: document.querySelector('.hero-actions'),
            visual: document.querySelector('.hero-visual')
        };
        
        // Staggered entrance animations with sophisticated timing
        const entranceSequence = [
            { element: heroElements.tagline, delay: 200 },
            { element: heroElements.title, delay: 400 },
            { element: heroElements.description, delay: 600 },
            { element: heroElements.actions, delay: 800 },
            { element: heroElements.visual, delay: 1000 }
        ];
        
        entranceSequence.forEach(({ element, delay }) => {
            if (element) {
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, delay);
            }
        });
        
        // Hero buttons with advanced micro-interactions
        const heroButtons = document.querySelectorAll('.hero-actions .btn');
        heroButtons.forEach((btn, index) => {
            // Ripple effect system
            btn.addEventListener('click', function(e) {
                createAdvancedRipple(this, e);
            });
            
            // Sophisticated hover states
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
                this.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
                
                // Subtle glow effect
                this.style.boxShadow = '0 25px 50px -12px rgba(229, 62, 62, 0.25)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '';
            });
        });
    }
    
    // Service Constellation Interactive System
    function initServiceConstellation() {
        const constellation = document.querySelector('.service-constellation');
        const serviceOrbs = document.querySelectorAll('.service-orb');
        
        if (!constellation) return;
        
        // Interactive orb behaviors
        serviceOrbs.forEach((orb, index) => {
            // Entrance animation with stagger
            setTimeout(() => {
                orb.style.opacity = '1';
                orb.style.transform = 'scale(1)';
            }, 1200 + (index * 200));
            
            // Sophisticated hover interactions
            orb.addEventListener('mouseenter', function() {
                // Scale and elevate the orb
                this.style.transform = 'scale(1.15) translateY(-8px)';
                this.style.transition = 'all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                this.style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.3)';
                this.style.zIndex = '10';
                
                // Create connecting lines to other orbs
                createConstellationConnections(this, serviceOrbs);
                
                // Show service information tooltip
                showServiceTooltip(this, getServiceInfo(this.dataset.service));
            });
            
            orb.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) translateY(0)';
                this.style.boxShadow = '';
                this.style.zIndex = '';
                
                // Remove connections
                removeConstellationConnections();
                hideServiceTooltip();
            });
            
            // Click interaction with service showcase
            orb.addEventListener('click', function() {
                const serviceType = this.dataset.service;
                const serviceCard = document.querySelector(`.service-showcase-card[data-service="${serviceType}"]`);
                
                if (serviceCard) {
                    // Smooth scroll to service with highlight
                    smoothScrollTo(serviceCard.offsetTop - 100, 800);
                    
                    // Highlight the service card
                    setTimeout(() => {
                        highlightServiceCard(serviceCard);
                    }, 400);
                }
                
                // Celebration effect
                createConstellationCelebration(this);
            });
        });
        
        // Ambient constellation movement
        setInterval(() => {
            serviceOrbs.forEach((orb, index) => {
                if (!orb.matches(':hover')) {
                    const randomFloat = (Math.random() - 0.5) * 4;
                    orb.style.transform += ` translateY(${randomFloat}px)`;
                    
                    setTimeout(() => {
                        orb.style.transform = orb.style.transform.replace(` translateY(${randomFloat}px)`, '');
                    }, 2000);
                }
            });
        }, 4000);
    }
    
    // Elegant Scroll Animations
    function initElegantScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const elegantObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    
                    // Different animation types based on element
                    if (element.classList.contains('service-showcase-card')) {
                        animateServiceCard(element);
                    } else if (element.classList.contains('metric-value')) {
                        animateCounterValue(element);
                    } else {
                        // Default elegant fade-in
                        element.style.opacity = '1';
                        element.style.transform = 'translateY(0)';
                    }
                    
                    elegantObserver.unobserve(element);
                }
            });
        }, observerOptions);
        
        // Observe all animatable elements
        const animatableElements = document.querySelectorAll(
            '.service-showcase-card, .metric-value, .contact-info-item, .section-intro'
        );
        
        animatableElements.forEach(el => {
            // Set initial state
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            
            elegantObserver.observe(el);
        });
    }
    
    // Enhanced Contact Form
    function initContactFormEnhancements() {
        const contactForm = document.getElementById('contactForm');
        const formInputs = contactForm.querySelectorAll('input, select, textarea');
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        
        // Progressive form enhancement
        formInputs.forEach(input => {
            let hasBeenFocused = false;
            
            // Focus animations
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
                
                if (!hasBeenFocused) {
                    this.style.transform = 'scale(1.02) translateY(-2px)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1) translateY(0)';
                    }, 200);
                    hasBeenFocused = true;
                }
                
                // Elegant focus indicator
                this.style.borderColor = 'var(--brand-red)';
                this.style.boxShadow = '0 0 0 3px rgba(229, 62, 62, 0.1)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                this.style.borderColor = '';
                this.style.boxShadow = '';
                
                if (this.value.trim()) {
                    this.parentElement.classList.add('completed');
                    showFieldSuccessIndicator(this);
                } else {
                    this.parentElement.classList.remove('completed');
                }
            });
            
            // Real-time validation feedback
            input.addEventListener('input', function() {
                const isValid = this.value.trim() !== '';
                
                if (isValid) {
                    this.style.borderColor = 'var(--teal)';
                } else {
                    this.style.borderColor = '';
                }
            });
        });
        
        // Enhanced form submission
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Sophisticated validation
            const formData = new FormData(contactForm);
            const requiredFields = ['name', 'email', 'service', 'message'];
            const missingFields = [];
            
            requiredFields.forEach(field => {
                if (!formData.get(field)) {
                    missingFields.push(field);
                }
            });
            
            if (missingFields.length > 0) {
                showElegantNotification('Please complete all required fields to proceed with your consultation request.', 'warning');
                highlightMissingFields(missingFields);
                return;
            }
            
            // Email validation
            const email = formData.get('email');
            if (!isValidEmail(email)) {
                showElegantNotification('Please enter a valid email address so our team can reach you.', 'warning');
                return;
            }
            
            // Create sophisticated mailto link
            const subject = `${formData.get('service')} - Enterprise Consultation Request from ${formData.get('name')}`;
            const company = formData.get('company') ? `\nCompany: ${formData.get('company')}` : '';
            const body = `Name: ${formData.get('name')}\nEmail: ${formData.get('email')}${company}\nService Interest: ${formData.get('service')}\n\nMessage:\n${formData.get('message')}\n\n---\nSubmitted via DigiConsult contact form\nTimestamp: ${new Date().toISOString()}`;
            
            const mailtoLink = `mailto:ck@digiconsult.ca?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            
            // Elegant submission sequence
            submitBtn.innerHTML = '<i class="fas fa-satellite-dish"></i> Preparing consultation request...';
            submitBtn.style.transform = 'scale(0.98)';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-rocket"></i> Launching communication...';
                submitBtn.style.background = 'linear-gradient(135deg, var(--teal), var(--indigo))';
                
                setTimeout(() => {
                    window.location.href = mailtoLink;
                    
                    setTimeout(() => {
                        showElegantNotification('Your consultation request is ready! We\'ll respond within 24 hours with strategic insights. 🚀', 'success');
                        
                        // Reset form with elegant animations
                        resetFormWithStyle(contactForm, submitBtn);
                        
                        // Celebration
                        createFormCelebration(submitBtn);
                    }, 1000);
                }, 1200);
            }, 800);
        });
    }
    
    // Advanced Whimsical Elements
    function initAdvancedWhimsicalElements() {
        // Cursor enhancement for interactive elements
        const interactiveElements = document.querySelectorAll('a, button, .service-orb, .service-showcase-card');
        
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                document.body.style.cursor = 'pointer';
                this.style.cursor = 'pointer';
            });
            
            element.addEventListener('mouseleave', function() {
                document.body.style.cursor = 'default';
            });
        });
        
        // Service cards with sophisticated interactions
        const serviceCards = document.querySelectorAll('.service-showcase-card');
        serviceCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                // Elegant hover state
                this.style.transform = 'translateY(-12px) scale(1.02)';
                this.style.transition = 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
                
                // Icon animation
                const icon = this.querySelector('.service-icon-large');
                if (icon) {
                    icon.style.transform = 'scale(1.1) rotate(8deg)';
                    icon.style.transition = 'transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                }
                
                // Highlight tags animation
                const tags = this.querySelectorAll('.highlight-tag');
                tags.forEach((tag, index) => {
                    setTimeout(() => {
                        tag.style.transform = 'translateY(-2px) scale(1.05)';
                        tag.style.background = 'var(--brand-red)';
                        tag.style.color = 'white';
                    }, index * 50);
                });
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                
                const icon = this.querySelector('.service-icon-large');
                if (icon) {
                    icon.style.transform = 'scale(1) rotate(0deg)';
                }
                
                const tags = this.querySelectorAll('.highlight-tag');
                tags.forEach(tag => {
                    tag.style.transform = 'translateY(0) scale(1)';
                    tag.style.background = '';
                    tag.style.color = '';
                });
            });
        });
        
        // Contact info items with delightful interactions
        const contactItems = document.querySelectorAll('.contact-info-item');
        contactItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const icon = this.querySelector('.contact-icon');
                if (icon) {
                    icon.style.transform = 'scale(1.2) rotate(10deg)';
                    icon.style.background = 'linear-gradient(135deg, var(--brand-red), var(--gold))';
                }
            });
            
            item.addEventListener('mouseleave', function() {
                const icon = this.querySelector('.contact-icon');
                if (icon) {
                    icon.style.transform = 'scale(1) rotate(0deg)';
                    icon.style.background = '';
                }
            });
        });
        
        // Easter egg: Advanced Konami code with enterprise theme
        let konamiSequence = [];
        const enterpriseKonami = [83, 69, 82, 86, 73, 67, 69, 78, 79, 87]; // SERVICENOW
        
        document.addEventListener('keydown', function(e) {
            konamiSequence.push(e.keyCode);
            if (konamiSequence.length > 10) {
                konamiSequence.shift();
            }
            
            if (JSON.stringify(konamiSequence) === JSON.stringify(enterpriseKonami)) {
                activateEnterpriseMode();
                konamiSequence = [];
            }
        });
    }
    
    // Performance Optimizations
    function initPerformanceOptimizations() {
        // Lazy load background images
        const elementsWithBg = document.querySelectorAll('[data-bg]');
        const bgObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.style.backgroundImage = `url(${element.dataset.bg})`;
                    bgObserver.unobserve(element);
                }
            });
        });
        
        elementsWithBg.forEach(el => bgObserver.observe(el));
        
        // Optimize scroll performance
        let ticking = false;
        function updateScrollBasedAnimations() {
            // Parallax effects for hero section
            const scrolled = window.pageYOffset;
            const hero = document.querySelector('.hero');
            
            if (hero && scrolled < window.innerHeight) {
                const rate = scrolled * -0.3;
                hero.style.transform = `translateY(${rate}px)`;
            }
            
            ticking = false;
        }
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateScrollBasedAnimations);
                ticking = true;
            }
        });
    }
    
    // Utility Functions
    function smoothScrollTo(targetY, duration) {
        const startY = window.pageYOffset;
        const difference = targetY - startY;
        const startTime = performance.now();
        
        function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = elapsed / duration;
            
            if (progress < 1) {
                const ease = easeInOutCubic(progress);
                window.scrollTo(0, startY + (difference * ease));
                requestAnimationFrame(step);
            } else {
                window.scrollTo(0, targetY);
            }
        }
        
        requestAnimationFrame(step);
    }
    
    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    }
    
    function createAdvancedRipple(element, event) {
        const ripple = document.createElement('span');
        ripple.classList.add('advanced-ripple');
        
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height) * 2;
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%);
            pointer-events: none;
            transform: scale(0);
            animation: advanced-ripple 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
            z-index: 1;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 800);
    }
    
    function createConstellationConnections(activeOrb, allOrbs) {
        const connections = [];
        const activeRect = activeOrb.getBoundingClientRect();
        const activeCenterX = activeRect.left + activeRect.width / 2;
        const activeCenterY = activeRect.top + activeRect.height / 2;
        
        allOrbs.forEach(orb => {
            if (orb !== activeOrb) {
                const orbRect = orb.getBoundingClientRect();
                const orbCenterX = orbRect.left + orbRect.width / 2;
                const orbCenterY = orbRect.top + orbRect.height / 2;
                
                const line = document.createElement('div');
                line.className = 'constellation-connection';
                
                const distance = Math.sqrt(
                    Math.pow(orbCenterX - activeCenterX, 2) + 
                    Math.pow(orbCenterY - activeCenterY, 2)
                );
                
                const angle = Math.atan2(orbCenterY - activeCenterY, orbCenterX - activeCenterX);
                
                line.style.cssText = `
                    position: fixed;
                    left: ${activeCenterX}px;
                    top: ${activeCenterY}px;
                    width: ${distance}px;
                    height: 2px;
                    background: linear-gradient(90deg, var(--brand-red), transparent);
                    transform-origin: 0 50%;
                    transform: rotate(${angle}rad) scaleX(0);
                    animation: constellation-line 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
                    pointer-events: none;
                    z-index: 1;
                `;
                
                document.body.appendChild(line);
                connections.push(line);
            }
        });
        
        // Store connections for cleanup
        activeOrb._connections = connections;
    }
    
    function removeConstellationConnections() {
        document.querySelectorAll('.constellation-connection').forEach(line => line.remove());
    }
    
    function getServiceInfo(serviceType) {
        const serviceData = {
            core: { name: 'ServiceNow Platform', description: 'Complete enterprise service management ecosystem' },
            itsm: { name: 'ITSM Suite', description: 'IT Service Management with intelligent automation' },
            itom: { name: 'ITOM Operations', description: 'IT Operations Management with AIOps' },
            spm: { name: 'SPM Portfolio', description: 'Strategic Portfolio Management excellence' },
            ai: { name: 'AI Automation', description: 'Intelligent enterprise automation solutions' }
        };
        
        return serviceData[serviceType] || { name: 'Enterprise Solution', description: 'Professional consulting services' };
    }
    
    function showServiceTooltip(element, serviceInfo) {
        const tooltip = document.createElement('div');
        tooltip.className = 'service-tooltip';
        tooltip.innerHTML = `
            <h4>${serviceInfo.name}</h4>
            <p>${serviceInfo.description}</p>
        `;
        
        tooltip.style.cssText = `
            position: fixed;
            background: var(--charcoal);
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            font-size: 0.9rem;
            z-index: 1000;
            opacity: 0;
            transform: scale(0.8);
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            pointer-events: none;
            max-width: 200px;
        `;
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = (rect.left + rect.width / 2) + 'px';
        tooltip.style.top = (rect.bottom + 10) + 'px';
        
        document.body.appendChild(tooltip);
        
        setTimeout(() => {
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'scale(1)';
        }, 50);
        
        element._tooltip = tooltip;
    }
    
    function hideServiceTooltip() {
        document.querySelectorAll('.service-tooltip').forEach(tooltip => tooltip.remove());
    }
    
    function showElegantNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `elegant-notification notification-${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle',
            info: 'fas fa-info-circle'
        };
        
        const colors = {
            success: { bg: 'linear-gradient(135deg, #10B981, #059669)', color: 'white' },
            warning: { bg: 'linear-gradient(135deg, #F59E0B, #D97706)', color: 'white' },
            error: { bg: 'linear-gradient(135deg, #EF4444, #DC2626)', color: 'white' },
            info: { bg: 'linear-gradient(135deg, #3B82F6, #2563EB)', color: 'white' }
        };
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem;">
                <i class="${icons[type]}" style="font-size: 1.25rem;"></i>
                <span style="flex: 1;">${message}</span>
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            max-width: 400px;
            padding: 1.5rem;
            border-radius: 1rem;
            background: ${colors[type].bg};
            color: ${colors[type].color};
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            z-index: 10000;
            opacity: 0;
            transform: translateX(100%) scale(0.8);
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            font-family: var(--font-primary);
            font-weight: 500;
            backdrop-filter: blur(10px);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0) scale(1)';
        }, 100);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%) scale(0.8)';
            setTimeout(() => notification.remove(), 400);
        }, 5000);
    }
    
    function activateEnterpriseMode() {
        showElegantNotification('🎉 Enterprise Excellence Mode Activated! ServiceNow specialists appreciate attention to detail!', 'success');
        
        // Add premium visual effects
        const serviceOrbs = document.querySelectorAll('.service-orb');
        serviceOrbs.forEach((orb, index) => {
            setTimeout(() => {
                orb.style.animation = `enterprise-pulse 2s ease-in-out infinite ${index * 0.3}s`;
            }, index * 200);
        });
        
        // Add golden border to service cards
        const serviceCards = document.querySelectorAll('.service-showcase-card');
        serviceCards.forEach(card => {
            card.style.border = '2px solid var(--gold)';
            card.style.boxShadow = '0 25px 50px -12px rgba(214, 158, 46, 0.2)';
        });
    }
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    function resetFormWithStyle(form, submitBtn) {
        form.reset();
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Request Strategic Consultation';
        submitBtn.style.background = '';
        submitBtn.style.transform = 'scale(1)';
        submitBtn.disabled = false;
        
        // Clear form states
        const formGroups = form.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            group.classList.remove('focused', 'completed');
        });
    }
    
    // Animation keyframes via JavaScript
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        @keyframes advanced-ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
        
        @keyframes constellation-line {
            to {
                transform: rotate(var(--angle)) scaleX(1);
            }
        }
        
        @keyframes enterprise-pulse {
            0%, 100% {
                box-shadow: 0 0 0 0 var(--gold);
                transform: scale(1);
            }
            50% {
                box-shadow: 0 0 0 20px transparent;
                transform: scale(1.05);
            }
        }
        
        .form-group.focused .form-label {
            color: var(--brand-red);
            transform: translateY(-2px);
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        .form-group.completed .form-input,
        .form-group.completed .form-select,
        .form-group.completed .form-textarea {
            border-color: var(--teal);
            background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%);
        }
        
        .navbar {
            transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    `;
    
    document.head.appendChild(styleSheet);
});

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeWebsite);
} else {
    initializeWebsite();
}

function initializeWebsite() {
    console.log('🚀 DigiConsult - Enterprise Excellence Initialized');
}