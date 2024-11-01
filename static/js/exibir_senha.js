function exibir_senha() {
    if(senha.getAttribute("type")== "password"){
    senha.setAttribute("type","text")
    olho.setAttribute("class", "fa-solid fa-eye-slash")
    }else{
        senha.setAttribute("type","password")

        olho.setAttribute("class", "fa-solid fa-eye")
    }
}

olho.addEventListener("click", exibir_senha)

