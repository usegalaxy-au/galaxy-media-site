// Scroll to an element with a custom offset when clicking on anchor links with
// hash navigation. This prevents the browser from scrolling past the target
// element.

const OFFSET = -120; // Custom offset (in px)

function scrollToElementWithOffset(elementId) {
  const targetElement = document.getElementById(elementId);

  if (targetElement) {
    const elementPosition =
      targetElement.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({
      top: elementPosition + OFFSET,
      behavior: "smooth", // Smooth scroll effect
    });
  }
}

// Handle clicks on anchor links with hash navigation
document.querySelectorAll("a").forEach((link) => {
  if (link.getAttribute("href").startsWith("#")) {
    link.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default anchor scroll
      const targetId = this.getAttribute("href").substring(1); // Get the target ID
      scrollToElementWithOffset(targetId); // Scroll with custom behavior
    });
  }
});

// Handle URL hash change (for direct navigation to #elementId)
window.addEventListener("hashchange", function () {
  const hash = window.location.hash.substring(1); // Get the current hash (without the #)
  scrollToElementWithOffset(hash); // Scroll with custom behavior
});

// Scroll on page load if the URL contains a hash
window.addEventListener("load", function () {
  const hash = window.location.hash.substring(1); // Get the current hash (without the #)
  if (hash) {
    scrollToElementWithOffset(hash); // Scroll with custom behavior
  }
});
