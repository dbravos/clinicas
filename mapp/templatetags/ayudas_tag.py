from django import template

register = template.Library()


AYUDAS = {

    "menu-principal": {
        "titulo": "Panel principal",
        "tooltip": "Ayuda del Panel principal",
        "contenido": """
            <p>
                AL inicio es necesario entrar al menu de Configuracion porque aqui es donde estan las opciones de entrada
                de Datos de la clinica y el mantenimiento de Usuarios.
                inicialmente siempre habra un usuario administrativo, con este se agregaran los usuarios necesarios
                es recomendable que cada usuario sea identificado el roll que tiene, ya sea de oficina,consejero,etc.
                tambien que permisos se le estan otorgando para que este usuario pueda accesar los diferentes modulos.
                Nota importante :            
                La aplicacion se cierra automaticamente (logout) a los 15 minutos de inactividad. 
                 
            </p>

        
        """
    },


    "menu_general": {
        "titulo": "Menu general para trabajo con internos",
        "tooltip": "Ayuda del menu general para trabajo con internos",
        "contenido": """
            <p>
                En esta sección puedes administrar la información
                generada en los modulos de consejeria,psicologia,medico y seguimiento.
            </p>

            <h6>¿Qué puedes hacer?</h6>
            <ul> Consejeria
                 <li>Los pricipales formatos requeridos por la CONASAMA como son Entrevista incial,</li>
                 <li>Cuestionario ASSIST,Sintomas de psicosis, de Depresion, Satisfaccion de vida,</li>
                 <li>asi como notas de evolucion individual, familiar y grupal y digitalizar y desplegar las tareas</li>
            </ul>
                           
            <ul> Psicologia
                 <li>La hoja de atencion psicologica inicial y las notas de evolucion</li>
            </ul>
            <ul> Medico
                 <li> El diagnostico inicial, Emision de recetas y el Historial medico</li>
                 <li> Aqui solo hay que hacer notar que para moder imprimir una receta primero hay que emitirla</li>
                 <li> o sea grabarla </li>
                 <li> al momento de grabarla apareceria en la parte de abajo de la pantalla de captura</li>
                 
            </ul>
            <ul> Seguimiento
                 <li> Hoja incial del seguimiento y las notas de evolucion</li>
                 <li> La hoja inicial de seguimiento es un formato parecido al formato de la entrevista inicial</li>
                 <li> y las notas de evolucion muy semejantes a las de consejeria y la mecanica es la misma </li>
                 
            </ul>
                                         

            <h6>Importante</h6>

            <p>
                Todos los formatos son sencillos y amigables en su captura solo las notas de evolucion y emision de 
                recetas es diferente el manejo pero en la pantalla correspondiente existe ayuda.
                Siempre Verifica que la información capturada sea correcta
                antes de guardar los cambios.
            </p>
        """
    },

    "internos": {
        "titulo": "Módulo de Internos",
        "tooltip": "Ayuda del módulo de Internos",
        "contenido": """
           <p>
               En esta sección puedes administrar la información
               de las personas internadas en la clínica.
           </p>

           <h6>¿Qué puedes hacer?</h6>

           <ul>
               <li>Agregar un nuevo interno dandole click en el boton superior izquierdo.</li>
               <li>Para consultar y/o modificar informacion ya existente darle click en el boton que dice "Editar" colocandose en el renglo/registro requerido.</li>
               <li>Asi mismo se pueden imprimir los reportes de solicitud de internacion, reporte de internacion, contrato y demas en esta misma opcion.</li>
               <li>Cuando se "Clickea" el boton de "Seleccionar" este es para trabajar con consejeria,psicoclogia y el medico.</li>
               <li>O bien registrar la salida en el boton que corresponde a "Registrar salida".</li>
           </ul>

           <h6>Importante</h6>

           <p>
               Verifica que la información capturada sea correcta
               antes de guardar los cambios.
           </p>
       """
    },

    "interno": {
        "titulo": "Pantalla de datos del interno",
        "tooltip": "Ayuda para trabajar con las opciones de manteminieto del registro del interno",
        "contenido": """
         
            <h6>Información del interno</h6>

            <p>
                Captura los datos solicitados procurando que
                la información sea correcta y completa.
            </p>

            <h6>Programacion de cuotas voluntarias</h6>

            <ul>
                <li>En la pestaña de "Datos generales" hasta el final esta un recuadro donde hay que programar las cuotas voluntarias para efecto que se cree un estado de cuenta</li>
                <li>Tambien aqui esta el boton de las impresiones varias necesarias al momento del ingreso del interno</li>
            </ul>

            <h6>Guardar</h6>

            <p>
                Revisa la información antes de seleccionar
                el botón Guardar.
            </p>
        """
    },

    "cuotas": {
        "titulo": "Opcion de captura de cuotas",
        "tooltip": "Ayuda para trabajar con la captura de cuotas voluntarias",
        "contenido": """

           <h6>Captura de cuotas</h6>
           <ul>Esta pantalla nos permite dar entrada a las cuotas voluntarias.
             <li> Se puede accesar la informacion del estado de cuenta del interno
              ya sea por numero de expediente o por nombre, al asi hacerlo se 
              despliega el estado de cuenta y nos prepara los archivos para la 
              captura de la informacion de la o las cuotas recibidas.</li>
              <h6>En los campos de captura tenemos:</h6>
              <li>Concepto    : Este pude ser la aportacion total, cuota por pagar, cuota voluntaria,
                            abono a cuota voluntaria o bien cancelacion de movimiento.</li>
              <li>Responsable : Propone el nombre del responsable que esta registrado en el expediente,
                            pero se puede modificar.</li>
              <li>Importe     : Propone el importe registrado en la programacion de las cuotas pero se
                            puede modificar.</li>
              <li>Fecha       : Propone la fecha del dia, tambien modificable</li>
              <li>Periodo     : Fechas que abarca el importe aportado.</li>
              <li>Observaciones: Hacer referencia al movimiento.</li>
               
                            
                                    
             
           </ul>

          

           <p>
               Revisa la información antes de seleccionar
               el botón Guardar.
           </p>
       """
    },
    "recibos": {
        "titulo": "Opcion de Recibos",
        "tooltip": "Ayuda para dar mantenimiento a la tabla de recibos",
        "contenido": """

          <h6>Recibos</h6>
          <ul>Esta pantalla nos permite trabajar con los recibos emitidos.
            <li> Se puede o pueden accesar el o los recibos emitidos ya sea por folio, numero de expediente o fechas.</li>
             <h6>Los campos desplegados son :</h6>
             <li>Folio      : Numero del recibo asignado automaticamente por sistema en un orden consecutivo</li>
             <li>Fecha      : Fecha de emision del recibo.</li>
             <li>Expediente : Numero del expediente del interno al cual le fue emitido este folio.</li>
             <li>Concepto/
                 Referencia : Breve explicacion del porque se emitio dicho recibo</li>
             <li>Importe    : Valor del recibo.</li>
             <li>Estatus    : Activo o Cancelado.</li>
             <li>Y hay dos botones, uno de impresion y otro de cancelacion, el de impresion como es su definicion es para imprimir
                 el recibo o recibos emitidos y el de cancelacion en caso de haber sido un movimiento erroneo poder regresar ese importe o valor al estado de cuenta
                 del interno identificando el motivo por el cual ha sido cancelado</li>
  
          </ul>



          <p>
              Revisa la información antes de seleccionar
              el botón Guardar.
          </p>
      """
    },

    "notas_evolucion_consejeria": {
        "titulo": "Notas de evolucion consejeria",
        "tooltip": "Ayuda para dar mantenimiento a las notas de evolucion de consejeria",
        "contenido": """

         <h6>¿Qué puedes hacer?</h6>
        <p>Esta pantalla nos enlista las notas de evolucion de consejeria.
           Se puede crear una nueva, siempre y cuando no haya una sesion abierta.
          o bien accesar alguna ya creada, si la nota ya esta cerrada (en la columna de status lo diria)
          solo se podra consultar, en caso de que estuviera abierta se selecciona y se puede modificar, o bien
          Cerrarla para poder crear otra. Al momento de cerrarla nos preguntara la fecha de cierre y tambien
          una pregunta de seguridad.
          
          </p>



        <p>
            Revisa la información antes de seleccionar
            el botón Guardar.
        </p>
    """
    },

    "notas_evolucion_psicologica": {
        "titulo": "Notas de evolucion psicologica",
        "tooltip": "Ayuda para dar mantenimiento a las notas de evolucion psicologica",
        "contenido": """

       <h6>¿Qué puedes hacer?</h6>
      <p>Esta pantalla nos enlista las notas de evolucion de psicologia.
         Se puede crear una nueva, siempre y cuando no haya una sesion abierta.
        o bien accesar alguna ya creada, si la nota ya esta cerrada (en la columna de status lo diria)
        solo se podra consultar, en caso de que estuviera abierta se selecciona y se puede modificar, o bien
        Cerrarla para poder crear otra. Al momento de cerrarla nos preguntara la fecha de cierre y tambien
        una pregunta de seguridad.

        </p>



      <p>
          Revisa la información antes de seleccionar
          el botón Guardar.
      </p>
  """
    },

}


@register.inclusion_tag("includes/ayuda.html")
def ayuda(nombre):

    return {
        "ayuda": AYUDAS.get(
            nombre,
            {
                "titulo": "Ayuda",
                "tooltip": "Ayuda de esta pantalla",
                "contenido": """
                    <p>
                        No existe información de ayuda
                        disponible para esta pantalla.
                    </p>
                """
            }
        ),
        "ayuda_id": f"modalAyuda_{nombre}",
    }