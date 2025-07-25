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


// event-sec

let eventCards = Array.from(
  document.querySelectorAll(".event-sec .event")
).reverse();

// Set initial rotation and opacity for all cards
gsap.set(eventCards, {
  // rotate: -10,
  // opacity: 0,
  // y: 100,
});

// Create a master timeline tied to scroll
let masterTL = gsap.timeline({
  scrollTrigger: {
    trigger: ".event-sec",
    start: "top top",
    end: `+=${eventCards.length * 150}vh`, // 100vh per card
    pin: true,
    scrub: true,
    anticipatePin: 1,
  },
});

// Animate each card in sequence
eventCards.forEach((card, i) => {
  masterTL
    .to(
      card,
      {
        opacity: 1,
        rotate: 0,
        y: 0,
        duration: 0.5,
        ease: "power2.out",
      },
      i
    ) // position at index in timeline

    .to(
      card,
      {
        opacity: 0,
        y: -100,
        duration: 0.5,
        ease: "power2.in",
      },
      i + 0.5
    );
});



// learnmore
let learnmoreTl = gsap.timeline({
  scrollTrigger: {
    trigger: ".how-it-works",
    start : 'top center',
    toggleActions : 'play reverse play reverse'
  },
});

learnmoreTl.to('.how-it-works .part div',{
  width : 200,
}).to('.how-it-works img',{
  x : 0
}).to('.how-it-works .part div p',{
  y:0,
})

gsap.to('.how-it-works',{
  scrollTrigger : {
    trigger : ".how-it-works",
    start: "center center",
    end : "+=200vh",
    pin : true,
    pinSpacing : true,
    anticipatePin : true
  }
})

gsap.to('.steps-sec .step-odd',{
  y : 200,
  scrollTrigger : {
    trigger : '.steps-sec',
    start : "top bottom",
    end : "bottom top",
    scrub : 0.1
  }
})

gsap.to(".steps-sec .step-even", {
  y: -200,
  scrollTrigger: {
    trigger: ".steps-sec",
    start: "top bottom",
    end: "bottom top",
    scrub: 0.1,
  },
});




// faq
gsap.to('.faq-slider',{
  scrollTrigger : {
    trigger : '.faq-slider',
    pin:true,
    start : "top 10%",
    end : "+=1000vh",
    pinSpacing : false
  }
})


// qna

let qnas = document.querySelectorAll('.qna-sec .qna')
let allQnaH2 = document.querySelectorAll('.qna-sec .qna h2')
qnas.forEach((qna, i) => {
  qna.addEventListener('click', () => {

    gsap.to('.qna-sec .qna',{
      height : 140
    })

    gsap.to(qna,{
      height : 270,
    })


    gsap.to(allQnaH2, {
      background: "#1a1a1a",
    });
    gsap.to(allQnaH2[i],{
      background : 'transparent',

    })

  })
})


