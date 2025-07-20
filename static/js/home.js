gsap.registerPlugin(ScrollTrigger);

// hero

gsap.to(".hero-head", {
  y: -255,
  duration: 0.5, // animate in 0.5 seconds
  ease: "power1.in",

  scrollTrigger: {
    trigger: ".hero",
    start: "bottom 99%",
    end: "+=500vh",
    toggleActions: "play none play none", // reanimate on enter/leave both ways
    pin: true,
    pinSpacing: true,
  },
});

gsap.to(".botom-para", {
  y: -70,
  duration: 0.5, // animate in 0.5 seconds
  ease: "power1.in",

  toggleActions: "play none play none", // reanimate on enter/leave both ways
  scrollTrigger: {
    trigger: ".hero",
    start: "bottom 99%",
    // No scrub, so animation happens instantly on trigger
  },
});

// sec-2

gsap.from(".sec-two h1", {
  opacity: 0,
  scrollTrigger: {
    trigger: ".sec-two",
    start: "center center",
    pin: true,
    end: "bottom 0%",
    toggleActions: "play reverse play reverse",
    pinSpacing: true,
  },
});
