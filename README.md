# Organização de eventos: 

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