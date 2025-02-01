
# Commerce Web50 project

## Descripción
Aplicación web de subastas desarrollada en Django que permite a los usuarios crear listados, realizar ofertas, comentar, gestionar una lista de seguimiento y recibir notificaciones en tiempo real.

## Características Clave
- **Autenticación de Usuarios**: Registro, inicio/cierre de sesión.
- **Gestión de Listados**: 
  - Creación con título, descripción, imagen, precio inicial y categoría.
  - Cierre manual de subastas con notificación al ganador.
- **Sistema de Ofertas**: Ofertas competitivas con actualización en tiempo real.
- **Interacción Social**: 
  - Comentarios en listados.
  - Lista de seguimiento para favoritos.
- **Notificaciones**: Alertas para nuevas ofertas, comentarios y resultados de subastas.
- **Paginación**: Visualización de 10 listados activos por página en la vista principal.

## Tecnologías
- **Backend**: Django 3+
- **Frontend**: HTML, CSS (estilos personalizados)
- **Base de Datos**: SQLite (por defecto, configurable)


## Requisitos Previos
- Python 3.+
- Django 5.0+

## Instalación y Ejecución
1. **Clonar Repositorio**
   ```bash
   git clone https://github.com/Wesleykyle2005/Commerce-Web50.git
   ```

2. **Instalar Dependencias**
   ```bash
   pip install django
   ```

3. **Configurar Base de Datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Poblar Datos de Prueba**
   ```bash
   python make_insertions.py
   ```
   *Crea:*
   - 30 usuarios
   - 30 categorías
   - 30 listados con ofertas y comentarios
   - Superusuario: **Usuario:** Admin1234 | **Contraseña:** Admin1234

5. **Iniciar Servidor**
   ```bash
   python manage.py runserver
   ```
   Acceder desde: http://localhost:8000

## Uso del Sistema
- **Acceso al Admin**: http://localhost:8000/admin (usar credenciales del superusuario)
- **Funcionalidades Destacadas**:
  - Usuarios registrados pueden crear/listar productos.
  - Ofertas deben superar el valor actual.
  - Notificaciones visibles en la barra de navegación.
  - Los creadores de listados pueden cerrar subastas manualmente.

## Notas Técnicas
- **Modelo de Usuario Personalizado**: Hereda de `AbstractUser` para futuras extensiones.
- **Seguridad**: Vistas críticas protegidas con `@login_required`.
- **Optimización**: Paginación para manejar grandes volúmenes de listados.
- **Notificaciones**: Sistema integrado usando el modelo `Notification` con relaciones a usuarios.

