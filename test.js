const GAME_BASE_URL = "localhost";

function connect(user) {
  window.alert(user);
}
var userinput = document.getElementById("userinput");
userinput.addEventListener("keydown", function (e) {
  if (e.code === "Enter") {
    //checks whether the pressed key is "Enter"
    connect(e.target.value);
  }
});

sockconnect()