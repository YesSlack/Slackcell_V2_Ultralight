function plot(x, y, time_range_s = 10, show_all = false){
  let time_range = Math.floor(time_range_s * update_rate);
  let _n = x.length;
  let x_range = [0, time_range_s];
  let y_range = [Math.min(...y), Math.max(...y)];

  if (_n < time_range){
    // set x range
    x_range = [0, time_range_s]
    //y_range = [y[n - time_range], y[n - 1]]
  }
  else{
    x_range = [x[_n - time_range], x[_n - 1]];

    if (!show_all){
      //only plot the
      // needed data on live plot
      x = x.slice(_n - time_range)
      y = y.slice(_n - time_range)
    }
  }
  var force = {
    x: x,
    y: y,
    mode: 'lines',
    name: 'Force',
    hovertemplate: '%{y:.2f} kN<extra></extra>'
  };
  var layout_ts = {...layout};
  layout_ts['title']['text'] = 'Live SlackCell Data';
  layout_ts['xaxis']['title'] = 'Time [s]';
  layout_ts['yaxis']['title'] = 'Force [kN]';
  layout_ts['xaxis']['range'] = x_range;
  layout_ts['yaxis']['range'] = y_range;
    //layout_ts['yaxis']['range'] = y_range;
  plot_data_ts = [force] //[force, lin_reg]
  Plotly.newPlot('chart', plot_data_ts, layout_ts, config);
}



function change_update_plot(){
  if (update_plot){
    clearInterval(interval_force_plot);
    document.getElementById('update_plot').checked = false
    update_plot = false
    plot(timestamp, force, 10, true)
  }else{
    setInterval(interval_force_plot, storage_time);
    n = timestamp.length
    interval_force_plot = setInterval(function() {plot(timestamp, force)}, 33);
    document.getElementById('update_plot').checked = true
    update_plot = true
  }
}
var update_plot = false;
var interval_force_plot;
change_update_plot();
