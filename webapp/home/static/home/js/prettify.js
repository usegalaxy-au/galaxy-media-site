// Prettify JSON fields

window.onload = () => {
  el = document.getElementById('id_address')
  el.value = JSON.stringify(JSON.parse(el.value), null, 4)
  el.setAttribute('style', 'font-family: monospace;')
}
