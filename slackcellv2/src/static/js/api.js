async function get_api(cmd) {
  const response = await fetch(cmd);
  return await response.text();
}
function get_api_sync(cmd) {
  const response =  fetch(cmd);
  return  response.text();
}
