# CRC-Implementation

Implementação completa de CRC-32 para validação de integridade em redes Ethernet.

## 📋 Descrição

Este projeto implementa um calculador de CRC-32 (Cyclic Redundancy Check) que simula o processo de validação de integridade usado em redes Ethernet. O programa permite:

1. **Cálculo de CRC-32**: Converte dados (hexadecimal ou ASCII) em bytes e calcula o CRC-32
2. **Geração de FCS**: Calcula o Frame Check Sequence (complemento de 1 do CRC)
3. **Validação de Quadros**: Verifica se um quadro recebido está íntegro ou corrompido

## 🔧 Características

- ✅ Suporte para entrada em hexadecimal e texto ASCII
- ✅ Uso do polinômio padrão Ethernet (0x04C11DB7)
- ✅ Otimização com tabela de lookup para cálculos rápidos
- ✅ Algoritmo direto (bit-a-bit) disponível para fins educacionais
- ✅ Interface interativa com menu
- ✅ Exemplos práticos de demonstração
- ✅ Validação de integridade de quadros recebidos
- ✅ Detecção de erros de transmissão

## 📚 Fundamentos de CRC-32

### Polinômio Padrão
```
0x04C11DB7 (usado em Ethernet)
```

### Processo de Cálculo
1. Inicializa CRC com 0xFFFFFFFF
2. Para cada byte dos dados:
   - XOR do byte com os 8 bits mais significativos do CRC
   - Para cada bit: se MSB=1, XOR com polinômio; caso contrário, shift left
3. XOR final com 0xFFFFFFFF

### FCS (Frame Check Sequence)
```
FCS = CRC ^ 0xFFFFFFFF (complemento de 1)
```

Em Ethernet, o FCS é transmitido junto com os dados para validação no receptor.

## 🚀 Como Usar

### Executar o programa
```powershell
python main.py
```

### Menu Principal
O programa apresenta um menu com as seguintes opções:

1. **Calcular CRC-32 e FCS**: 
   - Insira dados em hexadecimal ou ASCII
   - O programa exibe o CRC-32 calculado e o FCS

2. **Validar integridade de quadro**:
   - Insira os dados recebidos
   - Insira o FCS recebido
   - O programa verifica se o quadro está íntegro

3. **Exemplo de demonstração**:
   - Executa 4 exemplos práticos com explicações

4. **Sair**: Encerra o programa

## 📝 Exemplos de Uso

### Exemplo 1: Calcular CRC de "HELLO"
```
Entrada: HELLO (ASCII)
CRC-32: 0x4A17B156
FCS: 0xB5E84EA9
```

### Exemplo 2: Validar quadro recebido
```
Dados recebidos (hex): 48656C6C6F
FCS recebido: 0xB5E84EA9
Resultado: ✓ QUADRO VÁLIDO
```

### Exemplo 3: Detectar quadro corrompido
```
Dados recebidos (hex): 48656C6C6F
FCS recebido: 0xB5E84EA8 (erro de 1 bit)
Resultado: ✗ QUADRO CORROMPIDO
```

## 🏗️ Estrutura do Código

### Classe `CRC32Calculator`
Responsável por todos os cálculos de CRC-32:

- `_generate_crc_table()`: Gera tabela de lookup
- `_calculate_crc_direct(data)`: Cálculo direto bit-a-bit
- `_calculate_crc_table(data)`: Cálculo otimizado com tabela
- `calculate_crc(data, use_table=True)`: Interface principal
- `calculate_fcs(data)`: Calcula CRC e FCS
- `validate_frame(data, received_fcs)`: Valida integridade

### Funções Auxiliares
- `input_data_source()`: Solicita e converte dados de entrada
- `display_crc_calculation()`: Exibe resultados formatados
- `validate_frame_interactive()`: Interface de validação
- `menu_principal()`: Loop principal do programa

## 📊 Detalhes Técnicos

### Constantes
| Parâmetro | Valor |
|-----------|-------|
| Polinômio | 0x04C11DB7 |
| Valor Inicial | 0xFFFFFFFF |
| XOR Final | 0xFFFFFFFF |
| Tamanho | 32 bits |

### Complexidade
- **Tempo**: O(n) onde n é o número de bytes
- **Espaço**: O(1) para algoritmo direto, O(256) para tabela de lookup
- **Otimização**: Tabela de lookup reduz iterações de 8x

## 🔐 Garantias de Integridade

O CRC-32 pode detectar:
- ✅ Erro de 1 bit
- ✅ Erro de 2 bits (na maioria dos casos)
- ✅ Qualquer número ímpar de erros
- ✅ Bursts de erro até 32 bits

## 🛠️ Tecnologias

- **Linguagem**: Python 3.x
- **Dependências**: Nenhuma (apenas biblioteca padrão)
- **Compatibilidade**: Windows, macOS, Linux

## 📖 Referências

- [Ethernet Frame Format](https://en.wikipedia.org/wiki/Ethernet_frame)
- [CRC Polynomial](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)
- [IEEE 802.3 Standard](https://standards.ieee.org/ieee/802.3/6935/)

## 👨‍💻 Autor

Implementação educacional de CRC-32 para redes Ethernet.

## 📄 Licença

Aberto para fins educacionais e comerciais.
