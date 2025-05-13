# 📡 Morse Pro

**Encode and decode Morse code messages easily from Python or the command line.**

---

## 🔧 Installation

```bash
pip3 install morse_pro
````

---

## 🚀 Usage

### Depuis Python :

```python
from morse.encoder import encode_to_morse
from morse.decoder import decode_from_morse

# Encode text to Morse code
print(encode_to_morse("hello"))  # Output: .... . .-.. .-.. ---

# Decode Morse code to text
print(decode_from_morse(".... . .-.. .-.. ---"))  # Output: hello
```

### Depuis la ligne de commande (CLI) :

```bash
# Encode text to Morse code
morse_pro encode "hello"  # Output: .... . .-.. .-.. ---

# Decode Morse code to text
morse_pro decode ".... . .-.. .-.. ---"  # Output: hello
```

---

## 📦 Fonctionnalités

* 🔄 **Encoder du texte en code Morse**
* 🔄 **Décoder le code Morse en texte**
* 🖥️ **Support CLI** pour une utilisation facile depuis le terminal

---

## 📂 Structure du projet

```
Day82__Morse_Pro/
├── morse/
│   ├── __init__.py
│   ├── encoder.py
│   ├── decoder.py
│   ├── morse.py
│   └── py.typed
├── cli.py
├── tests/
│   ├── test_encoder.py
│   └── test_decoder.py
├── LICENSE
├── README.md
├── setup.py
└── pyproject.toml
```

---

## 🧑‍💻 Auteur

**Chrstphr CHEVALIER**
[GitHub Profile](https://github.com/ChrstphrChevalier)

```

### Explications :

1. **Structure uniforme** : Tout est dans un seul bloc markdown pour une meilleure lisibilité et cohérence.
2. **Hiérarchisation claire** : Chaque section a un titre distinct et les sous-sections sont clairement différenciées avec des niveaux de titres (`#`, `##`, `###`).
3. **Séparation claire des sections** : Les sections sont bien espacées, facilitant la navigation rapide dans le README. 
4. **Explication dans le code** : Les exemples sont commentés pour expliquer leur fonctionnement. 
```
