let reference_unit = document.getElementById('hx_reference_unit')
let offset = document.getElementById('hx_offset')
let offset_estimation = document.getElementById('offset_estimation')
var var_offset
var var_reference_unit

function get_hx_data(){
  get_api("/offset").then(val => {var_offset = val; offset.innerHTML = val});
  get_api("/reference_unit").then(val => {var_reference_unit = val; reference_unit.innerHTML = val});
}

function replace_html(obj, str){
  obj.innerHTML = str;
}

function estimate_offset(){
  replace_html(offset_estimation, "Estimating...");
  get_api("/estimate_offset")
  .then(val => {
    var_offset = val;
    offset_estimation.innerHTML = val;
  });
}

function estimate_reference_unit(){
  const val_known_force = Math.round(document.getElementById('known_force').value);
  if(!val_known_force){
    window.alert("Insert known force value");
    return;
  }
  reference_unit_estimation.innerHTML = "Estimating...";
  get_api("/estimate_reference_unit/" + val_known_force)
  .then(val => {
      var_reference_unit = val;
      reference_unit_estimation.innerHTML = val;
    });
}

function save_config(){
  if(var_offset && var_reference_unit){
    get_api("/save_hx_config/" + var_offset + "/" + var_reference_unit)
    .then(val => {
        document.getElementById('saved').innerHTML = val;
      });
  }
  else{
    window.alert("Offset or Reference Unit missing. Please redo the calibration")
  }
}

get_hx_data();
