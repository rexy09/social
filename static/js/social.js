document.addEventListener('emoji-click', event => {
    document.getElementById('message-input').value += event.detail.emoji.unicode;
    //  console.log(event.detail.emoji);
    //  console.log(event.detail);   
});

function mytoggle() {
    var x = document.getElementById("emoji-picker");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}