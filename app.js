document.addEventListener("DOMContentLoaded", function () {
  // Initialize Yahoo OAuth variables
  const clientId = "YOUR_YAHOO_CLIENT_ID";
  const redirectUri = "https://yourusername.github.io/FantasyVegaMetrics/";
  const authUrl = `https://api.login.yahoo.com/oauth2/request_auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=fantasy-sports`;

  // Check for authorization code in URL
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");

  if (code) {
    // TODO: Exchange the code for an access token
    // For a public client, you will make an AJAX request directly to Yahoo or to your server if you have one.
  }

  // Setup event listener for the "Authorize" button
  document.getElementById("authorize").addEventListener("click", function () {
    window.location.href = authUrl;
  });
});
