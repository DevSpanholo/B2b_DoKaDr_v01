import random
import hashlib

def generate_key(secret, length=16):
    """
    Gera uma chave de ativação com base em um segredo compartilhado.
    """
    key = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))
    hash_object = hashlib.sha256((key + secret).encode())
    key_hash = hash_object.hexdigest()[:8]  # Usa apenas os primeiros 8 caracteres do hash
    return f"{key}-{key_hash}"

def main():
    secret = "minha-chave-secreta"  # Este segredo deve ser igual no cliente
    keys = [generate_key(secret) for _ in range(200)]  # Gera 10 chaves
    print("Chaves de ativação geradas:")
    for key in keys:
        print(key)

if __name__ == "__main__":
    main()
