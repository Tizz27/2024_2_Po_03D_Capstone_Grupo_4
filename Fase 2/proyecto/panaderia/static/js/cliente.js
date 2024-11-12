function validarFormulario() {
    let nombreCompleto = document.getElementById("id_nombre_completo").value;
    let fechaNacimiento = document.getElementById("id_fecha_nacimiento").value;
    let email = document.getElementById("id_email").value;
    let contraseña = document.getElementById("id_contraseña").value;
    let direccion = document.getElementById("id_direccion").value;
    let rut = document.getElementById("id_rut").value;

    if (nombreCompleto === "") {
        alert("Nombre completo no ingresado");
        return false;
    }

    if (fechaNacimiento === "") {
        alert("Fecha de nacimiento no ingresada");
        return false;
    }

    if (email === "") {
        alert("Correo electrónico no ingresado");
        return false;
    }

    if (contraseña === "") {
        alert("Contraseña no ingresada");
        return false;
    }

    if (rut === "") {
        alert("RUT no ingresado");
        return false;
    }

    return true; // Si todos los campos son válidos
}