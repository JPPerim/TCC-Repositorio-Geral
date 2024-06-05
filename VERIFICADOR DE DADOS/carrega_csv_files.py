import os
import pandas as pd

# Configuração padrão para leitura de CSVs sem cabeçalhos
CSV_READ_OPTIONS = {
    'header': None,
    'encoding': 'utf-8'
}

def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

def load_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, **CSV_READ_OPTIONS)
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo {file_path}: {e}")
    return df

def process_base_file(base_directory='DADO_BASE'):
    base_files = list_csv_files(base_directory)
    if len(base_files) != 1:
        raise Exception(f"Esperava um único arquivo na pasta base, mas encontrei {len(base_files)} arquivos.")
    base_file = base_files[0]
    return load_csv_file(base_file)

def process_test_files(test_directory='DADO_TESTE'):
    test_files = list_csv_files(test_directory)
    df_tests = [[load_csv_file(test_file) for test_file in test_files],[test_files]]
    return df_tests

if __name__ == "__main__":
    df_base = process_base_file()
    df_tests = process_test_files()
    
    print(f"DataFrame base:\n{df_base.head()}")
    for i, df_test in enumerate(df_tests):
        print(f"DataFrame de teste {i+1}:\n{df_test.head()}")
