# simulated-annealing-escalonamento

Reimplementação em Python do método da minha dissertação de mestrado para o problema de **máquinas paralelas idênticas com datas de liberação e tempos de setup**, **Pm | r_j, s_j | Cmax**, resolvido com **Simulated Annealing**.

> Dissertação: MESQUITA, F. N. *Meta-heurística baseada em Simulated Annealing para programação da produção em máquinas paralelas com diferentes datas de liberação e tempos de setup*. Mestrado Profissional em Gestão Organizacional, Universidade Federal de Goiás (Regional Catalão), 2015.
>
> O código deste repositório foi reescrito agora, de forma independente, a partir do método descrito no texto. As instâncias são **sintéticas**, geradas aleatoriamente. Não é o software original da dissertação (que foi feito em Delphi), e os números abaixo não reproduzem os da dissertação.

## O problema

- m máquinas idênticas; cada tarefa j tem tempo de processamento p_j, setup s_j (independente da sequência) e data de liberação r_j.
- O setup pode ser **antecipado**: começa assim que a máquina fica livre, mas o processamento só começa depois de r_j. Assim, o fim da tarefa é max(fim anterior + s_j, r_j) + p_j.
- Objetivo: minimizar o makespan, Cmax = max C_j.

## O que está implementado

| Componente | Arquivo / função |
|---|---|
| Solução inicial: ordenar por r_j/(p_j+s_j) crescente e alocar na máquina de menor carga | `initial_solution` |
| Seis esquemas de perturbação: PS1 troca adjacente, PS2 troca aleatória, PS3 reinserção (intramáquina); PS4 troca, PS5 realocação, PS6 realocação de subsequência (intermáquinas) | `ps1` a `ps6` |
| Simulated Annealing (parâmetros padrão do exemplo da dissertação: Ti = 60, Tf = 0,01, r = 0,85) | `simulated_annealing` |
| Etapa de melhoria final (balanceamento de cargas) | `balance_step` |
| Quatro limitantes inferiores (LB1 a LB4) e o desvio relativo percentual (RPD) | `lower_bounds`, `rpd` |
| Gerador de instâncias (p ~ U(1,99), s ~ U(1,49), r em U(1,49), U(1,99) ou U(50,149)) | `random_instance` |

## Como executar

```bash
pip install -r requirements.txt
pytest                 # 13 testes
python experiment.py   # compara os esquemas PS1-PS6 com a solução inicial
```

Uso rápido:

```python
from sa_scheduling import random_instance, simulated_annealing, lower_bounds, rpd

p, s, r = random_instance(30, (1, 99), seed=1)
sol, cmax = simulated_annealing(p, s, r, m=3, ps="PS4")
print(cmax, rpd(cmax, lower_bounds(p, s, r, 3)["LB"]))
```

## Resultado do experimento incluído

```text
180 instâncias (n em {10, 30, 100}, m em {2, 5}, 3 faixas de r, 10 por classe)
método  RPD médio vs LB (%)
SI        5.10
PS1       4.81
PS2       4.82
PS3       4.87
PS4       4.11
PS5       4.71
PS6       5.10
```

O esquema **PS4** (troca de tarefas entre máquinas) foi o melhor, e PS1 e PS6 os mais fracos. É a mesma ordem qualitativa que observei na dissertação, mas com outras instâncias e outro tamanho de amostra, então as magnitudes não são comparáveis.

## Limitações

- O experimento é pequeno: 180 instâncias (a dissertação usou 720, com mais valores de n e m) e uma única semente por instância.
- Com os parâmetros padrão, o SA faz poucas iterações (cerca de 53 resfriamentos). Aumentar `iters_per_temp` ou o fator de resfriamento melhora a busca, mas muda o método original.
- O LB4 usa os tempos de processamento ordenados em ordem decrescente. A dissertação define o limitante pela regra LPT, e a ordenação adotada aqui é uma interpretação minha.
- Não há análise estatística (ANOVA) nem comparação com solver exato.

## Autora

Fernanda Neiva Mesquita. [Lattes](https://lattes.cnpq.br/3639678638834402)
# simulated-annealing-escalonamento
Simulated Annealing para escalonamento em máquinas paralelas (P||Cmax), comparado com LPT e limite inferior; com testes
