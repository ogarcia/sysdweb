/*
 * sysdweb.js
 * Copyright (C) 2016-2025 Óscar García Amor <ogarcia@connectical.com>
 *
 * Distributed under terms of the GNU GPLv3 license.
 */

const warningModal = new bootstrap.Modal('#warningModal', {})
var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
var tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

function reload(element) {
  fetch(document.URL)
    .then(res => res.text())
    .then(text => {
      const parser = new DOMParser();
      const htmlDocument = parser.parseFromString(text, 'text/html');
      const section = htmlDocument.documentElement.querySelector(element);
      document.querySelector(element).replaceWith(section);
      tooltipList.forEach((tooltip) => {tooltip.dispose()});
      tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
      tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  });
}

function unit(service, action) {
  var url = '/api/v1/' + service + '/' + action;
  fetch(url).then(res => res.json()).then(function (res) {
    for (key in res) {
      if (res[key] === 'OK') {
        reload('#services');
        var timerId = setInterval(function(){
          reload('#services');
        }, 1000);
        setTimeout(function(){clearInterval(timerId);}, 10000);
      } else {
        warningModal.show();
      }
    }
  });
}

setInterval(function() {
  reload('#services');
}, 20000);
