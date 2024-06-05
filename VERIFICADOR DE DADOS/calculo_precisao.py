import carrega_csv_files
import pandas as pd
import statistics
import datetime

def calcula_tempo_decorrido(all_times):
    all_times = sorted(all_times)
    
    start_time = min(all_times)
    end_time = max(all_times)
    total_time = end_time - start_time
    times_from_start = [item - start_time for item in all_times]
    deltas = [times_from_start[i] - times_from_start[i - 1] for i in range(1, len(times_from_start))]

    if any(delta < 0 for delta in deltas):
        print("Aviso: delta negativo encontrado!")
        deltas = [abs(delta) for delta in deltas]
    
    max_time = max(deltas)
    min_time = min(deltas)
    mean_time = statistics.mean(deltas)
    median_time = statistics.median(deltas)
    stdev_time = statistics.stdev(deltas)

    return {
        'total_time': total_time,
        'start_time': start_time,
        'end_time': end_time,
        'max_time': max_time,
        'min_time': min_time,
        'mean_time': mean_time,
        'median_time': median_time,
        'stdev_time': stdev_time,
        'deltas': deltas
    }

def converte_tempo_para_segundos(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6
    return total_seconds

def check_dataframe(origin_dataframe, test_dataframes):
    results = []
    files_dataframes = test_dataframes[1]
    print(files_dataframes)
    test_dataframes = test_dataframes[0]
    # Converte o DataFrame de origem para string para garantir comparações precisas
    origin_str = origin_dataframe.astype(str)
    for i, test_dataframe in enumerate(test_dataframes):
        # Ignorar a primeira coluna do DataFrame de teste
        test_str = test_dataframe.iloc[:, 1:].astype(str)

        # Verificar duplicatas e dados faltantes
        duplicated_test = test_str.duplicated().sum()
        missing_rows = abs(len(origin_str) - len(test_str))

        # Certificar-se de comparar até o menor número de linhas
        min_rows = min(len(origin_str), len(test_str))
        matching_rows = (origin_str.head(min_rows).values == test_str.head(min_rows).values).all(axis=1).sum()

        # Calcular precisão e taxa de erro
        total_rows_origin = len(origin_str)
        total_errors = missing_rows + duplicated_test
        error_rate = total_errors / total_rows_origin if total_rows_origin > 0 else 0
        precision = 1 - error_rate

        # Convertendo a primeira coluna para segundos
        time_data = test_dataframe.iloc[:, 0].apply(converte_tempo_para_segundos).tolist()
        time_metrics = calcula_tempo_decorrido(time_data)
        results.append({
            'test_file_index': i + 1,
            'file_name': files_dataframes[0][i],
            'precision': precision,
            'duplicated_rows': duplicated_test,
            'missing_rows': missing_rows,
            'error_rate': error_rate,
            'total_time': time_metrics['total_time'],
            'start_time': time_metrics['start_time'],
            'end_time': time_metrics['end_time'],
            'max_time': time_metrics['max_time'],
            'min_time': time_metrics['min_time'],
            'mean_time': time_metrics['mean_time'],
            'median_time': time_metrics['median_time'],
            'stdev_time': time_metrics['stdev_time'],
            'deltas': time_metrics['deltas']
        })

        # Salvando deltas em um arquivo CSV separado
        deltas_df = pd.DataFrame(time_metrics['deltas'], columns=['deltas'])
        deltas_df.to_csv(f'deltas_test_{(i + 1)}.csv', index=False)

    return results

if __name__ == '__main__':
    base_df = carrega_csv_files.process_base_file()
    test_dfs = carrega_csv_files.process_test_files()
    
    precision_results = check_dataframe(base_df, test_dfs)
    
    # Convertendo resultados para DataFrame do pandas
    results_df = pd.DataFrame(precision_results)
    
    # Remover a coluna 'deltas' antes de salvar o arquivo principal
    results_df.drop(columns=['deltas'], inplace=True)
    
    # Salvando DataFrame em um arquivo CSV
    results_df.to_csv('precision_results.csv', index=False)
    
    print("Resultados salvos em 'precision_results.csv'")
