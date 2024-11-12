function Guardar() {
    let nombreProducto = document.getElementById("nombre_producto").value;
    if (nombreProducto == "") {
        alert("Nombre del producto no ingresado");
        return false;
    }

    let descripcion = document.getElementById("descripcion").value;
    if (descripcion == "") {
        alert("Descripción no ingresada");
        return false;
    }

    let precio = document.getElementById("precio").value;
    if (precio == "") {
        alert("Precio no ingresado");
        return false;
    }
    if (isNaN(precio) || parseFloat(precio) <= 0) {
        alert("Precio debe ser un número positivo");
        return false;
    }

    let stock = document.getElementById("stock").value;
    if (stock == "") {
        alert("Stock no ingresado");
        return false;
    }
    if (isNaN(stock) || parseInt(stock) < 0) {
        alert("Stock debe ser un número no negativo");
        return false;
    }

    let imagen = document.getElementById("imagen").value;
    if (imagen == "") {
        alert("Imagen no ingresada");
        return false;
    }

    let categoria = document.getElementById("categoria").value;
    if (categoria == "") {
        alert("Categoría no seleccionada");
        return false;
    }

    let administrador = document.getElementById("administrador").value;
    if (administrador == "") {
        alert("Administrador no seleccionado");
        return false;
    }

    // Si todos los campos son válidos
    return true;
}
