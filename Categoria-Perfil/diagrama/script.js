
function mostrarContenido(seccion) {
    let contenido = document.getElementById('contenido');

    if (seccion === 'archivos') {
        contenido.innerHTML = `
            <h2>Archivos</h2>
            <button>Subir Archivo</button>
            <button>Eliminar Archivo</button>
            <p>Aquí puedes subir y eliminar archivos.</p>
        `;
    } else if (seccion === 'categoria') {
        contenido.innerHTML = `
            <h2>Categorías</h2>
            <div class="categoria">
                <button>Trabajo</button>
                <button>Redes Sociales</button>
                <button>Bancario</button>
            </div>
        `;
    } else if (seccion === 'generar-clave') {
        contenido.innerHTML = `
            <h2>Generar Contraseña</h2>
            <p>Haz clic en el botón para generar una nueva contraseña:</p>
            <button>Generar Contraseña</button>
        `;
    } else if (seccion === 'ajustes') {
        contenido.innerHTML = `
            <h2>Ajustes</h2>
            <p>Ajusta las preferencias de la aplicación aquí.</p>
            <button>Guardar Ajustes</button>
        `;
    } else if (seccion === 'perfil') {
        contenido.innerHTML = `
            <h2>Mi Perfil</h2>
            <table>
                <tr>
                    <th>Nombre:</th>
                    <td>Juan Pérez</td>
                </tr>
                <tr>
                    <th>Apellidos:</th>
                    <td>Pérez López</td>
                </tr>
                <tr>
                    <th>Teléfono:</th>
                    <td>+51 987 654 321</td>
                </tr>
                <tr>
                    <th>Correo Electrónico:</th>
                    <td>juan.perez@correo.com</td>
                </tr>
            </table>
        `;
    }
}
