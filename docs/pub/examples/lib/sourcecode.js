// display source with syntax highlighting (prism), hidden until "source" is clicked

// NOTE: the example CSS that hid .code was removed when libs moved to unpkg,
// so inject the show/hide rules here to keep the sketch visible by default
$('<style>').text(`
.code {
  display: none;
  position: absolute;
  top: 0;
  background-color: white;
  width: 98%;
  min-height: 100vh;
  z-index: 10;
}
.code:target { display: block !important; }
.code.hidden { display: none !important; }
.code a {
  float: left;
  display: block;
  margin-top: 8px;
  font-size: 16px;
}
.code pre {
  position: static !important;
  background: none !important;
  box-shadow: none !important;
  background-image: none !important;
  border: none !important;
  max-height: none !important;
  margin: 2rem 0 0 1rem !important;
  padding: 10px !important;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 14px;
}
/* kill the prism-coy "curled paper" shadows */
.code pre::before,
.code pre::after {
  content: none !important;
  box-shadow: none !important;
  transform: none !important;
}
`).appendTo('head');

function getCode(url, id) {
  $.ajax({
    url: url,
    dataType: "text",
    success: function (data) {
      var encoded = data.replace(/[\u00A0-\u9999<>\&]/gim, function (i) {
        return '&#' + i.charCodeAt(0) + ';';
      });
      $(id).html(encoded);
      if ($(id).length > 0) Prism.highlightElement($(id)[0]);
    }
  });
}

// add a "close" link inside each source pane to hide it again
function addCloseLinks() {
  $('.code').prepend('<a href="#" class="close-code">close</a>');
  $('.close-code').on('click', function (e) {
    e.preventDefault();
    $('.code').removeClass('hidden');
    // clear the fragment so :target no longer matches (CSS hides the pane)
    try {
      history.replaceState(null, '', window.location.pathname + window.location.search);
    } catch (err) {
      window.location.hash = 'none'; // nonexistent id, so nothing is targeted
    }
    // if the hash didn't change (e.g. already cleared), force-hide via class
    $('.code:target').addClass('hidden');
  });
  // when navigating to a source link, clear any forced-hide state
  $(window).on('hashchange', function () {
    $('.code').removeClass('hidden');
  });
}

$(() => {
  getCode("code.js", "#source-code");
  if ($('#grammar').length) getCode("../../data/haiku.json", "#grammar");
  addCloseLinks();
});  
