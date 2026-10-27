(function($) {

    "use strict";


    if ($('.popup-with-zoom-anim').length) {
        $('.popup-with-zoom-anim').magnificPopup({
            type: 'inline',

            fixedContentPos: false,
            fixedBgPos: true,

            overflowY: 'auto',

            closeBtnInside: true,
            preloader: false,

            midClick: true,
            removalDelay: 300,
            mainClass: 'my-mfp-zoom-in'
        });
    }
    
    // Instant Non-Blocking Preloader Release
    function handlePreloader() {
        var $pre = $('.preloader');
        if ($pre.length) {
            $pre.removeClass('nav-transitioning').addClass('loaded').hide();
        }
    }

    // High-Performance Instant Hover Prefetcher (Caches target page into HTTP cache on hover)
    function initInstantNavigationPrefetch() {
        var prefetched = {};
        $(document).on('pointerenter mouseenter', 'a[href]', function() {
            var href = $(this).attr('href');
            if (!href || href === '#' || href.indexOf('javascript:') === 0) return;
            if (href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return;
            if (href.indexOf('wa.me') !== -1 || href.indexOf('whatsapp') !== -1) return;
            if ($(this).attr('target') === '_blank') return;
            if (href.indexOf('#') === 0) return;

            try {
                var url = new URL(href, window.location.href);
                if (url.origin !== window.location.origin) return;
                var cleanPath = url.pathname;
                if (!prefetched[cleanPath] && cleanPath.endsWith('.html')) {
                    prefetched[cleanPath] = true;
                    var link = document.createElement('link');
                    link.rel = 'prefetch';
                    link.href = cleanPath;
                    document.head.appendChild(link);
                }
            } catch (e) {}
        });
    }

    // Universal Floating WhatsApp Widget
    function initFloatingWhatsApp() {
        if ($('#dalal-wa-float-btn').length) return;
        var defaultText = encodeURIComponent("Hello Mr. Vinit Dalal, I have an inquiry regarding Dalal Machine Tools machinery.");
        var html = '<a href="https://wa.me/919821232131?text=' + defaultText + '" target="_blank" id="dalal-wa-float-btn" class="dalal-wa-float" title="Chat with Mr. Vinit Dalal on WhatsApp" rel="noopener noreferrer">' +
                   '  <div class="dalal-wa-pulse"></div>' +
                   '  <i class="fa fa-whatsapp"></i>' +
                   '  <span class="dalal-wa-label">WhatsApp RFQ</span>' +
                   '</a>';
        $('body').append(html);
    }

    // Immediate execution on DOM ready - Zero artificial delay
    $(document).ready(function() {
        handlePreloader();
        initInstantNavigationPrefetch();
        initFloatingWhatsApp();
    });
    // Instant fallback
    handlePreloader();

    //Update Header Style and Scroll to Top
    function headerStyle() {
        if ($('.main-header').length) {
            var windowpos = $(window).scrollTop();
            var siteHeader = $('.main-header');
            var sticky_Header = $('.sticky-header');
            var scrollLink = $('.scroll-to-top');
            if (windowpos >= 300) {
                sticky_Header.addClass("animated slideInDown")
                siteHeader.addClass('fixed-header');
                scrollLink.fadeIn(300);
            } else {
                sticky_Header.removeClass("animated slideInDown")
                siteHeader.removeClass('fixed-header');
                scrollLink.fadeOut(300);
            }
        }
    }

    headerStyle();

    if ($("#polyglot-language-options").length) {
        $('#polyglotLanguageSwitcher').polyglotLanguageSwitcher({
            effect: 'fade',
            testMode: true,
            onChange: function(evt) {
                    alert("The selected language is: " + evt.selectedItem);
                }
                //                ,afterLoad: function(evt){
                //                    alert("The selected language has been loaded");
                //                },
                //                beforeOpen: function(evt){
                //                    alert("before open");
                //                },
                //                afterOpen: function(evt){
                //                    alert("after open");
                //                },
                //                beforeClose: function(evt){
                //                    alert("before close");
                //                },
                //                afterClose: function(evt){
                //                    alert("after close");
                //                }
        });
    };

    if ($('.area_select').length) {
        $('.area_select').on('change', function() {
            var val = $(this).val();
            if (val) {
                $('.state:not(#value' + val + ')').slideUp();
                $('#value' + val).slideDown();
            } else {
                $('.state').slideDown();
            }
        });
    }

    //Main Slider Carousel
    if ($('.main-slider-carousel').length) {
        $('.main-slider-carousel').owlCarousel({
            loop: true,
            margin: 0,
            nav: true,
            dots: true,
            smartSpeed: 800,
            autoplay: 6000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            items: 1,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1200: {
                    items: 1
                }
            }
        });
    }

    //Single Item- Carousel
    if ($('.single-item-carousel').length) {
        $('.single-item-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1200: {
                    items: 1
                }
            }
        });
    }


    //Submenu Dropdown Toggle
    if ($('.main-header .navigation li.dropdown ul').length) {
        $('.main-header .navigation li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

        //Dropdown Button
        $('.main-header .navigation li.dropdown .dropdown-btn').on('click', function() {
            $(this).prev('ul').slideToggle(500);
        });

        //Disable dropdown parent link
        $('.navigation li.dropdown > a').on('click', function(e) {
            e.preventDefault();
        });
    }

    //Info - Carousel
    if ($('.info-carousel').length) {
        $('.info-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1200: {
                    items: 1
                }
            }
        });
    }


    //Single Item Carousel
    if ($('.highlight-carousel').length) {
        $('.highlight-carousel').owlCarousel({
            loop: true,
            margin: 20,
            nav: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                800: {
                    items: 1
                },
                1024: {
                    items: 1,
                },
                1200: {
                    items: 1
                }
            }
        });
    }

    //Services Carousel
    if ($('.services-carousel').length) {
        $('.services-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                778: {
                    items: 2
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
    }

    //Services Carousel
    if ($('.project-carousel').length) {
        $('.project-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            center: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                778: {
                    items: 2
                },
                800: {
                    items: 2
                },
                991: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
    }

    //Services Carousel
    if ($('.project-two-carousel').length) {
        $('.project-two-carousel').owlCarousel({
            loop: true,
            margin: 50,
            nav: false,
            center: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                778: {
                    items: 1
                },
                800: {
                    items: 1
                },
                991: {
                    items: 1
                },
                1200: {
                    items: 1,
                    margin: 0,
                    stagePadding: 175,
                },
                1500: {
                    items: 1,
                    stagePadding: 400
                }
            }
        });
        $('.project-style-two-carousel-nav.btn-prev').on('click', function() {
           $('.project-two-carousel').trigger('next.owl.carousel'); 
        });
        $('.project-style-two-carousel-nav.btn-next').on('click', function() {
           $('.project-two-carousel').trigger('prev.owl.carousel'); 
        });
    }
        //Services Carousel
    if ($('.testimonial-carousel').length) {
        $('.testimonial-carousel').owlCarousel({
            loop:true,
            margin:20,
            nav:false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: [ '<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>' ],
            responsive:{
                0:{
                    items:1
                },
                480:{
                    items:1
                },
                800:{
                    items:1
                },
                1024:{
                    items:1,
                },
                1200:{
                    items:1
                }
            }
        });         
    }

    //Services Carousel
    if ($('.testimonials-carousel').length) {
        $('.testimonials-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: false,
            dots: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 15
                },
                480: {
                    items: 1,
                    stagePadding: 15
                },
                800: {
                    items: 2,
                    stagePadding: 15
                },
                1024: {
                    items: 3,
                    stagePadding: 15
                },
                1200: {
                    items: 3,
                    stagePadding: 15
                }
            }
        });
    }
    //Services Carousel
    if ($('.testimonials-carousel-two').length) {
        $('.testimonials-carousel-two').owlCarousel({
            loop: true,
            margin: 30,
            nav: false,
            dots: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 15
                },
                480: {
                    items: 1,
                    stagePadding: 15
                },
                800: {
                    items: 2,
                    stagePadding: 15
                },
                1024: {
                    items: 3,
                    stagePadding: 15
                },
                1200: {
                    items: 3,
                    stagePadding: 15
                }
            }
        });
    }

    //client Carousel
    if ($('.clients-carousel').length) {
        $('.clients-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: false,
            dots: false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                800: {
                    items: 3
                },
                1024: {
                    items: 4
                },
                1200: {
                    items: 4
                }
            }
        });
    }

    //client Carousel
    if ($('.client-carousel-two').length) {
        $('.client-carousel-two').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            dots: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                800: {
                    items: 3
                },
                1024: {
                    items: 4
                },
                1200: {
                    items: 4
                }
            }
        });
    }

    //News Carousel
    if ($('.news-carousel').length) {
        $('.news-carousel').owlCarousel({
            loop: true,
            margin: 0,
            nav: false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                778: {
                    items: 2
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
    }

    //News 2 Carousel
    if ($('.blog-two-carousel').length) {
        $('.blog-two-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                778: {
                    items: 2
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 2
                },
                1200: {
                    items: 2
                }
            }
        });

        $('#blog-2-carousel-nav .prev-btn').on('click', function() {
           $('.blog-two-carousel').trigger('next.owl.carousel'); 
        });
        $('#blog-2-carousel-nav .next-btn').on('click', function() {
           $('.blog-two-carousel').trigger('prev.owl.carousel'); 
        });
    }

    //Sponsors Carousel
    if ($('.sponsors-carousel').length) {
        $('.sponsors-carousel').owlCarousel({
            loop: true,
            margin: 0,
            nav: false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                800: {
                    items: 4
                },
                1024: {
                    items: 5
                },
                1200: {
                    items: 6
                }
            }
        });
    }

    // Contact Carousel
    if ($('.contact-carousel').length) {
        $('.contact-carousel').owlCarousel({
            loop: true,
            margin: 20,
            nav: true,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                800: {
                    items: 1
                },
                1024: {
                    items: 1,
                },
                1200: {
                    items: 1
                }
            }
        });
    }

    // Contact Carousel
    if ($('.branches-carousel').length) {
        $('.branches-carousel').owlCarousel({
            loop: true,
            margin: 20,
            nav: true,
            smartSpeed: 700,
            autoplay: false,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                800: {
                    items: 1
                },
                1024: {
                    items: 1,
                },
                1200: {
                    items: 1
                }
            }
        });
    }

    //Branches- Carousel
    if ($('.industry-carousel').length) {
        $('.industry-carousel').owlCarousel({
            loop: true,
            margin: 0,
            nav: false,
            smartSpeed: 700,
            autoplay: 5000,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1024: {
                    items: 3
                },
                1440: {
                    items: 4,
                },
                1920: {
                    items: 5
                }
            }
        });
    }

    //Verticle Services Carousel
    if ($('.verticle-carousel').length) {
        $('.verticle-carousel').slick({
            dots: true,
            autoplay: true,
            loop: true,
            autoplaySpeed: 5000,
            infinite: true,
            responsive: true,
            slidesToShow: 2,
            vertical: true,
            prevArrow: '<button type="button" class="slick-prev"><span class="flaticon-fast-forward"><span></button>',
            nextArrow: '<button type="button" class="slick-next"><span class="flaticon-fast-forward"><span></button>',
            slidesToScroll: 1
        });
    }

    //Masonary
    function enableMasonry() {
        if ($('.masonry-items-container').length) {

            var winDow = $(window);
            // Needed variables
            var $container = $('.masonry-items-container');

            $container.isotope({
                itemSelector: '.masonry-item',
                masonry: {
                    columnWidth: 0
                },
                animationOptions: {
                    duration: 500,
                    easing: 'linear'
                }
            });

            winDow.on('resize', function() {

                $container.isotope({
                    itemSelector: '.masonry-item',
                    animationOptions: {
                        duration: 500,
                        easing: 'linear',
                        queue: false
                    }
                });
            });
        }
    }

    enableMasonry();


    //Gallery Filters
    if ($('.filter-list').length) {
        $('.filter-list').mixItUp({});
    }


    //Product Tabs
    if ($('.project-tab').length) {
        $('.project-tab .product-tab-btns .p-tab-btn').on('click', function(e) {
            e.preventDefault();
            var target = $($(this).attr('data-tab'));

            if ($(target).hasClass('actve-tab')) {
                return false;
            } else {
                $('.project-tab .product-tab-btns .p-tab-btn').removeClass('active-btn');
                $(this).addClass('active-btn');
                $('.project-tab .p-tabs-content .p-tab').removeClass('active-tab');
                $(target).addClass('active-tab');
            }
        });
    }


    //Price Range Slider
    if ($('.price-range-slider').length) {
        $(".price-range-slider").slider({
            range: true,
            min: 0,
            max: 90,
            values: [8, 85],
            slide: function(event, ui) {
                $("input.property-amount").val(ui.values[0] + " - " + ui.values[1]);
            }
        });

        $("input.property-amount").val($(".price-range-slider").slider("values", 0) + " - $" + $(".price-range-slider").slider("values", 1));
    }


    //Jquery Spinner / Quantity Spinner
    if ($('.quantity-spinner').length) {
        $("input.quantity-spinner").TouchSpin({
            verticalbuttons: true
        });
    }


    //Fact Counter + Text Count
    if ($('.count-box').length) {
        $('.count-box').appear(function() {

            var $t = $(this),
                n = $t.find(".count-text").attr("data-stop"),
                r = parseInt($t.find(".count-text").attr("data-speed"), 10);

            if (!$t.hasClass("counted")) {
                $t.addClass("counted");
                $({
                    countNum: $t.find(".count-text").text()
                }).animate({
                    countNum: n
                }, {
                    duration: r,
                    easing: "linear",
                    step: function() {
                        $t.find(".count-text").text(Math.floor(this.countNum));
                    },
                    complete: function() {
                        $t.find(".count-text").text(this.countNum);
                    }
                });
            }

        }, { accY: 0 });
    }


    //Accordion Box
    if ($('.accordion-box').length) {
        $(".accordion-box").on('click', '.acc-btn', function() {

            var outerBox = $(this).parents('.accordion-box');
            var target = $(this).parents('.accordion');

            if ($(this).hasClass('active') !== true) {
                $(outerBox).find('.accordion .acc-btn').removeClass('active');
            }

            if ($(this).next('.acc-content').is(':visible')) {
                return false;
            } else {
                $(this).addClass('active');
                $(outerBox).children('.accordion').removeClass('active-block');
                $(outerBox).find('.accordion').children('.acc-content').slideUp(300);
                target.addClass('active-block');
                $(this).next('.acc-content').slideDown(300);
            }
        });
    }


    //Tabs Box
    if ($('.tabs-box').length) {
        $('.tabs-box .tab-buttons .tab-btn').on('click', function(e) {
            e.preventDefault();
            var target = $($(this).attr('data-tab'));

            if ($(target).is(':visible')) {
                return false;
            } else {
                target.parents('.tabs-box').find('.tab-buttons').find('.tab-btn').removeClass('active-btn');
                $(this).addClass('active-btn');
                target.parents('.tabs-box').find('.tabs-content').find('.tab').fadeOut(0);
                target.parents('.tabs-box').find('.tabs-content').find('.tab').removeClass('active-tab');
                $(target).fadeIn(300);
                $(target).addClass('active-tab');
            }
        });
    }

    //Custom Seclect Box
    if ($('.custom-select-box').length) {
        $('.custom-select-box').selectmenu().selectmenu('menuWidget').addClass('overflow');
    }

    //LightBox / Fancybox
    if ($('.lightbox-image').length) {
        $('.lightbox-image').fancybox({
            openEffect: 'fade',
            closeEffect: 'fade',
            helpers: {
                media: {}
            }
        });
    }


    //Contact Form Validation
    if ($('#contact-form').length) {
        $('#contact-form').validate({
            rules: {
                username: {
                    required: true
                },
                email: {
                    required: true,
                    email: true
                },
                subject: {
                    required: true
                },
                message: {
                    required: true
                }
            }
        });
    }


    // Scroll to a Specific Div
    if ($('.scroll-to-target').length) {
        $(".scroll-to-target").on('click', function() {
            var target = $(this).attr('data-target');
            // animate
            $('html, body').animate({
                scrollTop: $(target).offset().top
            }, 1000);

        });
    }


    // Elements Animation
    if ($('.wow').length) {
        var wow = new WOW({
            boxClass: 'wow', // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            offset: 0, // distance to the element when triggering the animation (default is 0)
            mobile: false, // trigger animations on mobile devices (default is true)
            live: true // act on asynchronously loaded content (default is true)
        });
        wow.init();
    }

    // bootstrap animated slider
    function bootstrapAnimatedLayer() {

        /* Demo Scripts for Bootstrap Carousel and Animate.css article
         * on SitePoint by Maria Antonietta Perna
         */

        //Function to animate slider captions 
        function doAnimations(elems) {
            //Cache the animationend event in a variable
            var animEndEv = 'webkitAnimationEnd animationend';

            elems.each(function() {
                var $this = $(this),
                    $animationType = $this.data('animation');
                $this.addClass($animationType).one(animEndEv, function() {
                    $this.removeClass($animationType);
                });
            });
        }

        //Variables on page load 
        var $myCarousel = $('#minimal-bootstrap-carousel'),
            $firstAnimatingElems = $myCarousel.find('.item:first').find("[data-animation ^= 'animated']");

        //Initialize carousel 
        $myCarousel.carousel({
            interval: 7000
        });

        //Animate captions in first slide on page load 
        doAnimations($firstAnimatingElems);

        //Pause carousel  
        $myCarousel.carousel('pause');


        //Other slides to be animated on carousel slide event 
        $myCarousel.on('slide.bs.carousel', function(e) {
            var $animatingElems = $(e.relatedTarget).find("[data-animation ^= 'animated']");
            doAnimations($animatingElems);
        });
    }
    bootstrapAnimatedLayer();

    /* ==========================================================================
       DALAL MASTER MOTION & INTERACTION SUITE v4.0
       ========================================================================== */

    // 1. Dynamic Rolling Number Count-Up
    function initRollingCounters() {
        if (!('IntersectionObserver' in window)) return;
        var counters = document.querySelectorAll('.counter-roll:not(.counted)');
        if (!counters.length) return;

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var el = entry.target;
                    el.classList.add('counted');
                    var target = parseFloat(el.getAttribute('data-target')) || 0;
                    var suffix = el.getAttribute('data-suffix') || '';
                    var duration = 1800; // ms
                    var startTime = performance.now();

                    function step(now) {
                        var progress = Math.min((now - startTime) / duration, 1);
                        var easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                        var currentVal = Math.floor(easeProgress * target);
                        el.textContent = currentVal.toLocaleString() + suffix;
                        if (progress < 1) requestAnimationFrame(step);
                    }
                    requestAnimationFrame(step);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.25 });

        counters.forEach(function(c) { observer.observe(c); });
    }

    // 2. Universal Floating WhatsApp Action Button (FAB)
    function initFloatingWhatsApp() {
        if (document.querySelector('.floating-wa-btn')) return;
        var fab = document.createElement('a');
        fab.className = 'floating-wa-btn';
        fab.href = 'https://wa.me/919821232131?text=Hello%20Mr.%20Vinit%20Dalal,%20I%20have%20an%20urgent%20machinery%20requirement.';
        fab.target = '_blank';
        fab.rel = 'noopener noreferrer';
        fab.setAttribute('aria-label', 'Chat with Mr. Vinit Dalal on WhatsApp');
        fab.setAttribute('title', 'Direct WhatsApp with Managing Director (+91 9821232131)');
        fab.innerHTML = '<i class="fa fa-whatsapp"></i>';
        document.body.appendChild(fab);
    }

    // 3. Interactive Image Lightbox Modal
    function initDalalLightbox() {
        // Create modal backdrop if not present
        if (!document.getElementById('dalal-lightbox-modal')) {
            var lb = document.createElement('div');
            lb.id = 'dalal-lightbox-modal';
            lb.className = 'dalal-lightbox-backdrop';
            lb.innerHTML = '<div class="dalal-lightbox-content">' +
                '<button type="button" class="dalal-lightbox-close" aria-label="Close Lightbox">&times;</button>' +
                '<img id="dalal-lightbox-view" src="" alt="Machinery Inspection Fullscreen" style="width:100%; height:auto; max-height:85vh; object-fit:contain; display:block;">' +
                '<div id="dalal-lightbox-caption" style="padding:15px 20px; color:#fff; font-size:14px; font-weight:600; background:#131722;"></div>' +
                '</div>';
            document.body.appendChild(lb);

            var closeBtn = lb.querySelector('.dalal-lightbox-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    lb.classList.remove('is-open');
                });
            }
            lb.addEventListener('click', function(e) {
                if (e.target === lb) lb.classList.remove('is-open');
            });
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') lb.classList.remove('is-open');
            });
        }

        // Delegate click for zoomable images
        document.addEventListener('click', function(e) {
            var target = e.target.closest('.gallery-thumb-box img, [data-lightbox], .pdp-main-img-wrap img');
            if (!target) return;
            var fullSrc = target.getAttribute('data-full') || target.src;
            var caption = target.alt || 'Dalal Machine Tools Inspection View';
            var lb = document.getElementById('dalal-lightbox-modal');
            var img = document.getElementById('dalal-lightbox-view');
            var cap = document.getElementById('dalal-lightbox-caption');
            if (lb && img) {
                img.src = fullSrc;
                if (cap) cap.textContent = caption;
                lb.classList.add('is-open');
            }
        });
    }

    // 4. CFO FAQ Accordion
    function initCfoFaq() {
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('.cfo-faq-btn');
            if (!btn) return;
            var box = btn.closest('.cfo-faq-box');
            if (!box) return;
            var isActive = box.classList.contains('active');
            document.querySelectorAll('.cfo-faq-box').forEach(function(b) { b.classList.remove('active'); });
            if (!isActive) box.classList.add('active');
        });
    }

    // 5. Dual Map Switcher
    function initMapSwitcher() {
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('.map-switch-btn');
            if (!btn) return;
            var targetMap = btn.getAttribute('data-map');
            document.querySelectorAll('.map-switch-btn').forEach(function(b) { b.classList.remove('active'); });
            btn.classList.add('active');

            var iframe = document.getElementById('contact-map-iframe');
            if (!iframe) return;

            if (targetMap === 'pune') {
                // Pune Industrial Machinery Yard Corridor
                iframe.src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d121059.04360341757!2d73.79292671509172!3d18.52461645063469!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bc2bf2e67461101%3A0x828d43bf9d082e33!2sPune%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1700000000000';
            } else {
                // Mumbai Commerce Centre, Tardeo
                iframe.src = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3773.189569722304!2d72.81226027581177!3d18.96720798221379!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7ce6826079965%3A0xbcf03aebf6f6984f!2sCommerce%20Centre%2C%20Tardeo%2C%20Mumbai%2C%20Maharashtra%20400034!5e0!3m2!1sen!2sin!4v1700000000000';
            }
        });
    }

    // 6. Dual-Channel Lead Pipeline (Unified API persistence + WhatsApp notification)
    window.handleUnifiedInquiry = function(formData, targetContainerId) {
        var container = document.getElementById(targetContainerId);
        var submitBtn = container ? container.querySelector('button[type="submit"]') : null;
        var originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Securing Your Machinery Quotation...';
        }

        // Post to backend database
        fetch('/api/inquiries', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
        .then(function(r) { return r.json(); })
        .then(function(res) {
            var refId = (res && res.inquiryId) ? res.inquiryId : ('INQ-' + Date.now().toString().slice(-6));
            
            // Render on-page confirmation toast
            if (container) {
                var toast = document.createElement('div');
                toast.className = 'inquiry-success-toast';
                toast.innerHTML = '<div style="display:flex; align-items:flex-start; gap:14px;">' +
                    '<div style="width:40px; height:40px; border-radius:50%; background:#10b981; color:#fff; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0;">' +
                    '<i class="fa fa-check"></i></div>' +
                    '<div>' +
                    '<h4 style="margin:0 0 6px; font-weight:700; color:#1e293b; font-size:18px;">Quotation Request Registered!</h4>' +
                    '<p style="margin:0 0 8px; font-size:14px; color:#475569; line-height:1.5;">Thank you, <strong>' + (formData.name || 'Valued Client') + '</strong>. Your inquiry for <strong>' + (formData.machineName || formData.machineId || 'Machinery') + '</strong> has been recorded.</p>' +
                    '<span class="inquiry-ref-badge">Inquiry Ref: ' + refId + '</span>' +
                    '<div style="margin-top:14px;">' +
                    '<a href="https://wa.me/919821232131?text=' + encodeURIComponent('Hello Mr. Vinit Dalal, I submitted Inquiry Ref: ' + refId + ' for ' + (formData.machineName || formData.machineId || 'Machinery') + '. Name: ' + formData.name + ', Company: ' + (formData.company || 'N/A')) + '" ' +
                    'target="_blank" class="theme-btn btn-style-one" style="padding:8px 18px; font-size:13px; background:#25D366; border-color:#25D366; color:#fff; font-weight:700; display:inline-flex; align-items:center; gap:6px;">' +
                    '<i class="fa fa-whatsapp"></i> Notify Mr. Vinit Dalal on WhatsApp &rarr;</a>' +
                    '</div>' +
                    '</div></div>';
                
                container.parentNode.insertBefore(toast, container);
                toast.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            // Open WhatsApp window with pre-filled message
            var waMsg = 'Hello Mr. Vinit Dalal,\nInquiry Ref: ' + refId + '\nName: ' + (formData.name || '') + '\nCompany: ' + (formData.company || '') + '\nPhone: ' + (formData.phone || '') + '\nRequirement: ' + (formData.machineName || formData.machineId || '') + '\nDetails: ' + (formData.message || '');
            window.open('https://wa.me/919821232131?text=' + encodeURIComponent(waMsg), '_blank');
        })
        .catch(function() {
            // Offline/direct WhatsApp fallback
            var waMsg = 'Hello Mr. Vinit Dalal,\nName: ' + (formData.name || '') + '\nCompany: ' + (formData.company || '') + '\nRequirement: ' + (formData.machineName || formData.machineId || '') + '\nDetails: ' + (formData.message || '');
            window.open('https://wa.me/919821232131?text=' + encodeURIComponent(waMsg), '_blank');
        })
        .finally(function() {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }
        });
    };

    /* ==========================================================================
       When document is Scrolling, do
       ========================================================================== */

    $(window).on('scroll', function() {
        headerStyle();
    });

    /* ==========================================================================
       When document is loaded, do
       ========================================================================== */

    $(window).on('load', function() {
        handlePreloader();
        enableMasonry();
    });

    // Modern Split Minimalist FAQ Accordion Toggle
    window.toggleDalalSplitFaq = function(btn) {
        var item = btn.closest('.faq-minimal-item');
        if (!item) return;
        var list = item.closest('.faq-minimal-list');
        var isOpen = item.classList.contains('is-open');

        // Close other items in the same list for clean accordion behavior
        if (list) {
            var siblingItems = list.querySelectorAll('.faq-minimal-item');
            siblingItems.forEach(function(el) {
                el.classList.remove('is-open');
                var button = el.querySelector('.faq-minimal-btn');
                if (button) button.setAttribute('aria-expanded', 'false');
            });
        }

        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    };

    function initCfoFaq() {
        // Fallback compatibility
    }

    // Initialize Master Motion Suite on DOM ready
    $(document).ready(function() {
        initRollingCounters();
        initFloatingWhatsApp();
        initDalalLightbox();
        initCfoFaq();
        initMapSwitcher();
    });

})(window.jQuery);
