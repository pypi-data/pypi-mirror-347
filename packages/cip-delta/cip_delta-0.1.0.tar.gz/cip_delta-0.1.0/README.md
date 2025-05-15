# CIP — Cifra de Integridade Primal

A **CIP (Cifra de Integridade Primal)** é um sistema de autenticação vetorial baseado em **projeção espectral sobre a estrutura dos números primos**.  
Ela **não utiliza criptografia clássica**, **não exige chaves secretas**, e oferece **integridade absoluta de dados**, mesmo diante de **alterações microscópicas (1 bit)**.

Este pacote implementa o núcleo funcional do CIP para uso local ou em notebooks Python.

> 📦 Módulo principal: `cip.core`

---

## 🔧 Funcionalidades Principais

### `delta_pi(x)`
- Calcula a dualidade primal dos primos.
- Define a estrutura oscilatória central do sistema.

### `construct_cosine_matrix(x, size)`
- Gera uma matriz simétrica a partir de `|Δπ(x)|`.
- Essa matriz é usada para obter a base vetorial harmônica.

### `codificar_bloco(texto, bloco_size)`
- Codifica um bloco de texto ou bytes em vetor `float` normalizado.

### `decodificar_bloco(vetor)`
- Reconstrói os bytes a partir do vetor decodificado.

### `cip_assinar_blocos_bytes(dados, x, size)`
- Assina blocos binários por projeção espectral + SHA-256.
- Retorna a lista de hashes e a chave estrutural usada.

### `cip_verificar_blocos_bytes(dados, assinaturas_ref, chave)`
- Verifica a integridade de cada bloco.
- Detecta qualquer alteração estrutural no conteúdo.

### `cip_cifrar_blocos_bytes(dados, x, size)`
- Cifra blocos em vetores espectrais.
- Os dados cifrados parecem ruído puro sem a base correta.

### `cip_decifrar_blocos_bytes(data_or_path)`
- Reverte os vetores cifrados para os bytes originais, com a base harmônica.
- Impede reconstrução se a base for incorreta.

---

## ⚙️ Características Técnicas

- Estrutura espectral baseada em `|Δπ(x)|`, sem uso direto da função zeta.
- Projeção vetorial reversível sobre base derivada dos números primos.
- SHA-256 aplicado sobre projeções vetoriais (não sobre os dados em si).
- Compatível com qualquer tipo de dado binário: `.txt`, `.pdf`, `.png`, `.mp3`, etc.
- Resistente a ataques quânticos: **sem fatoração, sem curva elíptica, sem segredo**.

---

## 🚀 Exemplo de Uso Básico

```python
from cip.core import (
    cip_assinar_blocos_bytes,
    cip_verificar_blocos_bytes,
    cip_cifrar_blocos_bytes,
    cip_decifrar_blocos_bytes
)

with open("documento.pdf", "rb") as f:
    dados = f.read()

assinaturas, chave = cip_assinar_blocos_bytes(dados)
alterados, total = cip_verificar_blocos_bytes(dados, assinaturas, chave)

print(f"Blocos alterados: {alterados} / {total}")
```

## Autor
**Alvaro Costa**  
Auditor Fiscal da Receita Estadual de São Paulo  
Cientista de Dados — Fundador do Projeto DELTA  
São Paulo, Brasil

Projeto DELTA — Dual Eigenvalue Lattice for Transformative Arithmetic

Repositório oficial: https://github.com/costaalv/projeto-delta
Licença: MIT
