// Se inicializa el carrito global
let carritoGlobal = []; 

const cambiarVista = (vista) => {
    // Se oculta la vista actual
    document.getElementById('vista-menu').classList.add('oculto');
    document.getElementById('vista-cart').classList.add('oculto');
    document.getElementById('btn-menu').classList.remove('activo');
    document.getElementById('btn-cart').classList.remove('activo');

    // Se muestra la vista seleccionada
    document.getElementById(`vista-${vista}`).classList.remove('oculto');
    document.getElementById(`btn-${vista}`).classList.add('activo');
};

const cargarProductos = async () => {
    try {
        // Se obtiene la lista desde la API
        const res = await fetch('/productos');
        const productos = await res.json();
        const grilla = document.getElementById('grilla-productos');
        grilla.innerHTML = '';
        
        // Se genera la card para cada producto
        productos.forEach(prod => {
            grilla.innerHTML += `
                <div class="card">
                    <img src="/static/img/${prod.imagen}" alt="${prod.nombre}">
                    <div class="card-info">
                        <h3>${prod.nombre}</h3>
                        <p class="precio">$${prod.precio.toLocaleString('es-AR')}</p>
                        <button class="btn-add" onclick="agregarAlCarrito(${prod.id})">Añadir al carrito</button>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error al cargar productos:", error);
    }
};

const cargarCarrito = async () => {
    try {
        // Se solicita el estado actual del carrito
        const res = await fetch('/carrito/total');
        const data = await res.json();
        carritoGlobal = data.carrito;
        
        // Se actualiza el total en la interfaz
        const totalFormateado = data.total.toLocaleString('es-AR');
        document.getElementById('total-flotante').innerText = totalFormateado;
        document.getElementById('total-cart-page').innerText = totalFormateado;
        document.getElementById('cart-count').innerText = data.carrito.length;
        
        // Se agrupa el contenido por nombre de producto
        let agrupado = {};
        data.carrito.forEach(item => {
            if (!agrupado[item.nombre]) {
                agrupado[item.nombre] = { ...item, cantidad: 0, ids: [] };
            }
            agrupado[item.nombre].cantidad++;
            agrupado[item.nombre].ids.push(item.id_carrito);
        });

        const lista = document.getElementById('lista-carrito');
        lista.innerHTML = '';
        
        // Se renderiza cada fila en la tabla del carrito
        Object.values(agrupado).forEach(item => {
            let subtotal = item.precio * item.cantidad;
            let idParaEliminar = item.ids[item.ids.length - 1]; 
            
            lista.innerHTML += `
                <tr>
                    <td>${item.nombre}</td>
                    <td>
                        <button class="btn-accion" onclick="eliminarDelCarrito(${idParaEliminar})">-</button>
                        ${item.cantidad}
                        <button class="btn-accion" onclick="agregarAlCarritoPorNombre('${item.nombre}')">+</button>
                    </td>
                    <td>
                        $${subtotal.toLocaleString('es-AR')} 
                        <button class="btn-remove" onclick="eliminarTodosDelCarrito('${item.nombre}')" title="Quitar todos">x</button>
                    </td>
                </tr>
            `;
        });
    } catch (error) {
        console.error("Error al cargar el carrito:", error);
    }
};

const agregarAlCarrito = async (id) => {
    // Se envía el producto al servidor
    await fetch(`/carrito/${id}`, { method: 'POST' });
    cargarCarrito();
};

const agregarAlCarritoPorNombre = async (nombre) => {
    // Se busca el ID correspondiente para incrementar cantidad
    const item = carritoGlobal.find(i => i.nombre === nombre);
    if(item) {
        const res = await fetch('/productos');
        const productos = await res.json();
        const prodId = productos.find(p => p.nombre === nombre).id;
        await fetch(`/carrito/${prodId}`, { method: 'POST' });
        cargarCarrito();
    }
};

const eliminarDelCarrito = async (id_carrito) => {
    // Se solicita la eliminación de una unidad
    await fetch(`/carrito/${id_carrito}`, { method: 'DELETE' });
    cargarCarrito();
};

const eliminarTodosDelCarrito = async (nombre) => {
    // Se eliminan todas las unidades del producto seleccionado
    const itemsAEliminar = carritoGlobal.filter(i => i.nombre === nombre);
    for (let item of itemsAEliminar) {
        await fetch(`/carrito/${item.id_carrito}`, { method: 'DELETE' });
    }
    cargarCarrito();
};

// Se ejecuta la carga inicial
cargarProductos();
cargarCarrito();