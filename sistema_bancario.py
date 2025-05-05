# Adaptação do código para POO
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        # Atributos privados
        self._endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) # Herdou de Cliente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self.saldo -= valor
            print("\n === Saque realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n === Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3, ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

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
        self.transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
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


# Função para o menu
def menu():
    menu ="""\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar conta
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))


# Recebe argumentos apenas por posição (Positional only)
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n### Depósito realizado com sucesso! ###")
    else:
        print("\n### Operação falhou! O valor informado é inválido. ###")
    return saldo, extrato

    
# Recebe argumentos apenas por nome (Keywords only)
def sacar(*, saldo, valor, extrato, limite, numeros_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numeros_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou. Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou. O valor do saque excede o limite permitido. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou. Quantidade máximo de saques realizados. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numeros_saques += 1
        print("Saque realizado com sucesso.")
        print(f"Saques realizados hoje: {numeros_saques}")

    else:
        print("Operação falhou. O valor informado é inválido.")

    return saldo, extrato, numeros_saques


# Exibir extrato por posição e nome (Positional only e Keywords only)
def exibir_extrato(saldo, /,*, extrato):
    print("\n=============== EXTRATO ===============")
    print("NÃO TEVE MOVIMENTAÇÕES" if not extrato else extrato)
    print(f"Saldo atual:\tR$ {saldo:.2f}")
    print("==========================================")


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF: @@@")
        return

    nome =input("Informe o seu nome completo: ")
    data_nascimento =input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("### Usuário criado com sucesso! ###")


# Função para filtrar usuarios na lista
def filtrar_usuario(cpf, usuarios):
    # Verifica se já existe algum usuário com o CPF informado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario # Retorna dicionário do usuario
    return None # CPF não encontrado, retorna None


# Função para criação de conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n### Conta criada com sucesso! ###")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

# Função para listar contas existentes
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    AGENCIA = "0001"
    LIMITE_VALOR_SAQUE = 500
    LIMITE_SAQUES = 3

    saldo = 0
    extrato = ""
    contador_saque_diario = 0
    usuarios =[]
    contas = []
    
    while True:
        opcao = menu() # Chamando por funcao

        if opcao == "d":
            print("Deposito")
            valor_deposito = float(input("Informe o valor para depósito: "))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
        
        elif opcao == "s":
            print("Saque")
            valor_saque = float(input("Informe o valor do saque: "))
            saldo, extrato, contador_saque_diario = sacar(
                saldo=saldo, 
                valor=valor_saque,
                extrato=extrato,
                limite=LIMITE_VALOR_SAQUE,
                numeros_saques=contador_saque_diario,
                limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            # Forma diferente da criação usuario
            # Faz essa verificação para não armazenar na lista contas vazias pois o retorno da função se usuario for falso é none
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada.")

main()