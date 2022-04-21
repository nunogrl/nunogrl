      function display_gpx(elt) {
        if (!elt) return;

        var url = elt.getAttribute('data-gpx-source');
        var mapid = elt.getAttribute('data-map-target');
        if (!url || !mapid) return;

        function _t(t) { return elt.getElementsByTagName(t)[0]; }
        function _c(c) { return elt.getElementsByClassName(c)[0]; }

        var map = L.map(mapid);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: 'Map data &copy; <a href="http://www.osm.org">OpenStreetMap</a>'
        }).addTo(map);

        var control = L.control.layers(null, null).addTo(map);

        new L.GPX(url, {
          async: true,
          marker_options: {
            startIconUrl: 'pin-icon-start.png',
            endIconUrl:   'pin-icon-end.png',
            shadowUrl:    'pin-shadow.png',
          },
        }).on('loaded', function(e) {
          var gpx = e.target;
          map.fitBounds(gpx.getBounds());
          control.addOverlay(gpx, gpx.get_name());

          /*
           * Note: the code below relies on the fact that the demo GPX file is
           * an actual GPS track with timing and heartrate information.
           */
          _t('h3').textContent = gpx.get_name();
          _c('start').textContent = gpx.get_start_time().toDateString() + ', '
            + gpx.get_start_time().toLocaleTimeString();
          _c('distance').textContent = gpx.get_distance().toFixed();
          _c('duration').textContent = gpx.get_duration_string(gpx.get_moving_time());
          _c('pace').textContent     = gpx.get_duration_string(gpx.get_moving_pace_imp(), true);
          _c('avghr').textContent    = gpx.get_average_hr();
          _c('elevation-gain').textContent = gpx.to(gpx.get_elevation_gain()).toFixed(0);
          _c('elevation-loss').textContent = gpx.to(gpx.get_elevation_loss()).toFixed(0);
          _c('elevation-net').textContent  = gpx.to(gpx.get_elevation_gain()
            - gpx.get_elevation_loss()).toFixed(0);
        }).addTo(map);
      }

      display_gpx(document.getElementById('demo'));

