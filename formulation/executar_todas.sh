#!/bin/bash

INSTANCE_DIR="../inf05010_2024-2_B_TP_instances_organizacao-de-eventos"
LOG_FILE="execution_log.txt"

echo "Nome | seed | Sf5 | Sf300 | Uf5 | Uf300 | FT5 | FT300 " > "$LOG_FILE"

for instance in "$INSTANCE_DIR"/*.txt; do
    # iterar seed de 1 a 10
    for seed in {1..10}; do
        filename=$(basename "$instance")

        result_5s=$(julia formulation.jl "$instance" "$seed" 5)
        bkv_5s=$(echo "$result_5s" | grep "Melhor solução encontrada" | awk '{print $4}')
        lim_sup_5s=$(echo "$result_5s" | grep "Limite superior" | awk '{print $3}')
        tempo_5s=$(echo "$result_5s" | grep "Tempo de execução" | awk '{print $4}')

        result_300s=$(julia formulation.jl "$instance" "$seed" 300)
        bkv_300s=$(echo "$result_300s" | grep "Melhor solução encontrada" | awk '{print $4}')
        lim_sup_300s=$(echo "$result_300s" | grep "Limite superior" | awk '{print $3}')
        tempo_300s=$(echo "$result_300s" | grep "Tempo de execução" | awk '{print $4}')

        # Tratamento para valores ausentes
        bkv_5s=${bkv_5s:-N/A}
        lim_sup_5s=${lim_sup_5s:-N/A}
        tempo_5s=${tempo_5s:-N/A}
        bkv_300s=${bkv_300s:-N/A}
        lim_sup_300s=${lim_sup_300s:-N/A}
        tempo_300s=${tempo_300s:-N/A}

        # Exibe resultados no terminal
        echo "Instance: $filename | Seed: $seed"
        echo "Melhor solução encontrada 5s: $bkv_5s"
        echo "Melhor solução encontrada 300s: $bkv_300s"
        echo "Limite superior 5s: $lim_sup_5s"
        echo "Limite superior 300s: $lim_sup_300s"
        echo "Tempo de execução 5s: $tempo_5s"
        echo "Tempo de execução 300s: $tempo_300s"

        echo "$filename | $seed | $bkv_5s | $bkv_300s | $lim_sup_5s | $lim_sup_300s | $tempo_5s | $tempo_300s" >> "$LOG_FILE"
    done
done
