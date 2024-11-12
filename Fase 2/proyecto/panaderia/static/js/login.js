function validarFormularioLogin() {
    var username = document.getElementById("id_username").value;
    var password = document.getElementById("id_password").value;

    if (username == "" || password == "") {
        alert("Por favor, complete todos los campos.");
        return false;
    }
    return true;
}