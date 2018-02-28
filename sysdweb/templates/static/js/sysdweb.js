/*
 * sysdweb.js
 * Copyright (C) 2016-2018 Óscar García Amor <ogarcia@connectical.com>
 *
 * Distributed under terms of the GNU GPLv3 license.
 */

function unit(service, action) {
  var url = '/api/v1/' + service + '/' + action;

  $.getJSON( url, function( data ) {
    $.each( data, function( key, val ) {
      if (val == 'OK') {
        $('#services').load(document.URL + ' #services');
        var timerId = setInterval(function(){
          $('#services').load(document.URL + ' #services');
        }, 1000);
        setTimeout(function(){clearInterval(timerId);}, 10000);
      } else {
          $('#warningModal').modal('show')
      }
    });
  });
}

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
  setInterval(function() {
    $('#services').load(document.URL + ' #services', function() {
      $('[data-toggle="tooltip"]').tooltip();
    });
  }, 20000);
});
