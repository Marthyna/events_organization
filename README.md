## Organização de eventos: 

Estrutura dos arquivos do projeto:
```
/events_organization/
├── README.md
├── formulation/
│   ├── executar_todas.sh
│   ├── execution_log.txt
│   ├── formulation.jl
├── inf05010_2024-2_B_TP_instances_organizacao-de-eventos/
│   ├── 01.txt
│   ├── 02.txt
│   │   ...
│   └── 10.txt
└── metaheuristic/
    └── iterated_local_search.py
```

## Execução da formulação inteira:
Na pasta `formulation`:
- rodar o script `executar_todas.sh` para a execução de todas as instâncias do problema encontradas na pasta `inf05010_2024-2_B_TP_instances_organizacao-de-eventos/`, usando sementes de aleatoriedade de 1 a 10, rodando por 5 segundos e 5 minutos, 
- ou `julia formulation.jl <nome do arquivo> <semente> <tempo em segundos>` para execução de um arquivo, semente de aleatoriedade e tempo específicos.

## Execução da Meta-heurística
Na pasta `metaheuristic`: 
#### **Parâmetros**
- **Parâmetros obrigatórios**:
  - `file_path`: Caminho para o arquivo de entrada com a instância do problema.
  - `seed`: Semente aleatória para garantir reprodutibilidade.
  - `--termination-criterion`: Critério de parada, podendo ser:
    - `iterations`: Número máximo de iterações.
    - `time`: Tempo máximo de execução (em segundos).
- **Parâmetros opcionais**:
  - `--max-iterations`: Número máximo de iterações (obrigatório se o critério de parada for `iterations`).
  - `--max-time`: Tempo máximo de execução em segundos (obrigatório se o critério de parada for `time`).
- Template:
  ```bash
  python3 iterated_local_search.py <nome do arquivo com caminho> <semente> --termination-criterion <criterio de parada> <--max-iterations ou --max-time> <número máximo de iterações ou tempo>

#### **Exemplo de Execução**
1. Critério de iterações:
   ```bash
   python3 iterated_local_search.py instance.txt 2 --termination-criterion iterations --max-iterations 1000
2. Critério de tempo:
   ```bash
   python3 iterated_local_search.py instance.txt 2 --termination-criterion time --max-time 5