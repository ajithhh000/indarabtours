import re
import sys
from pathlib import Path

HOME_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">'''

STANDARD_NAV = '''<nav id="navbar" class="fixed top-0 left-0 right-0 z-50 bg-white transition-shadow duration-300">
    <div class="container-main flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16 md:h-20">
      <!-- Logo -->
      <a href="../" class="flex items-center gap-2.5 flex-shrink-0" aria-label="IND ARAB TOURS AND TRAVELS Home">
        <img src="../public/logo-mark.png" alt="IND ARAB TOURS AND TRAVELS logo" width="40" height="40" class="h-10 w-auto">
        <span class="font-heading text-lg text-primary font-bold leading-tight hidden sm:inline">IND ARAB TOURS AND TRAVELS</span>
      </a>

      <!-- Desktop Nav Links -->
      <ul class="hidden md:flex items-center gap-1 font-cta text-sm font-semibold uppercase tracking-wide">
            <li><a href="../" class="px-3 py-2 text-text-secondary hover:text-primary border-b-2 border-transparent transition-colors duration-200">Home</a></li>
            <li><a href="../destinations/" class="px-3 py-2 text-text-secondary hover:text-primary border-b-2 border-transparent transition-colors duration-200">Destinations</a></li>
            <li><a href="../resources/" class="px-3 py-2 text-text-secondary hover:text-primary border-b-2 border-transparent transition-colors duration-200">Resources</a></li>
            <li><a href="../about/" class="px-3 py-2 text-primary border-b-2 border-primary transition-colors duration-200">About</a></li>
            <li><a href="../contact/" class="px-3 py-2 text-text-secondary hover:text-primary border-b-2 border-transparent transition-colors duration-200">Contact</a></li>
      </ul>

      <!-- Mobile Hamburger -->
      <button id="mobile-menu-btn" class="md:hidden flex items-center justify-center w-10 h-10 rounded-lg hover:bg-surface transition-colors" aria-label="Toggle navigation menu" aria-expanded="false">
        <svg id="hamburger-icon" class="w-6 h-6 text-primary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
        <svg id="close-icon" class="w-6 h-6 text-primary hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div id="mobile-menu" class="md:hidden hidden bg-white border-t border-gray-100 shadow-lg">
      <ul class="flex flex-col font-cta text-sm font-semibold uppercase tracking-wide">
            <li><a href="../" class="block px-6 py-3.5 text-text-secondary hover:bg-surface hover:text-primary border-l-4 border-transparent transition-colors">Home</a></li>
            <li><a href="../destinations/" class="block px-6 py-3.5 text-text-secondary hover:bg-surface hover:text-primary border-l-4 border-transparent transition-colors">Destinations</a></li>
            <li><a href="../resources/" class="block px-6 py-3.5 text-text-secondary hover:bg-surface hover:text-primary border-l-4 border-transparent transition-colors">Resources</a></li>
            <li><a href="../about/" class="block px-6 py-3.5 text-primary bg-surface/50 border-l-4 border-primary">About</a></li>
            <li><a href="../contact/" class="block px-6 py-3.5 text-text-secondary hover:bg-surface hover:text-primary border-l-4 border-transparent transition-colors">Contact</a></li>
      </ul>
    </div>
  </nav>'''

STANDARD_FOOTER = '''<footer class="bg-primary text-white">
    <div class="container-main pt-16 pb-8 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 lg:gap-8">

        <!-- Column 1: Logo & About -->
        <div class="sm:col-span-2 lg:col-span-1">
          <a href="../" class="flex items-center gap-2.5 mb-4" aria-label="IND ARAB TOURS AND TRAVELS Home">
            <img src="../public/logo-mark.png" alt="IND ARAB TOURS AND TRAVELS logo" width="40" height="40" class="h-10 w-auto">
            <span class="font-heading text-white font-bold text-base leading-tight">IND ARAB TOURS AND TRAVELS</span>
          </a>
          <p class="text-white/70 text-sm leading-relaxed">
            Your trusted travel partner in Sharjah, crafting unforgettable international journeys from the UAE.
          </p>
          <!-- Social Icons -->
          <div class="flex items-center gap-3 mt-5">
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors" aria-label="Instagram">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
            </a>
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors" aria-label="Facebook">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
            <a href="https://x.com" target="_blank" rel="noopener noreferrer" class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors" aria-label="X (formerly Twitter)">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
          </div>
        </div>

        <!-- Column 2: Quick Links -->
        <div>
          <h4 class="font-cta font-bold text-sm uppercase tracking-wider text-accent mb-4">Quick Links</h4>
          <ul class="space-y-2.5 text-sm">
            <li><a href="../" class="text-white/80 hover:text-white transition-colors">Home</a></li>
            <li><a href="../about/" class="text-white/80 hover:text-white transition-colors">About</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Destinations</a></li>
            <li><a href="../contact/" class="text-white/80 hover:text-white transition-colors">Contact</a></li>
            <li><a href="../resources/" class="text-white/80 hover:text-white transition-colors">Resources</a></li>
          </ul>
        </div>

        <!-- Column 3: Destinations -->
        <div>
          <h4 class="font-cta font-bold text-sm uppercase tracking-wider text-accent mb-4">Destinations</h4>
          <ul class="space-y-2.5 text-sm">
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Turkey</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Egypt</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Georgia</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Jordan</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">Morocco</a></li>
            <li><a href="../destinations/" class="text-white/80 hover:text-white transition-colors">India</a></li>
          </ul>
        </div>

        <!-- Column 4: Contact Info -->
        <div>
          <h4 class="font-cta font-bold text-sm uppercase tracking-wider text-accent mb-4">Contact Us</h4>
          <ul class="space-y-3 text-sm text-white/80">
            <li class="flex gap-2.5">
              <svg class="w-5 h-5 flex-shrink-0 text-accent mt-0.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>
              </svg>
              <span>Sharjah Research Technology and Innovation Park Free Zone Authority, BLOCK B-B52-091, SHARJAH, UAE</span>
            </li>
            <li class="flex items-center gap-2.5">
              <svg class="w-5 h-5 flex-shrink-0 text-accent" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/>
              </svg>
              <a href="tel:+971502161719" class="hover:text-white transition-colors">+971-50 2161 719</a>
            </li>
            <li class="flex items-center gap-2.5">
              <svg class="w-5 h-5 flex-shrink-0 text-accent" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/>
              </svg>
              <a href="mailto:info.indarabtours@gmail.com" class="hover:text-white transition-colors">info.indarabtours@gmail.com</a>
            </li>
          </ul>
        </div>

      </div>

      <!-- Copyright -->
      <div class="border-t border-white/10 mt-10 pt-6 text-center">
        <p class="text-white/50 text-sm">&copy; <span id="footer-year"></span> IND ARAB TOURS AND TRAVELS. All rights reserved.</p>
      </div>
    </div>
  </footer>'''

STANDARD_FLOATING_BTN = '''<a
    href="mailto:info.indarabtours@gmail.com?subject=General%20Enquiry&body=Hello%2C%20I%27d%20like%20to%20know%20more%20about%20your%20tour%20packages."
    class="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-accent flex items-center justify-center shadow-lg hover:scale-110 hover:shadow-xl transition-all duration-200"
    aria-label="Send us an email"
  >
    <svg class="w-6 h-6" fill="none" stroke="white" stroke-width="1.8" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/>
    </svg>
  </a>'''

STANDARD_SCRIPTS = '''<script>
    /* -- Navbar scroll shadow -- */
    (function () {
      var navbar = document.getElementById('navbar');
      window.addEventListener('scroll', function () {
        if (window.scrollY > 10) { navbar.classList.add('shadow-md'); }
        else { navbar.classList.remove('shadow-md'); }
      }, { passive: true });
    })();

    /* -- Mobile menu toggle -- */
    (function () {
      var btn = document.getElementById('mobile-menu-btn');
      var menu = document.getElementById('mobile-menu');
      var hamburgerIcon = document.getElementById('hamburger-icon');
      var closeIcon = document.getElementById('close-icon');
      var menuOpen = false;
      btn.addEventListener('click', function () {
        menuOpen = !menuOpen;
        menu.classList.toggle('hidden', !menuOpen);
        hamburgerIcon.classList.toggle('hidden', menuOpen);
        closeIcon.classList.toggle('hidden', !menuOpen);
        btn.setAttribute('aria-expanded', menuOpen ? 'true' : 'false');
      });
    })();

    /* -- Footer year -- */
    (function () {
      var el = document.getElementById('footer-year');
      if (el) el.textContent = new Date().getFullYear();
    })();
  </script>'''

CHEVRON = '<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>'

def make_hero(title, subtitle, bg_image):
    return f'''<section class="page-hero" aria-label="Page banner">
      <img src="{bg_image}" alt="" class="page-hero-bg" fetchpriority="high">
      <div class="page-hero-overlay"></div>
      <div class="page-hero-content">
        <nav aria-label="Breadcrumb" class="breadcrumb">
          <ol class="flex items-center justify-center gap-2">
            <li><a href="../">Home</a></li>
            <li aria-hidden="true">{CHEVRON}</li>
            <li class="text-white font-medium" aria-current="page">{title}</li>
          </ol>
        </nav>
        <h1 class="page-hero-title">{title}</h1>
        <p class="page-hero-subtitle">{subtitle}</p>
      </div>
    </section>'''

def standardize_subpage(path, page_title, page_subtitle, bg_image, active_nav):
    text = Path(path).read_text(encoding='utf-8')

    # Replace Google Fonts
    text = re.sub(
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet">',
        HOME_FONTS,
        text,
        count=1,
        flags=re.DOTALL
    )

    # Replace navbar
    text = re.sub(
        r'<nav id="navbar"[\s\S]*?</nav>',
        STANDARD_NAV,
        text,
        count=1
    )

    # Replace header/hero page header block
    text = re.sub(
        r'<header[\s\S]*?</header>',
        make_hero(page_title, page_subtitle, bg_image),
        text,
        count=1
    )

    # Replace footer
    text = re.sub(
        r'<footer[\s\S]*?</footer>',
        STANDARD_FOOTER,
        text,
        count=1
    )

    # Replace floating email button
    text = re.sub(
        r'<a\s+href="mailto:[^"]+"[\s\S]*?</a>',
        STANDARD_FLOATING_BTN,
        text,
        count=1
    )

    # Replace scripts block before </body>
    text = re.sub(
        r'<script>[\s\S]*?</script>\s*</body>',
        STANDARD_SCRIPTS + '\n</body>',
        text,
        count=1
    )

    # Replace max-w-7xl containers with container-main
    # Handle variations of max-w-7xl mx-auto px-4 sm:px-6 lg:px-8
    text = re.sub(
        r'class="([^"]*)max-w-7xl mx-auto px-4 sm:px-6 lg:px-8([^"]*)"',
        r'class="\1container-main\2"',
        text
    )

    Path(path).write_text(text, encoding='utf-8')
    print(f"Updated {path}")

if __name__ == '__main__':
    base = Path('/mnt/c/Users/ajith/Downloads/indarabtours (3)/indarabtours')
    standardize_subpage(
        base / 'about/index.html',
        'About Us',
        'Your trusted partner for international travel from the UAE',
        'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1600&h=900&fit=crop',
        'about'
    )
