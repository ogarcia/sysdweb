/*
 * sysdweb.js
 * Copyright (C) 2016 Óscar García Amor <ogarcia@connectical.com>
 *
 * Distributed under terms of the GNU GPLv3 license.
 */

$(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
});

function unit(service, action) {
  var url = '/api/v1/' + service + '/' + action;

  $.get( url, function( data ) {
    $('#services').load(document.URL + ' #services');
    var timerId = setInterval(function(){
      $('#services').load(document.URL + ' #services');
    }, 1000);
    setTimeout(function(){
      clearInterval(timerId);
    }, 10000);
  });
}

$(document).ready(function(){
  setInterval(function() {
    $('#services').load(document.URL + ' #services');
  }, 20000);
});
