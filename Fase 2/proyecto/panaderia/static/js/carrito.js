function agregarAlCarrito(productoId) {
    fetch(`/agregar_al_carrito/${productoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',  // Token CSRF para seguridad
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensaje) {
            actualizarCarrito(data.carrito);
        }
    });
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(productoId) {
    fetch(`/eliminar_del_carrito/${productoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensaje) {
            actualizarCarrito(data.carrito);
        }
    });
}

// Función para actualizar el contenido del carrito en la interfaz
function actualizarCarrito(carrito) {
    let carritoContainer = document.getElementById('carrito-container');
    carritoContainer.innerHTML = '';  // Limpia el carrito actual

    // Recorre los productos en el carrito y agrégalos al HTML
    carrito.forEach(item => {
        let productoHTML = `<div>
                                <span>${item.nombre} (${item.cantidad})</span>
                                <span>$${item.precio}</span>
                                <button onclick="eliminarDelCarrito(${item.id})">Eliminar</button>
                            </div>`;
        carritoContainer.innerHTML += productoHTML;
    });

    // Actualiza el total del carrito
    document.getElementById('total').innerText = `$${carrito.total}`;
}