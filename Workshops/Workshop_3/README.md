# Workshop 3 — Kaggle Systems Simulation: 20 Questions

This repository contains the full implementation and analysis for Workshop 3 of the Systems Analysis and Design course at Universidad Distrital Francisco José de Caldas. The project is based on the Kaggle competition “LLM 20 Questions Games”.

## 📌 Objective

To simulate a simplified version of the “20 Questions” game system using real Kaggle data, following the architecture designed in Workshop 2. The simulation explores how different bot strategies behave in various controlled scenarios and evaluates the internal logic of the system.

## 🧩 Project Structure

- `data_loader.py`: Loads datasets with robust strategies to handle formatting issues. Implements the “Data Source” module.
- `game_engine.py`: Manages game flow, rules, and validation. Implements the “Game Logic Controller”.
- `scoring.py`: Updates bot skills using a μ–σ model. Implements the “Skill Evaluation System”.
- `matchmaking.py`: Matches bots with similar skills to ensure fairness. Implements the “Matchmaking System”.
- `analysis.py`: Generates metrics and plots to analyze behavior and detect patterns.
- `simulation.py`: Orchestrates all components and executes defined scenarios.
- `main.py`: Coordinates the simulation pipeline from data loading to result analysis.

## 🧪 Simulation Scenarios

Three distinct simulation scenarios were defined to test the architecture:

- **Balanced** — Standard settings, structured questions, 80% answer consistency.
- **Chaotic** — Random strategy, low consistency (50%), simulating noisy environments.
- **Skilled** — High-skill bots with advanced reasoning, 90% answer consistency.

## 🔍 Key Results

- The system showed stable behavior in all scenarios.
- The success rate exceeded 90% in every case, even in chaotic conditions.
- Skill evolution patterns revealed structural advantages for the questioner role.
- Some limitations were found in how well the scenarios differed in outcome.
- Correlation analysis confirmed expected relationships between key variables.

## ⚙️ Technologies Used

- Python 3.x  
- Jupyter Notebooks / Google Colab  
- pandas, numpy  
- matplotlib, seaborn  

## 🔗 Resources

- 📁 Dataset: [Kaggle - LLM 20 Questions Games](https://www.kaggle.com/datasets/waechter/llm-20-questions-games)
- 📓 Notebook: [Google Colab - Workshop 3 Simulation](https://colab.research.google.com/drive/1gwowtMPHHY238kZR7LUklmCinKeiQ8xS?usp=sharing)

## 👨‍💻 Authors

- Laura Daniela Muñoz Ipus — 20221020022  
- Luisa Fernanda Guerrero Ordoñez — 20212020099  
- Esteban Alexander Bautista Solano — 20221020089  

## 📚 References

1. Waechter, T. (2024). *LLM 20 Questions Games Dataset*. Kaggle.  
   https://www.kaggle.com/datasets/waechter/llm-20-questions-games  
2. Sierra, C. A. (2025). *Systems Analysis and Design – Course Materials*.  
   https://github.com/EngAndres/ud-public/tree/main/courses/systems-analysis  
3. Google Colab Notebook.  
   https://colab.research.google.com/drive/1gwowtMPHHY238kZR7LUklmCinKeiQ8xS?usp=sharing

