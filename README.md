# PQC_DS

A flexible benchmarking and analysis framework for Post-Quantum Cryptography Digital Signatures, developed as part of the MSc thesis  
**“Analysis and Testing of Post Quantum Algorithms for Digital Signatures”**.

---
⚠️ Warning: all the functionalities of the tool have been implemented across several iterations, either in separate branches or previous commits. In the next update, all of them will be shown in the main branch, providing a more easy to use version of the framework. Thank you for your patience :)

---

## 🚀 Features

- **Modular testing harness** for multiple PQC signature schemes (CRYSTALS-Dilithium, Falcon, SPHINCS+)
- **Operation benchmarking** of some of the main subroutines of the different signature schemes
- **Automated measurement** of key-generation, signing, and verification performance
- **Statistical error analysis** and visualization (plots & CSV output)
- **Docker-based isolation** for reproducible environments
- **Extensible directory structure** add new schemes or test cases with minor changes

---

## 📦 Prerequisites

Before running the framework, ensure your system has:

- **Docker** (for containerized builds & execution)  
- **Python 3.8+**  
  - Packages:  
    - `matplotlib`  
    - `pandas`

---

## 🔧 Quick Start

1. Clone the repo
   ```bash
   git clone https://github.com/your-username/PQC_DS.git
   cd PQC_DS
   ```
2. Run the main launcher
   ```bash
   ./main.sh
   ```
   - You’ll be prompted to select which algorithm/framework to benchmark
   - For Falcon tests, switch to the falcon_ntru branch first
4. View your results
   - Each solution’s directory contains a *results/* folder with:
     - CSV tables of raw timing data
     - PNG plots summarizing performance



  

