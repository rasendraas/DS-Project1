# Setup Environment untuk Proyek Analisis Data 1
## 1. Buat Environment Baru
```bash
conda create --name proyek_analisis_data_1 python=3.11
```

## 2. Aktivasi Environment
```bash
conda activate proyek_analisis_data_1
```

## 3. Install Library
```bash
conda install pandas
conda install numpy
conda install matplotlib
conda install seaborn
conda install scikit-learn
pip install streamlit
pip install streamlit-option-menu
```

## 4. Generate `requirements.txt`
```bash
pip3 freeze > "requirements.txt"
```

## 5. Run `Dashboard`
```bash
streamlit run dashboard.py
```