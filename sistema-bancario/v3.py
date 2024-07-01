from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Main():
    def menu():
        menu = """\n
        [1]\tCadastrar Cliente
        [2]\tCadastrar Conta
        [3]\tDepositar
        [4]\tSacar 
        [5]\tExtrato
        [6]\tListar Contas
        [0] Sair
    """
        return input(textwrap.dedent(menu))

    def filtrar_cliente(cpf, clientes):
        filtro = [cliente for cliente in clientes if cliente.cpf == cpf]
        return filtro[0] if filtro else None

    def recuperar_conta(cliente):
        if not cliente.conta:
            print("\n[Falha Sistêmica]: O cliente solicitado não possui conta...")
            return
        return cliente.contas[0]

    def criar_cliente(clientes):
        cpf = input("CPF do Cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n[Falha Sistêmica]: O cliente solicitado não está cadastrado no sistema...")
            return
        
        nome = input("Nome Completo: ")
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        endereco = input("Endereço (logradouro, n - bairro - cidade/estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        clientes.append(cliente)

        print("\n[Sucesso]: Cliente cadastrado com sucesso!")

    def criar_conta(numero_conta, clientes, contas):
        cpf = input("CPF do Cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n[Falha Sistêmica]: O cliente solicitado não está cadastrado no sistema...")
            return

        conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)

        print("\n[Sucesso]: Conta cadastrada com sucesso!")  
    
    def depositar(clientes):
        cpf = input("CPF do Cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n[Falha Sistêmica]: O cliente solicitado não está cadastrado no sistema...")
            return        
        
        valor = float(input("Insira o valor do depósito: "))
        transacao = Deposito(valor)

        conta = recuperar_conta(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)

    def sacar(clientes):
        cpf = input("CPF do Cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n[Falha Sistêmica]: O cliente solicitado não está cadastrado no sistema...")
            return   
        
        valor = float(input("Insira o valor do saque: "))
        transacao = Saque(valor)

        conta = recuperar_conta(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)

    def exibir_extrato(clientes):
        cpf = input("CPF do Cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n[Falha Sistêmica]: O cliente solicitado não está cadastrado no sistema...")
            return

        conta = recuperar_conta(cliente)
        if not conta:
            return
        print("--------------EXTRATO BANCÁRIO--------------")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "[Atenção]: nenhuma movimentação foi efetuada até o momento."   
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}: \n\tR${transacao['valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
        print("------------------------------------------")

    def listar_contas(contas):
        for conta in contas:
            print("=" + 100)
            print(textwrap.dedent(str(conta)))
        

    def main():
        clientes = []
        contas = []

        while True:
            opcao = menu()

            #Cadastrar Cliente
            if opcao == "1":
                criar_cliente(clientes)

            #Cadastrar Conta
            elif opcao == "2":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)

            #Depositar
            elif opcao == "3":
                depositar(clientes)
            
            #Sacar 
            elif opcao == "4":
                sacar(clientes)

            #Extrato
            elif opcao == "5":
                exibir_extrato(clientes)
            
            #Listar Contas
            elif opcao == "6":
                listar_contas(contas)
            
            elif opcao == 0:
                break

            else:
                print("[Falha Sistêmica]: Opção inválida, tente")

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
   def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    property
    def saldo(self):
        return self._saldo

    property
    def numero(self):
        return self._numero
    
    property
    def agencia(self):
        return self._agencia
    
    property
    def cliente(self):
        return self._cliente

    property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("\n[Falha Sistêmica]: Você não possui saldo suficiente para operação...")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n[Sucesso]: Saque efetuado com sucesso!")
            return True
        
        else:
            print("\n[Falha Sistêmica]: Valor informado inválido...")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n[Sucesso]: Depósito efetuado com sucesso!")
        
        else:
            print("\n[Falha Sistêmica]: Valor informado inválido...")
            return False
        
        return True

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes 
             if transacao["tipo"] == "Saque"]
        )

        if valor > self.limite:
            print(f"\n[Falha Sistêmica]: Você excedeu o limite permitido de R$500,00...")

        elif numero_saque > self.limite_saque:
            print(f"\n[Falha Sistêmica]: Você excedeu o limite de 3 saques...")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_trasacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
