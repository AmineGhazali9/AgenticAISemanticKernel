# Assistant – Gouvernance et politique

Ce projet implémente un assistant strategique interactif dédié au cadre de gouvernance, construit avec Streamlit et Azure AI Projects. Grâce à trois agents spécialisés — recherche documentaire, recherche web et synthèse — l'application permet de répondre de manière contextualisée et structurée aux questions liées aux politiques internes de télétravail.

---

## Introduction

**Démo : Assistant en gouvernance intelligent**

Ce code implémente une application Streamlit qui utilise plusieurs agents IA pour analyser la charte RH de Cofomo et proposer des recommandations sur le télétravail.

L’application combine :

- **Analyse de documents internes**  
  Extraction des informations clés des politiques de gouvernance.
- **Recherche de tendances marché**  
  Identification des meilleures pratiques et innovations en gouvernance.
- **Synthèse et recommandations concrètes**  
  Guidance pour les décisions des équipes RH et des managers.

Le tout est piloté via une interface web simple et interactive développée avec Streamlit.

---

## Getting Started

### Prérequis

- **Python 3.9+** installé sur votre machine.  
- **Compte Azure** avec la ressource AI Projects configurée.  
- **Clé et chaîne de connexion** Azure AI Projects (ENV: `AZURE_AI_PROJECT_CONNECTION_STRING`).

### Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://votre-repo/assistant-rh-teletravail.git
   cd assistant-rh-teletravail
   ```

2. **Créer et activer** un environnement virtuel  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Installer** les dépendances  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Configuration

1. **Fichier `.env`**  
   Créez un fichier `.env` à la racine du projet et ajoutez-y :  
   ```ini
   AZURE_AI_PROJECT_CONNECTION_STRING="<Votre chaîne de connexion Azure AI Projects>"
   ```
2. **Identifiants des agents**  
   Ouvrez `AssistantRH.py` et remplacez les constantes `AGENT1_ID`, `AGENT2_ID` et `AGENT3_ID` par les identifiants de vos agents Azure AI.

---

## Build and Test

### Lancement de l’application

Exécutez la commande suivante pour démarrer l’interface Streamlit :  
```bash
streamlit run AssistantRH.py
```  
L’application sera disponible par défaut sur http://localhost:8501 .
