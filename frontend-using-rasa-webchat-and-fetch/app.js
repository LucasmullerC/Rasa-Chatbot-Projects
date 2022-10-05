const listaNomes = document.getElementById("toptext");
let pessoas = [];

function enviar(){
    const form = document.getElementById('form');

    form.addEventListener("submit", function(event){
      event.preventDefault(); // prevents form from submitting
    })

    var x = document.getElementById("ftext");
    msg = {
        sender:"Você",
        text: x.value
    }
    pessoas.push(msg)

    var xhr = new XMLHttpRequest();
    var url = "http://localhost:5005/webhooks/rest/webhook";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log("Sucesso")
            json.forEach(endmsg => {
                msgbot = {
                    sender:"BOT",
                    text: endmsg.text,
                    image: endmsg.image
                }
                pessoas.push(msgbot)
            });
            criarListaPessoas()
        }
        else{
            console.log("erro")
        }
    };
    var data = JSON.stringify({"sender": "user", "message": x.value});
    xhr.send(data);
}

function criarListaPessoas() {
    listaNomes.innerHTML = "";
    pessoas.forEach(pessoa => {
      const newLi = document.createElement("li");
      let newText = "";
      if(pessoa.text == undefined){
        newText = new Image(200, 150);
        newText.src = pessoa.image;
      }
      else{
        newText = document.createTextNode(`${pessoa.sender} - ${pessoa.text}`);
      }
      newLi.appendChild(newText);
      listaNomes.appendChild(newLi);
    });
  }
