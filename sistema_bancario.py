# módulo para formatação de texto eficiente
import textwrap

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


def main():
    saldo = 0
    LIMITE_VALOR_SAQUE = 500
    extrato = ""
    contador_saque_diario = 0
    LIMITE_SAQUES = 3
    
    while True:
        opcao = menu() # Chamando por funcao

        if opcao == "d":
            print("Deposito")
            valor_deposito = float(input("Informe o valor para depósito: "))
        
            if valor_deposito > 0:
                saldo += valor_deposito
                extrato +=f"Depósito: R$ {valor_deposito:.2f}\n"
                print("Depósito realizado com sucesso!")
            else:
                print("Operação falhou: O valor informado é inválido")
        
        elif opcao == "s":
            print("Saque")
            valor_saque = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor_saque > saldo
            excedeu_limite = valor_saque > LIMITE_VALOR_SAQUE
            excedeu_saques = contador_saque_diario >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Operação falhou. Você não tem saldo suficiente.")
            elif excedeu_limite:
                print("Operação falhou. O valor do saque excede o limite permitido.")
            elif excedeu_saques:
                print("Operação falhou. Quantidade máximo de saques realizados.")
        
            elif valor_saque > 0:
                saldo -= valor_saque
                extrato += f"Saque: R$ {valor_saque:.2f}\n"
                contador_saque_diario += 1
                print("Saque realizado com sucesso.")
            else:
                print("Operação falhou. O valor informado é inválido.")

        elif opcao == "e":
            print("\n********** EXTRATO **********")
            print("NÃO TEVE MOVIMENTAÇÕES" if not extrato else extrato)
            print(f"Saldo atual R$ {saldo:.2f}")
            print("*****************************")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada.")

main()