 var layout = {
   title: {
     text: 'Title',
     font:{
       color: '#ccc',
     },
     yref: "paper",
     y : 1,
     yanchor : "bottom"
   },
   margin: {
     t: 50,
     r: 30,
   },
   paper_bgcolor: '#141617',
   plot_bgcolor: '#141617',
   xaxis: {
     color: '#b3b3b3',
     gridcolor: '#333',
     zerolinecolor: '#333',
     showgrid: false,
     title: 'XLabel',
     hoverformat: '.3f',
     zeroline: false,
   },
   yaxis: {
     color: '#b3b3b3',
     gridcolor: '#333',
     zerolinecolor: '#666',
     title: 'YLabel',
     hoverformat: '.2f',
     // zeroline: false,
   },
   colorway: ['E24A33', '348ABD', '988ED5', '777777', 'FBC15E', '8EBA42', 'FFB5B8'],
   hoverlabel:{
     namelength: 3,
   },
   legend: {
     orientation: "h",
     font: {
      color: '#aaa'
    },
   },

 };
 var config = {
   modeBarButtonsToRemove: ['zoomIn2d', 'zoomOut2d', 'autoScale2d', 'toggleSpikelines', 'toggleHover'],
   displaylogo: false
 };
 var annotation = {
   xref: 'x',
   yref: 'y',
   showarrow: false,
   font: {
     family: 'Courier New, monospace',
     size: 16,
     color: '#ccc'
   },
   align: 'center',
   borderpad: 4,
   // bgcolor: '#1a1c1d',
   opacity: 1
};
