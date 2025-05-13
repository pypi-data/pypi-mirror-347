# 📡 Morse Pro - Encodeur et Décodeur de Code Morse

### <p align="center"> #Day82 </p>

### Aperçu

**Morse Pro** est une bibliothèque Python et une application en ligne de commande permettant d'encoder et de décoder des messages en code Morse de manière simple et rapide. Que ce soit pour des applications de communication, des projets éducatifs, ou simplement pour découvrir le code Morse, **Morse Pro** fournit une solution pratique à travers Python ou directement depuis le terminal.

Ce projet comprend :
- Une **fonctionnalité d'encodage** pour convertir du texte en code Morse.
- Une **fonctionnalité de décodage** pour convertir du code Morse en texte lisible.
- Une **interface en ligne de commande (CLI)** pour une utilisation facile depuis le terminal.

### Compétences acquises
- **Programmation Python** : Développement d'un module Python structuré avec gestion de fichiers et modules.
- **Traitement de texte** : Manipulation de chaînes de caractères pour convertir entre texte et code Morse.
- **Développement de CLI** : Création d'une interface en ligne de commande pour une utilisation rapide.
- **Tests unitaires** : Mise en place de tests pour assurer la fiabilité du code (avec `unittest` ou `pytest`).
- **Packaging et distribution** : Création d'une bibliothèque Python publiée sur PyPI.

### Partie obligatoire
- **Encodage du texte** : Conversion du texte en une chaîne de code Morse, caractère par caractère.
- **Décodage du Morse** : Retour du code Morse à son texte d'origine, gestion des erreurs de formatage.
- **Tests** : Tests unitaires pour s'assurer que les fonctions d'encodage et de décodage fonctionnent correctement.

### Pourquoi ce projet est pertinent

**Morse Pro** est une démonstration idéale de l'application d'une logique simple à un problème pratique, tout en offrant une extension vers un projet plus complexe de programmation Python. Ce projet combine des aspects fondamentaux du développement logiciel, comme la gestion de modules et la gestion des erreurs, ce qui en fait un excellent outil d'apprentissage.

En plus d'être utile dans un contexte pédagogique, ce projet peut être intégré dans divers systèmes de communication ou applications nécessitant une interface texte simplifiée. La gestion du code Morse, bien que vieille, reste un concept fondamental dans l'histoire des communications.

---

## 🔧 Installation

Pour installer **Morse Pro**, vous pouvez utiliser `pip` directement depuis PyPI :

```bash
pip3 install morse_pro
````

---

## 🚀 Usage

### Depuis Python :

```python
from morse.encoder import encode_to_morse
from morse.decoder import decode_from_morse

# Encoder du texte en code Morse
print(encode_to_morse("hello"))  # Sortie : .... . .-.. .-.. ---

# Décoder du code Morse en texte
print(decode_from_morse(".... . .-.. .-.. ---"))  # Sortie : hello
```

---

## 📦 Fonctionnalités

* 🔄 **Encodage de texte en code Morse** : Convertissez n'importe quel texte en une séquence Morse.
* 🔄 **Décodage du code Morse en texte** : Récupérez facilement un texte à partir de sa version Morse.
* 📦 **Package PyPI** : Installation rapide avec `pip` pour une intégration dans vos projets.

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
├── tests/
│   ├── test_encoder.py
│   └── test_decoder.py
├── LICENSE
├── README.md
├── setup.py
└── pyproject.toml
```
