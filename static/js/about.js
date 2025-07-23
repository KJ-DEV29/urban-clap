// Animate the "OUR SERVICES" hero section and cards with GSAP and ScrollTrigger

// Ensure GSAP and ScrollTrigger are loaded in your HTML for this to work

document.addEventListener("DOMContentLoaded", function () {
    // Animate the hero section
    if (document.querySelector('.hero-section')) {
        gsap.from(".hero-section h1", {
            y: 60,
            opacity: 0,
            duration: 1,
            ease: "power3.out"
        });
        gsap.from(".hero-section .lead", {
            y: 40,
            opacity: 0,
            duration: 1,
            delay: 0.3,
            ease: "power3.out"
        });
    }

    // Animate main service cards
    gsap.utils.toArray('.row.mb-5 .card.h-100').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top 80%",
                toggleActions: "play none none none"
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            delay: i * 0.15,
            ease: "power2.out"
        });
    });

    // Animate premium service cards
    gsap.utils.toArray('.card.text-center.h-100').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top 85%",
                toggleActions: "play none none none"
            },
            y: 40,
            opacity: 0,
            duration: 0.7,
            delay: i * 0.1,
            ease: "power2.out"
        });
    });

    // Animate blood type cards
    gsap.utils.toArray('.blood-type-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top 90%",
                toggleActions: "play none none none"
            },
            scale: 0.8,
            opacity: 0,
            duration: 0.6,
            delay: i * 0.05,
            ease: "back.out(1.7)"
        });
    });

    // Animate donation process steps
    gsap.utils.toArray('.process-step').forEach((step, i) => {
        gsap.from(step, {
            scrollTrigger: {
                trigger: step,
                start: "top 95%",
                toggleActions: "play none none none"
            },
            y: 30,
            opacity: 0,
            duration: 0.5,
            delay: i * 0.1,
            ease: "power1.out"
        });
    });

    // Animate pricing cards
    gsap.utils.toArray('.pricing-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top 90%",
                toggleActions: "play none none none"
            },
            y: 40,
            opacity: 0,
            duration: 0.7,
            delay: i * 0.1,
            ease: "power2.out"
        });
    });

    // Animate CTA section
    if (document.querySelector('.cta-section')) {
        gsap.from('.cta-section', {
            scrollTrigger: {
                trigger: '.cta-section',
                start: "top 80%",
                toggleActions: "play none none none"
            },
            scale: 0.95,
            opacity: 0,
            duration: 1,
            ease: "power2.out"
        });
    }
});



// Animate "Mission & Vision" cards
gsap.utils.toArray('.row.mb-5 .card.h-100').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: "top 90%",
            toggleActions: "play none none none"
        },
        y: 40,
        opacity: 0,
        duration: 0.7,
        delay: i * 0.1,
        ease: "power2.out"
    });
});

// Animate "Our Story" card
if (document.querySelector('.card-header h4 .fa-history')) {
    gsap.from('.card-header h4 .fa-history', {
        scrollTrigger: {
            trigger: '.card-header h4 .fa-history',
            start: "top 95%",
            toggleActions: "play none none none"
        },
        x: -30,
        opacity: 0,
        duration: 0.7,
        ease: "power2.out"
    });
    gsap.from('.card-header h4', {
        scrollTrigger: {
            trigger: '.card-header h4',
            start: "top 95%",
            toggleActions: "play none none none"
        },
        y: 30,
        opacity: 0,
        duration: 0.7,
        delay: 0.2,
        ease: "power2.out"
    });
    gsap.from('.card-body .lead', {
        scrollTrigger: {
            trigger: '.card-body .lead',
            start: "top 95%",
            toggleActions: "play none none none"
        },
        x: 30,
        opacity: 0,
        duration: 0.7,
        delay: 0.3,
        ease: "power2.out"
    });
}

// Animate "Core Principles" cards
gsap.utils.toArray('.section-header + .col-md-3 .card, .section-header + .col-md-3 ~ .col-md-3 .card').forEach((card, i) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: "top 92%",
            toggleActions: "play none none none"
        },
        y: 40,
        opacity: 0,
        duration: 0.7,
        delay: i * 0.1,
        ease: "power2.out"
    });
});

// Animate "Leadership Team" cards
gsap.utils.toArray('.team-member').forEach((member, i) => {
    gsap.from(member, {
        scrollTrigger: {
            trigger: member,
            start: "top 95%",
            toggleActions: "play none none none"
        },
        y: 40,
        opacity: 0,
        duration: 0.7,
        delay: i * 0.1,
        ease: "power2.out"
    });
});

// Animate blood drop icon
if (document.querySelector('.blood-drop')) {
    gsap.from('.blood-drop', {
        scrollTrigger: {
            trigger: '.blood-drop',
            start: "top 95%",
            toggleActions: "play none none none"
        },
        scale: 0.7,
        opacity: 0,
        duration: 0.8,
        ease: "back.out(1.7)"
    });
}

// Animate section headers
gsap.utils.toArray('.section-header').forEach((header, i) => {
    gsap.from(header, {
        scrollTrigger: {
            trigger: header,
            start: "top 96%",
            toggleActions: "play none none none"
        },
        y: 30,
        opacity: 0,
        duration: 0.7,
        delay: i * 0.1,
        ease: "power2.out"
    });
});
