import random


def es_primo(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generar_primo(bits):
    while True:
        p = random.getrandbits(bits)
        if es_primo(p):
            return p


def mcd_extendido(a, b):
    if a == 0:
        return b, 0, 1
    else:
        mcd, x, y = mcd_extendido(b % a, a)
        return mcd, y - (b // a) * x, x


def inverso_modular(a, m):
    mcd, x, _ = mcd_extendido(a, m)
    if mcd != 1:
        raise Exception("El inverso multiplicativo no existe")
    else:
        return x % m


def generar_claves(bits):
    p = generar_primo(bits // 2)
    q = generar_primo(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = inverso_modular(e, phi)

    return ((e, n), (d, n), (p, q))


def cambiar_base(num, base):
    if num == 0:
        return [0]
    digitos = []
    while num:
        digitos.append(num % base)
        num //= base
    return digitos[::-1]


def cuadrado_y_multiplicacion(base, exponente, modulo):
    resultado = 1
    base = base % modulo
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        exponente = exponente >> 1
        base = (base * base) % modulo
    return resultado


def cifrar(mensaje, clave_publica):
    e, n = clave_publica
    mensaje_int = int.from_bytes(mensaje.encode(), 'big')
    return cuadrado_y_multiplicacion(mensaje_int, e, n)


def descifrar(texto_cifrado, clave_privada, p, q):
    d, n = clave_privada

    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = inverso_modular(q, p)

    m1 = cuadrado_y_multiplicacion(texto_cifrado % p, dp, p)
    m2 = cuadrado_y_multiplicacion(texto_cifrado % q, dq, q)
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q

    return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()


bits = 256
clave_publica, clave_privada, (p, q) = generar_claves(bits)

print(f"Clave pública: {clave_publica}")
print(f"Clave privada: {clave_privada}")
print(f"Primos p: {p}, q: {q}")

mensaje = str(input("Ingresa tu palabra: "))
print(f"Mensaje original: {mensaje}")

cifrado = cifrar(mensaje, clave_publica)
print(f"Mensaje cifrado: {cifrado}")

descifrado = descifrar(cifrado, clave_privada, p, q)
print(f"Mensaje descifrado: {descifrado}")