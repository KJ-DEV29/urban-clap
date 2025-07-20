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




// card - sec

gsap.to(".cards-sec img", {
  y: 0,
  stagger: 0.1,
  scrollTrigger: {
    trigger: ".cards-sec .card",
    start: "top 45%",
    toggleActions: "play reverse play reverse",
  },
});

gsap.to('.cards-sec' , {
    scrollTrigger : {
        trigger : '.cards-sec',
        start : 'center center',
        pin : true,
        end : "+=400vh",
        pinSpacing : true
    }
})

let allCards = document.querySelectorAll(".cards-sec .card img");
let allcardText = document.querySelectorAll(".cards-sec .card .content");
let allcardBg = document.querySelectorAll(".cards-sec .content .bg");
allCards.forEach((card, idx) => {
    card.addEventListener('mouseenter' , () => {
        gsap.to(allcardText[idx], {
            x : 0
        })

        gsap.to(allcardBg[idx], {
            scaleX : "100%",
            delay : 0.2
        })
    })

    card.addEventListener("mouseleave", () => {
      gsap.to(allcardText[idx], {
        x: '-100%',
      });

      gsap.to(allcardBg[idx], {
        scaleX: "0",
        delay: 0.2,
      });
    });
})