import json
#Json será utilizado para armazenar as informações de usuários.
import hashlib
#Hashlib será utilizada para criptografar as senhas.
import os
#OS será utilizada para interações com o sistema operacional.
from datetime import datetime, timedelta
#Ferramentas de registro de tempo. (Data e Hora)
import statistics
#Calculos estatisticos(moda,mediana)
import matplotlib.pyplot as plt
#Construção de gráficos(Requer instalação: "pip install matplotlib")
import time
#Inserção de Pausas

Dados_de_Usuario = "usuarios.json"
def carregar_usuario():
    if not os.path.exists(Dados_de_Usuario):
        return {}
    with open(Dados_de_Usuario, "r") as f:
        return json.load(f)
    
def salvar_usuarios(usuarios):
    with open(Dados_de_Usuario, "w") as f:
        json.dump(usuarios, f, indent = 4)

#Criptografia
def senha_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario():
    while True:
        print("\n"*3)
        usuarios = carregar_usuario()
        print()
        print("\nAo prosseguir com o cadastro, você autoriza o uso dos seus dados pessoais(nome, idade e interações com o sistema) exclusivamente para fins de didáticos e de estudo, com o objetivo de analisar e aprimorar\na inclusão digital e o ensino da lógica computacional por meio deste sistema.")
        print("Seus dados não são compartilhados, e o acesso à sua conta é protegido por senha criptografada.\nVocê poderá a qualquer momento solicitar a exclusão do seu usuário do sistema, conforme previsto pela Lei Geral de Proteção de Dados.")
        termo = input("\nDigite 1 se li e aceito os termos: ")
        print("-"*70)
        if termo == "1":
            break
        else:
            print("Invalido")
    while True:
        nome = input("\nInsira o nome de usuário: ").strip().lower()
        if nome in usuarios:
            print("Nome de usuario ja existente. Tente outro!")
        else:
            break
    
    senha = input("Digite a senha: ").strip()
    hash_senha = senha_hash(senha)
    
    idade = input("Digite a sua idade: ")

    usuarios[nome] = {
        "senha": hash_senha,
        "criado_em": datetime.now().strftime( "%d-%m-%Y, %H:%M:%S" ),
        "idade" : idade
    }
    salvar_usuarios(usuarios)
    print ("Usuário cadastrado com sucesso!")

def login_usuario():
    usuarios = carregar_usuario()
    print("\n"*3)
    
    nome = input("Insira o seu nome de usuário: ").strip().lower()
    senha = input("Insira a sua senha: ")
    
    print("\n"*8)
    
    if nome in usuarios:
        hash_senha = senha_hash(senha)
        if usuarios[nome]["senha"] == hash_senha:
            print("-" * 70)
            print ("Login realizado com sucesso!")
            menu_usuario(nome)
            return True
        else:
            print("Senha incorreta!")
    else:
        print("Usuário não encontrado!")
        
def menu():
    while True:
        print("\n"*6)
        print ("-" * 70)
        print("Bem vindo(a)! Selecione uma opção abaixo")
        print()
        print("\n1.Criar novo usuário\n2.Fazer login em usuário cadastrado\n3.Login de administrador\n4.Sair\n5.Mais informações")
        op = input("Selecione a opção desejada:\n")
        if op == "1":
            print("-" * 70)
            cadastrar_usuario()
        elif op == "2":
            print("-" * 70)
            login_usuario()
        elif op == "3":
            login_administrador()
            
        elif op == "4":
            print(f"\nEncerrando . . .")
            break
        elif op == "5":
            menu_mais_informacoes()
        else:
            print ("Opção inválida")
            
def menu_mais_informacoes():
    while True:
        print()
        print("\n **MAIS INFORMAÇÕES**")
        print("\n1.Quais sao os dados coletados\n2.Por que coletamos os dados\n3.Quem tem acesso aos dados\n4.Exclusao de cadastro\n5.Voltar")
        op = input("\n\nO que deseja saber? ")
        if op == "1":
            print("-"*70)
            print("No momento da criação do cadastro, o sistema coleta o nome de usuário, idade, a senha no formato de criptografia hash SHA-256, e a data de criação da conta.\nDepois de efetuado o login, o sistema também registra o tempo em que usuário ficou logado.")
            print("-"*70)
        elif op == "2":
            print("-"*70)
            print("Os dados são coletados exclusivamente para propósitos educacionais e estatísticos, e são utilizados para e somente para realização de cálculos matemáticos")
            print("-"*70)
        elif op == "3":
            print("-"*70)
            print("Apenas o administrador da plataforma, que possui um login restrito tem acesso aos dados agregados.\nVale ressaltar que as senhas são criptografas, e o próprio administrador não possui o acesso ao seu conteúdo original.")
            print("-"*70)
        elif op == "4":
            print("-"*70)
            print("O sistema implementa uma função direta no menu do usuário. A exclusão do seu cadastro remove permanentemente seus dados do arquivo JSON.")
            print("-"*70)
        elif op == "5":
            break
        else:
            print("Invalido!")
        
  
def menu_usuario(nome):
    inicio_sessao = datetime.now()
    while True:
        print("\n"*3)
        print("-" * 70)
        time.sleep(0.5)
        print(f"Bem vindo, {nome}!")
        time.sleep(1)
        print("\n1.Ver meus dados\n2.Sair da conta\n3.Modulo de Ensino\n0.Se desejar exluir o seu cadastro")
        op = input("Escolha o que vai fazer: ")
        print("\n"*3)
        if op == "1":
            with open(Dados_de_Usuario, "r") as f:
                    usuarios = json.load(f)
            if nome in usuarios:
                    dados = usuarios[nome]
                    print ("-" * 70)
                    print(f"Usuario: {nome} ")
                    print(f"Criado em: {dados.get('criado_em')}")
                    print(f"Idade:{dados.get('idade', 'Nao informada')}")
                    
        elif op == "0":
            excluir_usuario(nome)
            break
                
        elif op == "3":
            menu_modulos()
                       
        elif op == "2":
            fim_sessao = datetime.now()
            duracao = fim_sessao - inicio_sessao
            
            tempo_em_segundos = duracao.total_seconds()
            minutos, segundos = divmod(duracao.total_seconds(), 60)
            tempo = f"{int(minutos)} min e {int(segundos)} seg"
            with open (Dados_de_Usuario, "r") as f:
                usuarios = json.load(f)
                
            if nome in usuarios:
                usuarios[nome]['tempo_de_uso'] = tempo_em_segundos
                
            with open(Dados_de_Usuario, "w") as f:
                json.dump(usuarios, f , indent=4)
                
            time.sleep(1)
            print(f"Você usou o sistema por {int(minutos)} min e {int(segundos)} seg.")
            time.sleep(1.5)
            print("Saindo da conta . . .")
            time.sleep(2)
            break      
def excluir_usuario(nome):
    while True:
            print ("\n"*13)
            print("-" * 70)
            print("Se desejar, você pode excluir seu cadastro quando quiser.")
            aceitar_exclusao = input("Leia com atenção: Se voce deseja excluir a sua conta, deve digitar 'Sim'(Esta ação é irreversível), ou 0 para voltar para o menu principal\n------>:").strip().lower()
            if aceitar_exclusao == "sim":
                with open(Dados_de_Usuario, "r") as f:
                    usuarios = json.load(f)
            elif aceitar_exclusao == "0":
                break
            
            if nome in usuarios:
                del usuarios[nome]
                with open(Dados_de_Usuario, "w") as f:
                    json.dump(usuarios, f , indent=4)
                    time.sleep(1)
                    print("Seu cadastro foi excluido com sucesso")
                    time.sleep(3)
                    break  
        
def total_usuarios():
    with open(Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
        print("\n")
        print(f"Numero total de usarios cadastrados: {len(usuarios)}")
        
def tempo_medio_uso():
    with open (Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
        
    tempos = []
    for usuario in usuarios.values():
        tempo = usuario.get("tempo_de_uso", 0)
        tempos.append(tempo)
        
    if tempos:
        media = statistics.mean(tempos)
        print("\n")
        print(f"Tempo medio de uso: {media:.2f} segundos")
    else:
        ("\n"*2)
        print("Nenhum dado de tempo disponivel.")
        
def estatisticas_uso():
    with open(Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
    tempos = [u.get("tempo_de_uso", 0) for u in usuarios.values()]
    if len(tempos) >= 1:
        print(f"\nEstatisticas de uso(Em segundos): ")
        print(f"Media: {statistics.mean(tempos):.2f}")
        print(f"Mediana: {statistics.median(tempos):.2f}")
        try:
            print(f"Moda: {statistics.mode(tempos):.2f}")
        except statistics.StatisticsError:
            print("Nao ha moda(sem dados repetidos)")
    else:
        print("Dados Insuficientes!")
        
def menu_administrador():
    while True:
        print("\n"*5)
        print("=" *60)
        print("\n========= Menu do Administrador =========")
        print("\n1.Ver número total de usuários\n2.Ver tempo médio de uso\n3.Ver estatisticas simples por tempo(media,moda e mediana)\n4.Visualizar Graficos\n5.Voltar ao menu principal")
        op = input("\nEscolha a opção desejada: ")
        if op == "1":
            total_usuarios()
        elif op == "2":
            tempo_medio_uso()
        elif op == "3":
            estatisticas_uso()
        elif op == "4":
            menu_graficos()
        elif op == "5":
            break
        else:
            print("Invalido")
            

def login_administrador():
    admin_user = "setadministrador"
    admin_senha = "AWR2025"
    print("\n"*5)
    print("=== Login do Administrador ===")
    usuario = input("Insira o usuario: ").strip().lower()
    senha = input("Insira a senha: ")
    
    if usuario == admin_user and senha == admin_senha:
        print()
        print("=" * 60)
        print()
        time.sleep(1)
        print("Login de administrador realizado com sucesso!\n")
        time.sleep(2)
        menu_administrador()
    else:
        print("Credenciais incorretas. Por favor, tente novamente!")
#----------------------------------------------------------------------------------------------------Graficos    
def grafico_total_usuarios():
    with open (Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
        
    numero_total_usuarios = len(usuarios)
    
    plt.bar(['Usuarios'], [numero_total_usuarios], color = 'skyblue')
    plt.title('Numero total de Usuarios')
    plt.xlabel('Categoria')
    plt.ylabel('Quantidade de Usuarios')
    plt.show()
    
def grafico_tempo_medio():
    with open (Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
        
    tempos = [usuarios.get("tempo_de_uso", 0) for usuario in usuarios.values()]
    
    if tempos:
        media = statistics.mean(tempos)
        
        plt.bar(['Tempo medio de uso'],[media], color='lightgreen')
        plt.title('Tempo medio de uso(segundos)')
        plt.xlabel('Categoria')
        plt.ylabel('Tempo(Segundos)')
        plt.show()
    else:
        print("Nenhum dado de tempo disponivel")
        
def grafico_idade():
    with open(Dados_de_Usuario, "r") as f:
        usuarios = json.load(f)
        
    idades = [int(usuario.get("idade", 0)) for usuario in usuarios.values()]
    
    if idades:
        
        plt.hist(idades, bins=range(min(idades), max(idades) + 2), edgecolor='black', color='orange')
        plt.title('Distribuição das Idades de Usuários')
        plt.xlabel('Idade')
        plt.ylabel('Quantidade de usuarios')
        plt.show()
        
    else:
        print("Nenhum dado disponivel")
        
def menu_graficos():
    while True:
        print("=" * 70)
        print("\n======>Visualização de Gráficos<======")
        print("\n1.Gráfico Total de Usuarios\n2.Gráfico Tempo Medio de Uso\n3.Gráfico de distribuição de idades\n4.Sair")
        op = input("O que deseja visualizar? ")
        if op == "1":
            grafico_total_usuarios()
        elif op == "2":
            grafico_tempo_medio()
        elif op == "3":
            grafico_idade()
        elif op == "4":
            break
        else:
            print("Opção inválida!")
#----------------------------------------------------------------------------------------------------Graficos-Fim
#----------------------------------------------------------------------------------------------------------------Matemática e Estatística-Fim
#----------------------------------------------------------------------------------------------------------------PLCP-Inicio
def menu_modulos():
    while True:
        print("\n"*2)
        print("Bem vindo(a) à área de aprendizagem! Escolha um módulo para começar.\n1.Módulo de Pensamento Lógico Computacional com Python\n2.Módulo de Ética e Sustentabilidade\n3.Sair\n")
        print()
        op = input("O que deseja? ")
        
        if op == "1":
            modulo_logica()
        elif op == "2":
            modulo_sustentabilidade()
        elif op == "3":
            break
            
def modulo_logica():
    while True:
        time.sleep(1)
        print("----------->Modulo de ensino:Pensamento Lógico Computacional com Python*")
        print()
        time.sleep(1)
        print("Seja Bem vindo(a) ao módulo de ensino!\nAqui você aprenderá conceitos de Lógica Computacional e conceitos básicos de programação em Python!")
        op = input("Escolha 1 para continuar ou 2 para sair: ")
        
        if op == "1":
            print("\n" * 5)
            time.sleep(1)
            print("\nEntrando em módulo de Pensamento Lógico Computacional. . .")
            print("\n" * 3)
            time.sleep(1)
            
            pontuacao = 0 
            perguntas = [
                {
                    "pergunta" : "1. O que este codigo imprime?\n\n x=10\nif x > 5:\n   print('maior que cinco')\nelse:\n   print('Menor ou igual a 5')\n\nA)Maior que 5\nB)Menor ou igual a 5\nC)Erro\n\n",
                    "resposta" : "A"
                },
                {
                    "pergunta" : "2. Qual das alternativas representa uma estrutura de repetição? \nA) if\nB) while\nC) print\n\n",
                    "resposta" : "B"
                },
                {
                    "pergunta" : "3. Qual o restultado de:\n\nprint(2 + 3 * 4)\nA)20\nB)14\nC)24\n\n",
                    "resposta" : "B"
                },
                {
                    "pergunta": "4. Qual das opções representa uma variável válida em Python?\nA) nome_2\nB) 2nome\nC) nome-2\n\n",
                    "resposta": "A"
                },
                {
                    "pergunta": "5. Qual é o tipo do valor: 'Olá Mundo'?\nA) int\nB) bool\nC) str\n\n",
                    "resposta": "C"
                },
                {
                    "pergunta": "6. O que o operador '==' faz em Python?\nA) Atribui um valor a uma variável\nB) Soma dois valores\nC) Compara dois valores\n",
                    "resposta": "C"
                },
                {
                    "pergunta": "7. Qual é a saída do seguinte código?\n\nlista = [1, 2, 3]\nprint(lista[1])\n\nA) 2\nB) 1\nC) 3\n\n",
                    "resposta": "A"
                },
                {
                    "pergunta": "8. O que o seguinte laço imprime?\n\nfor i in range(3):\n    print(i)\n\nA) 0 1 2\nB) 1 2 3\nC) 0 1 2 3\n\n",
                    "resposta": "A"
                },
                {
                    "pergunta": "9. Qual das opções define corretamente uma função em Python?\n\nA) função minha():\n       pass\nB) def minha_funcao():\n       pass\nC) function minha():\n       pass\n\n",
                    "resposta": "B"
                },
                {
                    "pergunta": "10. Qual o resultado da expressão:\nTrue and False\n\nA) True\nB) False\nC) Erro\n\n",
                    "resposta": "B"
                },
                {
                    "pergunta": "11. Qual operador é usado para verificar se duas condições são verdadeiras ao mesmo tempo?\nA) or\nB) not\nC) and\n\n",
                    "resposta": "C"
                },
                {
                    "pergunta": "12. O que o seguinte código imprime?\n\nx = 5\ny = 10\nif x > 3 and y < 15:\n    print('Correto')\nelse:\n    print('Incorreto')\n\nA) Correto\nB) Incorreto\nC) Erro de sintaxe\n\n",
                    "resposta": "A"
                }
]
            for p in perguntas:
                resposta = input(p["pergunta"] + "\nSua resposta: ").upper()
                if resposta == p["resposta"]:
                    print("Correto!\n")
                    pontuacao +=1
                else:
                    print(f"Errado. A alternativa correta era: {p['resposta']}\n")
                    
            print(f"Fim do módulo! Sua pontuação: {pontuacao}/{len(perguntas)}")
            if pontuacao == len(perguntas):
                time.sleep(1)
                print("Muito bem! Você entendeu bem os conceitos.\n")
                time.sleep(2)
            elif pontuacao >=2:
                time.sleep(1)
                print("Ótimo! Continue praticando!\n")
                time.sleep(2)
            else:
                time.sleep(1)
                print("Tente novamente para melhorar seu entendimento!")
                time.sleep(3)
                
            print("\n"*3)
            time.sleep(1)
            print("     ---Verificação do nível de aprendizado---\n")
            time.sleep(1)
            nivel_aprendizado(pontuacao)
            time.sleep(2)
                
        elif op == "2":
            break    
        else:
            ("Invalido!")
            
def modulo_sustentabilidade():
    while True:
        time.sleep(1)
        print("----------->Modulo de ensino:Ética e sustentabilidade*")
        print()
        print("Seja Bem vindo(a) ao módulo de ensino!\nAqui você aprenderá conceitos de ética e sustentabilidade")
        op = input("Escolha 1 para continuar ou 2 para sair: ")
        
        if op == "1":
            time.sleep(1)
            print("\n" * 3)
            print("Entrando no modulo de sustentabilidade. . .")
            time.sleep(2)
            print("\n" * 3)
            print("  ***Manual de Ética e Sustentabilidade***\n")
            
            #capitulo 1
            time.sleep(2)
            print("----Capítulo 1 – O que é Ética Digital?")
            time.sleep(1)
            print()
            print(
                "A ética digital trata das condutas responsáveis no uso das tecnologias.Isso envolve respeitar outras pessoas online, evitar disseminação de informações falsas, proteger dados pessoais e agir com integridade nas interações\nvirtuais\nSer ético no mundo digital significa pensar nas consequências dos nossos atos, mesmo em ambientes onde o anonimato é possível.\n\n-Exemplos de práticas éticas-\n\n-->Não compartilhar notícias sem verificar a veracidade..\n-->Respeitar os direitos autorais de imagens, músicas e textos.\n-->Não expor outras pessoas sem consentimento.\n"
            )
            print("\n"*3)
            #capitulo 2
            time.sleep(2)
            print("----Capítulo 2 — Privacidade e Proteção de Dados")
            time.sleep(1)
            print()
            print(
                "Neste capítulo, discutimos a importância de proteger informações pessoais. Toda ação que realizamos online gera rastros: cliques, buscas, localizações, entre outros.\nÉ fundamental saber como nossos dados são coletados e utilizados por sites, redes sociais e aplicativos.\n\n-Dicas para preservar a privacidade-\n\n-->Utilizar senhas fortes e únicas.\n-->Ativar autenticação em duas etapas.\n-->Ler os termos de uso antes de aceitar."
            )
            print("\n"*3)
            #capitulo 3
            time.sleep(2)
            print("----Capítulo 3 — Sustentabilidade Digital")
            time.sleep(1)
            print()
            print(
                "Sustentabilidade digital não é apenas sobre o meio ambiente, mas também sobre o uso consciente e duradouro da tecnologia.\nIsso inclui o descarte correto de equipamentos eletrônicos, a redução de consumo de energia, e o uso de ferramentas que prolongam a vida útil dos dispositivos.\n\n-Práticas sustentáveis-\n\n-->Reutilizar ou doar eletrônicos em bom estado.\n-->Desligar equipamentos quando não estiverem em uso.\n-->Priorizar serviços que consomem menos recursos (ex: sites leves, aplicativos otimizados)."
            )
            print("\n"*3)
            #capitulo 4
            time.sleep(2)
            print("----Capítulo 4 — Combate à Desinformação")
            time.sleep(1)
            print()
            print(
                "Fake news podem causar grandes danos sociais, políticos e até à saúde pública.\nAprender a identificar fontes confiáveis e desenvolver pensamento crítico é essencial para uma convivência digital saudável.\n\n-Como combater a desinformação-\n\n-->Verifique a fonte da informação.\n-->Busque notícias em diferentes canais confiáveis.\n-->Denuncie conteúdos falsos em redes sociais."
            )
            print("\n"*3)
            #capitulo 5
            time.sleep(2)
            print("----Capítulo 5 — Cidadania Digital")
            time.sleep(1)
            print()
            print(
                "Ser cidadão digital é participar ativamente da sociedade online com consciência dos direitos e deveres.\nIsso inclui agir com respeito, promover inclusão, evitar discursos de ódio, e ajudar na construção de um ambiente virtual saudável.\n\n-Direitos do cidadão digital-\n\n-->Liberdade de expressão (com responsabilidade).\n-->Acesso à informação de forma clara e segura.\n-->Proteção contra crimes virtuais."
            )
            print("\n")
            break
          
        elif op == "2":
            break

def nivel_aprendizado(pontuacao):
    percentual = (pontuacao / 12) * 100
    time.sleep(1)
    if percentual >=80:
        print("Seu nivel de aprendizado: Excelente")
    elif percentual >=60:
        print("Seu nivel de aprendizado: Bom")
    elif percentual >=40:
        print("Seu nivel de aprendizado: Regular")
    else:
        print("Seu nivel de aprendizado: Ruim")
    print("\n"*3)
    
menu()