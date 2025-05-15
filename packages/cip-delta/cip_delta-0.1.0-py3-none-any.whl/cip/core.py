import numpy as np
from sympy import primerange
from numpy.linalg import eigh
from math import log
import hashlib

# -------------------------------
# Funções auxiliares principais
# -------------------------------

def delta_pi(x):
    def pi(n):
        return len(list(primerange(1, n + 1)))
    return pi(x) - 2 * pi(x // 2)

def construct_cosine_matrix(x, size):
    delta_vals = [delta_pi(i) for i in range(x, x + size)]
    matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            matrix[i, j] = np.cos(delta_vals[i] * log(x + j))
    return (matrix + matrix.T) / 2

def codificar_bloco(texto, bloco_size):
    if isinstance(texto, str):
        vetor = np.frombuffer(texto.encode('utf-8'), dtype=np.uint8).astype(float)
    elif isinstance(texto, bytes):
        vetor = np.frombuffer(texto, dtype=np.uint8).astype(float)
    else:
        raise TypeError("O bloco deve ser do tipo str ou bytes.")
    return np.pad(vetor, (0, max(0, bloco_size - len(vetor))))[:bloco_size]

def decodificar_bloco(vetor):
    vetor_int = np.clip(np.round(vetor), 0, 255).astype(np.uint8)
    return bytes(vetor_int)

# -------------------------------
# Cifragem e Decifragem em blocos
# -------------------------------

def cip_cifrar_blocos_bytes(dados, x=7213, size=1024):
    """
    Cifra um conteúdo em bytes usando projeção vetorial em base harmônica derivada de Δπ.
    Retorna um dicionário com os dados prontos para serem salvos como .npz.
    """
    matriz = construct_cosine_matrix(x, size)
    _, autovetores = eigh(matriz)
    base = autovetores[:, -size:]

    blocos = [dados[i:i+size] for i in range(0, len(dados), size)]
    cifrado = [base @ codificar_bloco(bloco, size) for bloco in blocos]

    blocos_bytes = [np.frombuffer(bloco.ljust(size, b'\x00'), dtype=np.uint8) for bloco in blocos]

    return {
        'cifrado': cifrado,
        'x': x,
        'size': size,
        'blocos_bytes': blocos_bytes
    }

def cip_assinar_blocos_bytes(dados, x=7213, size=1024):
    matriz = construct_cosine_matrix(x, size)
    _, autovetores = eigh(matriz)
    base = autovetores[:, -size:]
    base_inv = np.linalg.pinv(base)

    blocos = [dados[i:i+size] for i in range(0, len(dados), size)]
    assinaturas = []
    for bloco in blocos:
        vetor = codificar_bloco(bloco, size)
        projecao = base_inv @ vetor
        hash_val = hashlib.sha256(projecao.astype(np.float32).tobytes()).hexdigest()
        assinaturas.append(hash_val)
    return assinaturas, {'x': x, 'size': size}

def cip_decifrar_blocos_bytes(data_or_path):
    """
    Reconstrói o conteúdo original a partir de dados cifrados em blocos,
    retornando os bytes decodificados.

    Pode receber diretamente um dicionário (npz-like) ou o caminho para um .npz.
    """
    import numpy as np
    from numpy.linalg import pinv, eigh

    if isinstance(data_or_path, str):
        data = np.load(data_or_path, allow_pickle=True)
    else:
        data = data_or_path

    cifrado = data['cifrado']
    x = int(data['x'])
    size = int(data['size'])

    # Se os blocos originais estiverem disponíveis, usar diretamente
    if 'blocos_bytes' in data:
        blocos_bytes = data['blocos_bytes']
        return b''.join([bloco.tobytes() for bloco in blocos_bytes])

    # Caso contrário, reconstruir via projeção reversa
    matriz = construct_cosine_matrix(x, size)
    _, autovetores = eigh(matriz)
    base = autovetores[:, -size:]
    base_inv = pinv(base)

    blocos = []
    for bloco in cifrado:
        vetor_reconstruido = base_inv @ bloco
        vetor_int = np.clip(np.round(vetor_reconstruido), 0, 255).astype(np.uint8)
        blocos.append(bytes(vetor_int))

    return b''.join(blocos)

def cip_verificar_blocos_bytes(dados, assinaturas_ref, chave):
    matriz = construct_cosine_matrix(chave['x'], chave['size'])
    _, autovetores = eigh(matriz)
    base = autovetores[:, -chave['size']:]
    base_inv = np.linalg.pinv(base)

    blocos = [dados[i:i+chave['size']] for i in range(0, len(dados), chave['size'])]
    alterados = 0
    for i, bloco in enumerate(blocos):
        vetor = codificar_bloco(bloco, chave['size'])
        projecao = base_inv @ vetor
        hash_val = hashlib.sha256(projecao.astype(np.float32).tobytes()).hexdigest()
        if i >= len(assinaturas_ref) or hash_val != assinaturas_ref[i]:
            alterados += 1
    return alterados, len(blocos)

