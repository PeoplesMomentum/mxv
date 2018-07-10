<script type="text/javascript">
  
  // only allow elements with an Id in this array to be set via URL parameters
  var whiteListedIds = ["donation_first_name", "donation_last_name"];
  
  $(document).ready(function()
  {
    // for each URL parameter...
    var params = window.location.href.split('?')[1].split('&');
    for(var i = 0; i < params.length; i++)
    {
      // split into id/value
      var param = params[i].split('=');
      
      // if the id is whitelisted...
      if(whiteListedIds.indexOf(param[0]) > -1)
      {
        // set the element's value
        document.getElementById(param[0]).value = decodeURIComponent(param[1]);
      }
    }
  });
  
</script>