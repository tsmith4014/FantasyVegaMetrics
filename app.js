document.addEventListener("DOMContentLoaded", function () {
  const clientId = "YOUR_YAHOO_CLIENT_ID";
  const redirectUri =
    "https://tsmith4014.github.io/FantasyVegaMetrics/oauth.html"; // Redirect to your OAuth page
  const authUrl = `https://api.login.yahoo.com/oauth2/request_auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=fantasy-sports`;

  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");

  if (code) {
    // TODO: Implement code for access token exchange
  }

  document.getElementById("authorize").addEventListener("click", function () {
    window.location.href = authUrl;
  });
});
