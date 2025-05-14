import base64
import hashlib
import random
import string

class UltraUtils:

    # ====================== العمليات الحسابية ===========================
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

    # ======================= تشفير نصوص ================================
    @staticmethod
    def encrypt_text(text, key=5):
        return ''.join(chr((ord(c) + key) % 256) for c in text)

    @staticmethod
    def decrypt_text(text, key=5):
        return ''.join(chr((ord(c) - key) % 256) for c in text)

    # ======================= تشفير أرقام ===============================
    @staticmethod
    def encrypt_number(num):
        return int(''.join(str((int(d) + 7) % 10) for d in str(num)))

    @staticmethod
    def decrypt_number(num):
        return int(''.join(str((int(d) - 7) % 10) for d in str(num)))

    # ===================== تشفير بايتات ord ============================
    @staticmethod
    def encrypt_bytes(source):
        return [(ord(c) + 42) % 256 for c in source]

    @staticmethod
    def decrypt_bytes(data):
        return ''.join(chr((b - 42) % 256) for b in data)

    # ====================== تقوية التشفير ===============================
    @staticmethod
    def reinforce(data):
        step1 = base64.b64encode(data.encode()).decode()
        step2 = ''.join(reversed(step1))
        step3 = hashlib.sha256(step2.encode()).hexdigest()
        return step3

    # ===================== دالة مساعدة للتشفير ==========================
    class defTest:
        @staticmethod
        def b64encode(text):
            encoded = base64.b64encode(text.encode()).decode()
            pattern = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return f"{pattern[:5]}{encoded[::-1]}{pattern[5:]}"  # تطوير للشكل الأصلي

        @staticmethod
        def b64decode(data):
            middle = data[5:-5]
            decoded = base64.b64decode(middle[::-1]).decode()
            return decoded

    # =================== خوارزمية تشفير غريبة ============================
    @staticmethod
    def alien_encrypt(text):
        encrypted = ''
        for i, c in enumerate(text):
            encrypted += chr((ord(c) + i*3 + 13) % 256)
        return base64.b85encode(encrypted.encode()).decode()

    @staticmethod
    def alien_decrypt(text):
        decoded = base64.b85decode(text.encode()).decode()
        decrypted = ''
        for i, c in enumerate(decoded):
            decrypted += chr((ord(c) - i*3 - 13) % 256)
        return decrypted

    # =================== تشفير XOR مع مفتاح =============================
    @staticmethod
    def xor_encrypt(text, key):
        key_len = len(key)
        encrypted_chars = []
        for i, c in enumerate(text):
            encrypted_c = chr(ord(c) ^ ord(key[i % key_len]))
            encrypted_chars.append(encrypted_c)
        return ''.join(encrypted_chars)

    @staticmethod
    def xor_decrypt(ciphertext, key):
        # XOR is symmetric
        return UltraUtils.xor_encrypt(ciphertext, key)

    # =================== تشفير قيصر (Caesar) مع مفتاح متغير ============
    @staticmethod
    def caesar_encrypt(text, shift):
        return ''.join(chr((ord(c) + shift) % 256) for c in text)

    @staticmethod
    def caesar_decrypt(text, shift):
        return ''.join(chr((ord(c) - shift) % 256) for c in text)

    # =================== تشفير فيجنر (Vigenere cipher) ===================
    @staticmethod
    def vigenere_encrypt(plaintext, key):
        encrypted = []
        key_len = len(key)
        for i, c in enumerate(plaintext):
            shift = ord(key[i % key_len])
            encrypted.append(chr((ord(c) + shift) % 256))
        return ''.join(encrypted)

    @staticmethod
    def vigenere_decrypt(ciphertext, key):
        decrypted = []
        key_len = len(key)
        for i, c in enumerate(ciphertext):
            shift = ord(key[i % key_len])
            decrypted.append(chr((ord(c) - shift) % 256))
        return ''.join(decrypted)

    # =================== خوارزميات تجزئة Hashing ========================
    @staticmethod
    def hash_md5(data):
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def hash_sha1(data):
        return hashlib.sha1(data.encode()).hexdigest()

    @staticmethod
    def hash_sha512(data):
        return hashlib.sha512(data.encode()).hexdigest()

    @staticmethod
    def hash_blake2b(data):
        return hashlib.blake2b(data.encode()).hexdigest()

    # =================== تشفير مخصص مع قاعدة64 وتحويل مخصص ===================
    @staticmethod
    def custom_base64_encrypt(text):
        b64 = base64.b64encode(text.encode()).decode()
        chars = list(b64)
        n = len(chars)
        for i in range(0, n-1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        shuffled = ''.join(chars)
        return shuffled[::-1]

    @staticmethod
    def custom_base64_decrypt(text):
        reversed_text = text[::-1]
        chars = list(reversed_text)
        n = len(chars)
        for i in range(0, n-1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        unshuffled = ''.join(chars)
        decoded = base64.b64decode(unshuffled).decode()
        return decoded

    # =================== تشفير أرقام مخصص بمقاس دوران ======================
    @staticmethod
    def rotate_digits_encrypt(num):
        digits = list(str(num))
        rotated = digits[1:] + digits[:1]
        return int(''.join(rotated))

    @staticmethod
    def rotate_digits_decrypt(num):
        digits = list(str(num))
        rotated = digits[-1:] + digits[:-1]
        return int(''.join(rotated))

    # =================== تشفير فيستيل مخصص (مستوحى) =======================
    @staticmethod
    def feistel_encrypt(text, rounds=4, key=0xAB):
        data = list(text.encode())
        n = len(data)
        if n % 2 != 0:
            data.append(0)
            n += 1
        half = n // 2
        left = data[:half]
        right = data[half:]
        for r in range(rounds):
            f = [(b ^ (key + r)) for b in right]
            new_left = [l ^ f[i] for i, l in enumerate(left)]
            left, right = right, new_left
        encrypted = left + right
        return base64.b64encode(bytes(encrypted)).decode()

    @staticmethod
    def feistel_decrypt(ciphertext, rounds=4, key=0xAB):
        data = list(base64.b64decode(ciphertext.encode()))
        n = len(data)
        half = n // 2
        left = data[:half]
        right = data[half:]
        for r in reversed(range(rounds)):
            f = [(b ^ (key + r)) for b in left]
            new_right = [r ^ f[i] for i, r in enumerate(right)]
            right, left = left, new_right
        if left and left[-1] == 0:
            left = left[:-1]
        decrypted = left + right
        return bytes(decrypted).decode(errors='ignore')

    # =================== تشفير متعدد المراحل خاص ==========================
    @staticmethod
    def multi_stage_encrypt(text, key):
        step1 = UltraUtils.caesar_encrypt(text, 7)
        step2 = UltraUtils.xor_encrypt(step1, key)
        step3 = UltraUtils.custom_base64_encrypt(step2)
        return step3

    @staticmethod
    def multi_stage_decrypt(ciphertext, key):
        step1 = UltraUtils.custom_base64_decrypt(ciphertext)
        step2 = UltraUtils.xor_decrypt(step1, key)
        step3 = UltraUtils.caesar_decrypt(step2, 7)
        return step3

    # =================== تشفير خاص وحصري للمكتبة فقط ======================
    @staticmethod
    def ultra_unique_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        k = len(key_bytes)
        for i in range(n):
            swap_idx = (i + key_bytes[i % k]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        def rotate_left(b, count):
            return ((b << count) & 0xFF) | (b >> (8 - count))
        mixed = []
        for i, b in enumerate(data):
            b = b ^ key_bytes[i % k]
            b = rotate_left(b, (key_bytes[(i+1) % k] % 8))
            mixed.append(b)
        result = ''.join(f"{b:02x}" for b in mixed)
        return result

    @staticmethod
    def ultra_unique_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        def rotate_right(b, count):
            return (b >> count) | ((b << (8 - count)) & 0xFF)
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = bytes.fromhex(ciphertext)
        data = list(data)
        unmixed = []
        for i, b in enumerate(data):
            b = rotate_right(b, (key_bytes[(i+1) % k] % 8))
            b = b ^ key_bytes[i % k]
            unmixed.append(b)
        n = len(unmixed)
        for i in reversed(range(n)):
            swap_idx = (i + key_bytes[i % k]) % n
            unmixed[i], unmixed[swap_idx] = unmixed[swap_idx], unmixed[i]
        return bytes(unmixed).decode(errors='ignore')

    # =================== خوارزمية تشفير تقدمية متعددة الأبجدية جديدة =======
    @staticmethod
    def polyalphabetic_progressive_encrypt(text, key):
        key_len = len(key)
        encrypted = []
        for i, c in enumerate(text):
            shift = (ord(key[i % key_len]) + i) % 256
            encrypted.append(chr((ord(c) + shift) % 256))
        return ''.join(encrypted)

    @staticmethod
    def polyalphabetic_progressive_decrypt(text, key):
        key_len = len(key)
        decrypted = []
        for i, c in enumerate(text):
            shift = (ord(key[i % key_len]) + i) % 256
            decrypted.append(chr((ord(c) - shift) % 256))
        return ''.join(decrypted)

    # =================== خوارزمية تبديل البتات الخاصة =======================
    @staticmethod
    def bit_permutation_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        key_bytes = list(key.encode())
        def permute_bits(b, perm):
            result = 0
            for i in range(8):
                bit = (b >> i) & 1
                result |= bit << perm[i]
            return result
        base_perm = list(range(8))
        random.seed(sum(key_bytes))
        random.shuffle(base_perm)
        data = list(text.encode())
        encrypted = [permute_bits(b, base_perm) for b in data]
        return base64.b64encode(bytes(encrypted)).decode()

    @staticmethod
    def bit_permutation_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        key_bytes = list(key.encode())
        def inverse_permutation(perm):
            inv = [0]*len(perm)
            for i,p in enumerate(perm):
                inv[p] = i
            return inv
        def permute_bits(b, perm):
            result = 0
            for i in range(8):
                bit = (b >> i) & 1
                result |= bit << perm[i]
            return result
        base_perm = list(range(8))
        random.seed(sum(key_bytes))
        random.shuffle(base_perm)
        inv_perm = inverse_permutation(base_perm)
        data = list(base64.b64decode(ciphertext.encode()))
        decrypted = [permute_bits(b, inv_perm) for b in data]
        return bytes(decrypted).decode(errors='ignore')

    # =================== خوارزمية تشفير هجينة متقدمة =======================
    @staticmethod
    def hybrid_advanced_encrypt(text, key):
        step1 = UltraUtils.vigenere_encrypt(text, key)
        step2 = UltraUtils.bit_permutation_encrypt(step1, key)
        nums = [ord(c) for c in UltraUtils.custom_base64_encrypt(step2)]
        rotated_nums = []
        for num in nums:
            rotated_nums.append((num << 1) % 256)
        return ''.join(chr(n) for n in rotated_nums)

    @staticmethod
    def hybrid_advanced_decrypt(ciphertext, key):
        reversed_nums = []
        for c in ciphertext:
            reversed_nums.append((ord(c) >> 1) | ((ord(c) & 1) << 7))
        step1 = ''.join(chr(n) for n in reversed_nums)
        step2 = UltraUtils.custom_base64_decrypt(step1)
        step3 = UltraUtils.bit_permutation_decrypt(step2, key)
        step4 = UltraUtils.vigenere_decrypt(step3, key)
        return step4

    # =================== تشفير أرقام مخصص مع تبديل حرفي أبجدي ============
    @staticmethod
    def alpha_numeric_encrypt(num, key='K3Y'):
        num_str = str(num)
        mapped = []
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        key_sum = sum(ord(c) for c in key)
        for d in num_str:
            idx = (int(d) + key_sum) % len(alphabet)
            mapped.append(alphabet[idx])
        return ''.join(mapped)

    @staticmethod
    def alpha_numeric_decrypt(enc_str, key='K3Y'):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        key_sum = sum(ord(c) for c in key)
        decoded_digits = []
        for c in enc_str:
            idx = alphabet.index(c)
            decoded = (idx - key_sum) % 10
            decoded_digits.append(str(decoded))
        return int(''.join(decoded_digits))

    # =================== خوارزمية تشفير متقدمة وحصرية جديدة جدا =============
    @staticmethod
    def ultra_hyper_encrypt(text, key):
        if not key or len(key) < 4:
            raise ValueError("Key must be string of length at least 4")
        stage1 = UltraUtils.polyalphabetic_progressive_encrypt(text, key)
        data_bytes = list(stage1.encode())
        key_bytes = list(key.encode())
        n = len(data_bytes)
        k = len(key_bytes)
        layer1 = [b ^ key_bytes[i % k] for i, b in enumerate(data_bytes)]
        def permute_bits_layer(b, perm):
            res = 0
            for i in range(8):
                bit = (b >> i) & 1
                res |= bit << perm[i]
            return res
        base_perm = list(range(8))
        seed_val = sum(key_bytes) + len(text)
        random.seed(seed_val)
        random.shuffle(base_perm)
        layer2 = [permute_bits_layer(b, base_perm) for b in layer1]
        def rotate_right(b, n_shift):
            return (b >> n_shift) | ((b << (8 - n_shift)) & 0xFF)
        layer3 = []
        for i, b in enumerate(layer2):
            shift = key_bytes[(i*2) % k] % 8
            rotated = rotate_right(b, shift)
            swap_idx = (i + key_bytes[i % k]) % n
            layer3.append((rotated, swap_idx))
        final_bytes = [0]*n
        for i, (val, swap_idx) in enumerate(layer3):
            final_bytes[swap_idx] = val
        hex_encoded = ''.join(f"{b:02x}" for b in final_bytes)
        return hex_encoded

    @staticmethod
    def ultra_hyper_decrypt(ciphertext, key):
        if not key or len(key) < 4:
            raise ValueError("Key must be string of length at least 4")
        def rotate_left(b, n_shift):
            return ((b << n_shift) & 0xFF) | (b >> (8 - n_shift))
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = bytes.fromhex(ciphertext)
        n = len(data)
        data = list(data)
        inv = [0]*n
        for i in range(n):
            swap_idx = (i + key_bytes[i % k]) % n
            inv[swap_idx] = data[i]
        data = inv
        layer2 = []
        for i, b in enumerate(data):
            shift = key_bytes[(i*2) % k] % 8
            rotated = rotate_left(b, shift)
            layer2.append(rotated)
        def permute_bits_inverse(b, perm):
            res = 0
            for i in range(8):
                bit = (b >> perm[i]) & 1
                res |= bit << i
            return res
        base_perm = list(range(8))
        seed_val = sum(key_bytes) + (n//2)
        random.seed(seed_val)
        random.shuffle(base_perm)
        layer1 = [permute_bits_inverse(b, base_perm) for b in layer2]
        stage1_bytes = [b ^ key_bytes[i % k] for i, b in enumerate(layer1)]
        stage1_text = bytes(stage1_bytes).decode(errors='ignore')
        decrypted_text = UltraUtils.polyalphabetic_progressive_decrypt(stage1_text, key)
        return decrypted_text

    # =================== خوارزمية تشفير تسلسلي مميزة (مخصصة) ================
    @staticmethod
    def sequential_custom_encrypt(text, key):
        """
        تشفير تسلسلي يستعمل خلط مواضع متقدم وتبديل ثنائي مع لف حولي للبتات
        """
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        k = len(key_bytes)

        # خلط متقدم للمواضع (خوارزمية تبديل مستمرة)
        perm_indices = list(range(n))
        for i in range(n-1, 0, -1):
            swap_idx = (i * key_bytes[i % k] + key_bytes[(i*3) % k]) % n
            perm_indices[i], perm_indices[swap_idx] = perm_indices[swap_idx], perm_indices[i]

        permuted = [data[perm_indices[i]] for i in range(n)]

        # تبديل بت ثنائي مع لف حولي
        def rotate_left(b, count):
            return ((b << count) & 0xFF) | (b >> (8 - count))

        encrypted = []
        for i, b in enumerate(permuted):
            count = key_bytes[i % k] % 8
            b = rotate_left(b ^ key_bytes[(i*2) % k], count)
            encrypted.append(b)

        # ترميز base85 للناتج النهائي
        return base64.b85encode(bytes(encrypted)).decode()

    @staticmethod
    def sequential_custom_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        def rotate_right(b, count):
            return (b >> count) | ((b << (8 - count)) & 0xFF)
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = list(base64.b85decode(ciphertext.encode()))
        n = len(data)

        decrypted = []
        for i, b in enumerate(data):
            count = key_bytes[i % k] % 8
            b = rotate_right(b, count)
            b = b ^ key_bytes[(i*2) % k]
            decrypted.append(b)

        perm_indices = list(range(n))
        for i in range(n-1, 0, -1):
            swap_idx = (i * key_bytes[i % k] + key_bytes[(i*3) % k]) % n
            perm_indices[i], perm_indices[swap_idx] = perm_indices[swap_idx], perm_indices[i]

        inv_perm = [0]*n
        for i, idx in enumerate(perm_indices):
            inv_perm[idx] = i

        unpermuted = [decrypted[inv_perm[i]] for i in range(n)]

        return bytes(unpermuted).decode(errors='ignore')

    # =================== تشفير مواضع معقد وإزاحة ديناميكية مُعززة ===========
    @staticmethod
    def dynamic_positional_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        for i in range(n):
            shift = (key_bytes[i % len(key_bytes)] + i*i) % 256
            data[i] = (data[i] + shift) % 256
        # تبديل متكرّر للمواقع بناءً على المفتاح
        for i in range(n):
            swap_idx = (i*i + key_bytes[i % len(key_bytes)]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        return base64.b64encode(bytes(data)).decode()

    @staticmethod
    def dynamic_positional_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(base64.b64decode(ciphertext.encode()))
        key_bytes = list(key.encode())
        n = len(data)
        for i in reversed(range(n)):
            swap_idx = (i*i + key_bytes[i % len(key_bytes)]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        for i in range(n):
            shift = (key_bytes[i % len(key_bytes)] + i*i) % 256
            data[i] = (data[i] - shift) % 256
        return bytes(data).decode(errors='ignore')

    # =================== مزيج تشفير نصي رقمي مخصص عالي التعقيد ==========
    @staticmethod
    def complex_text_number_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")

        # تشفير نصي فيجنر + إزاحة تصاعدية
        vigenere_enc = UltraUtils.polyalphabetic_progressive_encrypt(text, key)

        # ترميز الحروف إلى قائمة أرقام
        nums = [ord(c) for c in vigenere_enc]

        # عمليات حسابية معقدة على الأرقام
        key_sum = sum(ord(c) for c in key)
        nums = [(n * key_sum + i*i) % 9973 for i, n in enumerate(nums)]  # 9973 عدد أولي خاص للتعقيد

        # تحويل الأرقام إلى سلسلة مشفرة (hex تدور)
        encrypted_parts = []
        for i, num in enumerate(nums):
            rotated = ((num << (i % 16)) | (num >> (16 - (i %16)))) & 0xFFFF
            encrypted_parts.append(f"{rotated:04x}")

        return ''.join(encrypted_parts)

    @staticmethod
    def complex_text_number_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")

        key_sum = sum(ord(c) for c in key)
        n = len(ciphertext)
        nums = []
        for i in range(0, n, 4):
            part = ciphertext[i:i+4]
            num = int(part, 16)
            rotated_back = ((num >> (i//4 % 16)) | (num << (16 - (i//4 %16)))) & 0xFFFF
            nums.append(rotated_back)

        # عكس العمليات الحسابية
        decrypted_nums = []
        for i, num in enumerate(nums):
            # معكوسة modulo لجمعية الثانية غير مباشرة معقدة
            # هنا لتسهيل نستخدم تقريب بالتقسيم (تحتاج تحسين في نظام حقيقي)
            val = (num - i*i) * pow(key_sum, -1, 9973) if key_sum != 0 else num
            val = val % 9973
            decrypted_nums.append(val)

        chars = [chr(n % 256) for n in decrypted_nums]
        intermediate_text = ''.join(chars)
        decrypted_text = UltraUtils.polyalphabetic_progressive_decrypt(intermediate_text, key)
        return decrypted_text


