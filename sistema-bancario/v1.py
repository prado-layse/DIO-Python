#versão 1 - métodos: saque(max 3x e <= 500), depósito , extrato

menu = f"""
    [d] Depósito
    [e] Extrato 
    [s] Saque
    [0] Sair
"""

saldo = 0
limite_saque = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = (float(input("Insira o valor do depósito: ")))

        if(deposito > 0):
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
            print(f"saldo: {saldo}")
        else:
            print(f"[Falha Operação]: o valor informado é inválido. Tente novamente.")
        
    elif opcao == "s":
        saque = (float(input(f"Insira o valor do saque: ")))

        if numero_saque >= LIMITE_SAQUE:
            print(f"[Falha Operacao]: você excedeu o seu limite de {LIMITE_SAQUE} saques)")
    
        elif saldo < saque:
            print(f"[Falha Operação]: o valor solicitado excede o seu saldo de R$ {saldo:.2f}")
        
        elif saque > limite_saque:
            print(f"[Falha Operacao]: você ultrapassou o limite de saque de R$ {limite_saque:.2f}")
        
        elif  saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saque += 1
            print(f"saldo {saldo}")
        
    
    elif opcao == "e":
        print(f"--------------EXTRATO BANCÁRIO--------------")
        print(f"[Atenção]: nenhuma movimentação foi efetuada" if not extrato else extrato)
        print(f"--------------------------------------------")
        print(f"Saldo: R$ {saldo:.2f}")
        print(f"--------------------------------------------")
        

    elif opcao == "0":
        print(f"Finalizando operação...")
        break