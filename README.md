xaes: cifrador y descifrador compatible con OpenSSL

Programa de consola en Python que cifra y descifra datos con AES-128 en modo CBC, derivando la clave a partir de una contraseña con PBKDF2 (SHA-256). El formato de salida es compatible con OpenSSL, así que se puede cifrar con xaes.py y descifrar con openssl, o al revés.

Proyecto realizado para la asignatura EI1034 - Seguridad Informática del Grado en Ingeniería Informática (Universitat Jaume I).

Características
Cifrado y descifrado con AES de 128 bits en modo CBC.
Derivación de clave con PBKDF2-HMAC-SHA256 (salt aleatorio de 8 bytes y 10 000 iteraciones).
Compatible con OpenSSL (aes-128-cbc -pbkdf2).
Trabaja con la entrada y la salida estándar, por lo que se puede usar en tuberías (|) y en procesos automáticos sin modificar el código.
Relleno de bloques con PKCS7.
Requisitos
Python 3 (versión reciente).
La biblioteca PyCryptodomex, que proporciona el paquete Cryptodome.
Pensado para Linux/Unix, aunque también funciona en Windows con Python instalado.

Instalación de las dependencias en Debian/Ubuntu:

bash
sudo apt install python3
pip install pycryptodomex

Después, da permisos de ejecución al script:

bash
chmod +x xaes.py
Uso
xaes.py [-e|-d] <contraseña>
Opción	Acción
-e	Cifrar (encrypt)
-d	Descifrar (decrypt)

El programa lee los datos de la entrada estándar y escribe el resultado en la salida estándar.

Cifrar
bash
cat myfile | ./xaes.py -e "mi contraseña" > myfile.enc

Cifra myfile con la contraseña indicada y guarda el resultado en myfile.enc.

Descifrar
bash
cat myfile.enc | ./xaes.py -d "mi contraseña" > myfile.dec

Descifra myfile.enc con la misma contraseña y guarda el resultado en myfile.dec.

Compatibilidad con OpenSSL

Cifrar con OpenSSL y descifrar con xaes.py:

bash
cat myfile | openssl aes-128-cbc -pbkdf2 -k "mi contraseña" > myfile.enc
cat myfile.enc | ./xaes.py -d "mi contraseña" > myfile.dec

Cifrar con xaes.py y descifrar con OpenSSL:

bash
cat myfile | ./xaes.py -e "mi contraseña" > myfile.enc
cat myfile.enc | openssl aes-128-cbc -pbkdf2 -d -k "mi contraseña" > myfile.dec
Cómo funciona
Derivación de clave (PBKDF2)

La contraseña se transforma en una clave de cifrado con PBKDF2 y SHA-256. El algoritmo recibe la contraseña, una salt aleatoria de 8 bytes, el número de iteraciones (10 000) y la longitud de la clave derivada (32 bytes). Esos 32 bytes se dividen en dos partes:

Los primeros 16 bytes son la clave AES.
Los últimos 16 bytes son el vector de inicialización (IV) del modo CBC.
Formato de los datos cifrados

Para que OpenSSL pueda reconocer los datos, la salida empieza con una cabecera de 16 bytes:

[ "Salted__" (8 bytes) ] + [ salt (8 bytes) ] + [ datos cifrados ]

OpenSSL usa la salt de la cabecera para volver a derivar la clave y descifrar correctamente.

Cifrado AES-CBC

Se usa el modo CBC en lugar de ECB porque el vector de inicialización evita que aparezcan patrones repetidos en el texto cifrado. Los datos se rellenan con PKCS7 hasta que su longitud sea múltiplo del tamaño de bloque (16 bytes).

Cifrar: pad() sobre los datos y después cipher.encrypt().
Descifrar: cipher.decrypt() y después unpad() para recuperar los datos originales.
Limitaciones

Es un proyecto académico, así que conviene tener en cuenta lo siguiente:

El modo CBC no autentica los datos: no detecta si el archivo cifrado ha sido modificado. Hoy se suelen preferir modos autenticados como AES-GCM.
La contraseña se pasa como argumento de la línea de comandos, por lo que puede quedar visible en el historial del terminal o en la lista de procesos.
Se usan 10 000 iteraciones de PBKDF2 para mantener la compatibilidad con OpenSSL; para uso real se recomienda un número mayor.
Referencias
Documentación de PyCryptodome: AES
Documentación de PyCryptodome: padding
Python: hashlib.pbkdf2_hmac
Stack Overflow: OpenSSL y la cabecera Salted__
Autor

Iván Roig Soligó
