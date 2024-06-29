#versão 1 - métodos: saque(max 3x e <= 500), depósito , extrato
#versão 2 - separar em funções (s, d, e) e criar 2 funções: cadastrar_usuario(cliente) e cadastrar_conta_bancaria

def cadastrar_cliente():
    global registro_clientes
    
    for cliente in registro_clientes:
        if cliente[2] == cpf:  # Verifica se o CPF já está cadastrado
            print(f"\n[Falha Sistêmica]: O CPF {cpf} já está cadastrado no sistema.")
            return None

    nome = input("Nome: ")
    dt_nascimento = input("Data de Nascimento (DDMMAAAA): ")
    cpf = input("CPF (somente números): ")
    endereco = input("Endereço: ")

    # Validar se CPF já existe
    for cliente in registro_clientes:
        if cliente[2] == cpf:  # Verifica se o CPF já está cadastrado
            print(f"\n[Falha Sistêmica]: O CPF {cpf} já está cadastrado no sistema.")
            return None
    
    # Separar o estado do endereço
    endereco_split = endereco.split(' - ')
    cidade_estado = endereco_split[-1].split('/')

    cliente = [nome, dt_nascimento, cpf, endereco, []]  # Incluímos uma lista vazia para contas
    registro_clientes.append(cliente)

    print("\n[Sucesso]: Cliente cadastrado com sucesso!")


def buscar_cliente_por_cpf(cpf):
    global registro_clientes
    
    for cliente in registro_clientes:
        if cliente[2] == cpf:
            return cliente
    
    return None  # Retorna None se o cliente não for encontrado


def cadastrar_conta_bancaria(cpf):
    global registro_clientes

    cliente = buscar_cliente_por_cpf(cpf)

    if cliente:
        agencia = "0001"
        numero_conta = len(cliente[-1]) + 1  # Gera número de conta sequencial
        saldo_inicial = 0

        conta = {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'saldo': saldo_inicial,
            'extrato': []
        }

        cliente[-1].append(conta)  # Adiciona a conta à lista de contas do cliente

        print("\n-----Dados da Conta-----")
        print(f"Titular da Conta: {cliente[0]}")
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("\n------------------------")

        return conta
    else:
        print(f"\n[Falha Sistêmica]: O cliente com CPF {cpf} não está cadastrado no sistema.")


def depositar(cpf):
    global registro_clientes

    cliente = buscar_cliente_por_cpf(cpf)

    if cliente:
        numero_conta = int(input("Digite o número da conta: "))
        conta = None

        # Procura a conta específica do cliente
        for c in cliente[-1]:
            if c['numero_conta'] == numero_conta:
                conta = c
                break

        if conta:
            deposito = float(input("Insira o valor do depósito: "))
            if deposito > 0:
                conta['saldo'] += deposito
                conta['extrato'].append(f"Depósito: R$ {deposito:.2f}")
                print(f"\nSaldo após depósito: R$ {conta['saldo']:.2f}")
            else:
                print(f"\n[Falha Operação]: o valor informado é inválido. Tente novamente.")
        else:
            print(f"\n[Falha Sistêmica]: Não foi encontrada a conta número {numero_conta} para o cliente com CPF {cpf}.")
    else:
        print(f"\n[Falha Sistêmica]: O cliente com CPF {cpf} não está cadastrado no sistema.")


def sacar(cpf):
    global registro_clientes

    cliente = buscar_cliente_por_cpf(cpf)

    if cliente:
        numero_conta = int(input("Digite o número da conta: "))
        conta = None

        # Procura a conta específica do cliente
        for c in cliente[-1]:
            if c['numero_conta'] == numero_conta:
                conta = c
                break

        if conta:
            limite_saque = 500
            LIMITE_SAQUE = 3

            if len(conta['extrato']) >= LIMITE_SAQUE:
                print(f"\n[Falha Operação]: você excedeu o seu limite de {LIMITE_SAQUE} saques.")
                return

            saque = float(input("Insira o valor do saque: "))

            if saque <= 0:
                print("\n[Falha Operação]: o valor informado é inválido. Tente novamente.")
                return

            if saque > conta['saldo']:
                print(f"\n[Falha Operação]: o valor solicitado ({saque:.2f}) excede o seu saldo de R$ {conta['saldo']:.2f}")
                return

            if saque > limite_saque:
                print(f"\n[Falha Operação]: você ultrapassou o limite de saque de R$ {limite_saque:.2f}")
                return

            conta['saldo'] -= saque
            conta['extrato'].append(f"Saque: R$ {saque:.2f}")
            print(f"\nSaldo após saque: R$ {conta['saldo']:.2f}")

        else:
            print(f"\n[Falha Sistêmica]: Não foi encontrada a conta número {numero_conta} para o cliente com CPF {cpf}.")
    else:
        print(f"\n[Falha Sistêmica]: O cliente com CPF {cpf} não está cadastrado no sistema.")


def extrato_bancario(cpf):
    global registro_clientes

    cliente = buscar_cliente_por_cpf(cpf)

    if cliente:
        numero_conta = int(input("Digite o número da conta: "))
        conta = None

        # Procura a conta específica do cliente
        for c in cliente[-1]:
            if c['numero_conta'] == numero_conta:
                conta = c
                break

        if conta:
            print(f"--------------EXTRATO BANCÁRIO DE {cliente[0]}--------------")

            if not conta['extrato']:
                print(f"[Atenção]: nenhuma movimentação foi efetuada até o momento.")
            else:
                for movimentacao in conta['extrato']:
                    print(movimentacao)
        else:
            print(f"\n[Falha Sistêmica]: Não foi encontrada a conta número {numero_conta} para o cliente com CPF {cpf}.")
    else:
        print(f"\n[Falha Sistêmica]: O cliente com CPF {cpf} não está cadastrado no sistema.")


registro_clientes = []

menu = """
    [1] Cadastrar Cliente
    [2] Cadastrar Conta
    [3] Depósito
    [4] Saque 
    [5] Extrato
    [0] Sair
"""

while True:
    print(menu)
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_cliente()
    
    elif opcao == "2":
        cpf = input("Digite o CPF do cliente: ")
        cadastrar_conta_bancaria(cpf)
    
    elif opcao == "3":
        cpf = input("Digite o CPF do cliente: ")
        depositar(cpf)
    
    elif opcao == "4":
        cpf = input("Digite o CPF do cliente: ")
        sacar(cpf)

    elif opcao == "5":
        cpf = input("Digite o CPF do cliente: ")
        extrato_bancario(cpf)
    
    elif opcao == "0":
        print(f"\nFinalizando operação...")
        break

    else:
        print(f"\nOpção inválida. Escolha uma opção válida do menu.")
