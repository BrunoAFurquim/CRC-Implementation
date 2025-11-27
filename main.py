"""@author: Bruno Augusto Furquim"""

import struct

class CRC32Calculator:
    # Polinômio padrão usado em Ethernet (0x04C11DB7)
    POLYNOMIAL = 0x04C11DB7
    INITIAL_VALUE = 0xFFFFFFFF
    FINAL_XOR = 0xFFFFFFFF
    
    def __init__(self):
        self.crc_table = self._generate_crc_table()
    
    def _generate_crc_table(self):
        """Gera tabela de lookup para cálculo rápido de CRC."""
        table = []
        
        for i in range(256):
            crc = i << 24
            for _ in range(8):
                if crc & 0x80000000:
                    crc = (crc << 1) ^ self.POLYNOMIAL
                else:
                    crc = crc << 1
                crc &= 0xFFFFFFFF
            table.append(crc)
        return table
    
    def _calculate_crc_direct(self, data):
        """
        Calcula CRC-32 de forma direta (bit-a-bit).
        """
        crc = self.INITIAL_VALUE
        for byte in data:
            crc ^= byte << 24
            
            for _ in range(8):
                if crc & 0x80000000:
                    crc = (crc << 1) ^ self.POLYNOMIAL
                else:
                    crc = crc << 1
                crc &= 0xFFFFFFFF
        return crc ^ self.FINAL_XOR
    
    def _calculate_crc_table(self, data):
        """
        Calcula CRC-32 usando tabela de lookup (otimizado).
        """
        crc = self.INITIAL_VALUE
        for byte in data:
            table_index = (crc >> 24) ^ byte
            crc = ((crc << 8) ^ self.crc_table[table_index]) & 0xFFFFFFFF
        return crc ^ self.FINAL_XOR
    
    def calculate_crc(self, data, use_table=True):
        """
        Calcula o CRC-32 dos dados fornecidos.
        Args:
            data: bytes a serem processados
            use_table: Se True, usa tabela de lookup (mais rápido)
        Returns:
            int: Valor do CRC-32 calculado
        """
        if use_table:
            return self._calculate_crc_table(data)
        else:
            return self._calculate_crc_direct(data)
    
    def calculate_fcs(self, data):
        """
        Calcula o FCS (Frame Check Sequence) = complemento de 1 do CRC.
        Em Ethernet, o FCS é enviado como complemento de 1 do CRC.
        Args:
            data: bytes a serem processados
        Returns:
            tuple: (CRC calculado, FCS = complemento de 1)
        """
        crc = self.calculate_crc(data)
        fcs = crc ^ 0xFFFFFFFF  # Complemento de 1
        return crc, fcs
    
    def validate_frame(self, data, received_fcs):
        """
        Valida a integridade de um quadro recebido.
        Args:
            data: dados recebidos
            received_fcs: valor do FCS recebido
        Returns:
            tuple: (is_valid, calculated_crc, calculated_fcs)
        """
        calculated_crc, calculated_fcs = self.calculate_fcs(data)
        is_valid = calculated_fcs == received_fcs
        return is_valid, calculated_crc, calculated_fcs


def input_data_source():
    """
    Solicita ao usuário a fonte de dados (hexadecimal ou ASCII).
    Returns:
        bytes: Dados convertidos para bytes
    """
    print("\n" + "="*60)
    print("ENTRADA DE DADOS")
    print("="*60)
    print("1. Inserir dados em hexadecimal")
    print("2. Inserir dados em texto ASCII")
    choice = input("\nEscolha (1 ou 2): ").strip()
    if choice == "1":
        hex_input = input("Digite os dados em hexadecimal (ex: 48656C6C6F): ").strip()
        try:
            data = bytes.fromhex(hex_input)
            print(f"✓ Dados convertidos: {data}")
            return data
        except ValueError:
            print("✗ Erro: Formato hexadecimal inválido!")
            return None
    elif choice == "2":
        text_input = input("Digite os dados em texto ASCII: ")
        data = text_input.encode('ascii')
        print(f"✓ Dados convertidos: {data}")
        return data
    else:
        print("✗ Escolha inválida!")
        return None

def display_crc_calculation(data, crc, fcs):
    """
    Exibe os resultados do cálculo de CRC de forma formatada.    
    Args:
        data: dados processados
        crc: valor do CRC-32 calculado
        fcs: valor do FCS calculado
    """
    print("\n" + "="*60)
    print("RESULTADO DO CÁLCULO CRC-32")
    print("="*60)
    print(f"Dados originais (hex):     {data.hex().upper()}")
    print(f"Dados originais (ASCII):   {data.decode('ascii', errors='replace')}")
    print(f"Tamanho dos dados:         {len(data)} bytes")
    print("\n" + "-"*60)
    print(f"CRC-32 Calculado:          0x{crc:08X}")
    print(f"CRC-32 Calculado (dec):    {crc}")
    print("\n" + "-"*60)
    print(f"FCS (Complemento):         0x{fcs:08X}")
    print(f"FCS (Complemento, dec):    {fcs}")
    print("="*60)

def validate_frame_interactive(calculator):
    """
    Executa a validação de quadro recebido.
    Args:
        calculator: Instância de CRC32Calculator
    """
    print("\n" + "="*60)
    print("VALIDAÇÃO DE INTEGRIDADE (RECEPTOR)")
    print("="*60)
    # Solicitar dados
    hex_input = input("Digite os dados recebidos em hexadecimal: ").strip()
    try:
        data = bytes.fromhex(hex_input)
    except ValueError:
        print("✗ Erro: Formato hexadecimal inválido!")
        return
    # Solicitar FCS recebido
    fcs_input = input("Digite o FCS recebido em hexadecimal (ex: ABCD1234): ").strip()
    try:
        received_fcs = int(fcs_input, 16)
    except ValueError:
        print("✗ Erro: FCS inválido!")
        return
    # Validar
    is_valid, calculated_crc, calculated_fcs = calculator.validate_frame(data, received_fcs)
    print("\n" + "-"*60)
    print("RESULTADO DA VALIDAÇÃO")
    print("-"*60)
    print(f"Dados recebidos (hex):     {data.hex().upper()}")
    print(f"Tamanho dos dados:         {len(data)} bytes")
    print(f"\nFCS Recebido:              0x{received_fcs:08X}")
    print(f"FCS Calculado:             0x{calculated_fcs:08X}")
    print(f"CRC-32 Calculado:          0x{calculated_crc:08X}")
    print("\n" + "="*60)
    if is_valid:
        print("✓ QUADRO VÁLIDO - Sem erros de transmissão detectados!")
    else:
        print("✗ QUADRO CORROMPIDO - Erro de transmissão detectado!")
    
    print("="*60)

def menu_principal():
    """Menu principal do programa."""
    calculator = CRC32Calculator()
    while True:
        print("\n" + "="*60)
        print("CALCULADORA CRC-32 PARA REDES ETHERNET")
        print("="*60)
        print("1. Calcular CRC-32 e FCS de dados")
        print("2. Validar integridade de quadro recebido")
        print("3. Exemplo de demonstração")
        print("4. Sair")
        print("="*60)
        choice = input("Escolha uma opção (1-4): ").strip()
        if choice == "1":
            data = input_data_source()
            if data is not None:
                crc, fcs = calculator.calculate_fcs(data)
                display_crc_calculation(data, crc, fcs)
        elif choice == "2":
            validate_frame_interactive(calculator)
        elif choice == "3":
            print("\n" + "="*60)
            print("EXEMPLO DE DEMONSTRAÇÃO")
            print("="*60)

            # Exemplo 1: Dados simples
            example1_data = b"HELLO"
            crc1, fcs1 = calculator.calculate_fcs(example1_data)
            print("\nExemplo 1: Mensagem 'HELLO'")
            display_crc_calculation(example1_data, crc1, fcs1)
            
            # Exemplo 2: Dados em hexadecimal
            example2_data = bytes.fromhex("48656C6C6F20576F726C64")
            crc2, fcs2 = calculator.calculate_fcs(example2_data)
            print("\nExemplo 2: Mensagem 'Hello World'")
            display_crc_calculation(example2_data, crc2, fcs2)
            
            # Exemplo 3: Validação com dados corretos
            print("\n" + "="*60)
            print("Exemplo 3: Validação de quadro correto")
            print("="*60)
            is_valid, calc_crc, calc_fcs = calculator.validate_frame(example1_data, fcs1)
            print(f"Dados: {example1_data}")
            print(f"FCS Recebido: 0x{fcs1:08X}")
            print(f"FCS Calculado: 0x{calc_fcs:08X}")
            print(f"Resultado: {'✓ VÁLIDO' if is_valid else '✗ INVÁLIDO'}")
            
            # Exemplo 4: Validação com dados corrompidos
            print("\n" + "="*60)
            print("Exemplo 4: Validação de quadro corrompido")
            print("="*60)
            corrupted_fcs = fcs1 ^ 0x00000001  # Simula erro de 1 bit
            is_valid, calc_crc, calc_fcs = calculator.validate_frame(example1_data, corrupted_fcs)
            print(f"Dados: {example1_data}")
            print(f"FCS Recebido: 0x{corrupted_fcs:08X}")
            print(f"FCS Calculado: 0x{calc_fcs:08X}")
            print(f"Resultado: {'✓ VÁLIDO' if is_valid else '✗ INVÁLIDO'}")
        
        elif choice == "4":
            print("\n✓ Programa encerrado. Até logo!")
            break
        else:
            print("✗ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()
