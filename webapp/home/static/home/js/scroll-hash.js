// Scroll to an element with a custom offset when clicking on anchor links with
// hash navigation. This prevents the browser from scrolling past the target
// element.

const OFFSET = -120; // Set offset from scroll target (px)

function scrollToElementWithOffset(elementId) {
  const targetElement = document.getElementById(elementId);

  if (targetElement) {
    const elementPosition =
      targetElement.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({
      top: elementPosition + OFFSET,
      behavior: "smooth",
    });
  }
}

// Handle clicks on anchor links with hash navigation
document.querySelectorAll("a").forEach((link) => {
  if (link.getAttribute("href").startsWith("#")) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      const targetId = this.getAttribute("href").substring(1);
      scrollToElementWithOffset(targetId);
      window.location.hash = targetId;
    });
  }
});

// Handle URL hash change (for direct navigation to #elementId)
window.addEventListener("hashchange", function () {
  const hash = window.location.hash.substring(1);
  scrollToElementWithOffset(hash);
});

// Scroll on page load if the URL contains a hash
window.addEventListener("load", function () {
  const hash = window.location.hash.substring(1);
  if (hash) {
    scrollToElementWithOffset(hash);
  }
});
