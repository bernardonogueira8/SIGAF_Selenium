import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os


# Configurações de tema e aparência
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
# --- Funções de Automação ---


def login(navegador, user, password):
    navegador.find_element(By.NAME, 'login').send_keys(user)
    navegador.find_element(By.NAME, 'senha').send_keys(password)
    navegador.find_element(By.NAME, "acessar").click()


def extrair_dados(navegador, prefeitura):
    navegador.get(
        'https://sigaf.sesab.ba.gov.br/?page=meta/view&id_view=tb_grs_1&_menu_acessado=324')
    wait = WebDriverWait(navegador, 10)

    try:
        campo_busca = wait.until(EC.presence_of_element_located(
            (By.NAME, 'busca__nom_grs**140,0;87___str//0/0')))
        campo_busca.clear()
        campo_busca.send_keys(prefeitura)

        btn_buscar = navegador.find_element(By.ID, "btn_busca")
        btn_buscar.click()

        btn_mostrar = wait.until(
            EC.element_to_be_clickable((By.ID, "btn_mostra")))
        btn_mostrar.click()

        # Espera carregar o campo específico do secretário
        wait.until(EC.presence_of_element_located(
            (By.ID, 'span_nom_sec_saude**140,0;87___str//0/0')))

        return {
            'Secretário de saúde': navegador.find_element(By.ID, 'span_nom_sec_saude**140,0;87___str//0/0').text,
            'Email': navegador.find_element(By.ID, 'td_input_email_sec_saude**140,0;87___str//0/0').text,
            'Telefone': navegador.find_element(By.ID, 'span_tel_sec_saude**140,0;87___tel//0/0').text,
            'Celular': navegador.find_element(By.ID, 'span_cel_sec_saude**140,0;87___tel//0/0').text,
            'Prefeitura': navegador.find_element(By.ID, 'span_nom_grs**140,0;87___str//0/0').text
        }
    except Exception as e:
        print(f"Erro ao processar {prefeitura}: {e}")
        return None

# --- Classe da Interface ---


class AppRobo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(
            "Automação do SIGAF - Baixar informações do Secretario de Saúde")
        self.geometry("550x600")

        # Variáveis de controle
        self.diretorio_destino = ""

        self.prefeituras_ba = [
            "PREFEITURA MUNICIPAL De Abaíra",
            "PREFEITURA MUNICIPAL De Abaré",
            "PREFEITURA MUNICIPAL De Acajutiba",
            "PREFEITURA MUNICIPAL De Adustina",
            "PREFEITURA MUNICIPAL De Água Fria",
            "PREFEITURA MUNICIPAL De Aiquara",
            "PREFEITURA MUNICIPAL De Alagoinhas",
            "PREFEITURA MUNICIPAL De Alcobaça",
            "PREFEITURA MUNICIPAL De Almadina",
            "PREFEITURA MUNICIPAL De Amargosa",
            "PREFEITURA MUNICIPAL De Amélia Rodrigues",
            "PREFEITURA MUNICIPAL De América Dourada",
            "PREFEITURA MUNICIPAL De Anagé",
            "PREFEITURA MUNICIPAL De Andaraí",
            "PREFEITURA MUNICIPAL De Andorinha",
            "PREFEITURA MUNICIPAL De Angical",
            "PREFEITURA MUNICIPAL De Anguera",
            "PREFEITURA MUNICIPAL De Antas",
            "PREFEITURA MUNICIPAL De Antônio Cardoso",
            "PREFEITURA MUNICIPAL De Antônio Gonçalves",
            "PREFEITURA MUNICIPAL De Aporá",
            "PREFEITURA MUNICIPAL De Apuarema",
            "PREFEITURA MUNICIPAL De Araças",
            "PREFEITURA MUNICIPAL De Aracatu",
            "PREFEITURA MUNICIPAL De Araci",
            "PREFEITURA MUNICIPAL De Aramari",
            "PREFEITURA MUNICIPAL De Arataca",
            "PREFEITURA MUNICIPAL De Aratuípe",
            "PREFEITURA MUNICIPAL De Aurelino Leal",
            "PREFEITURA MUNICIPAL De Baianópolis",
            "PREFEITURA MUNICIPAL De Baixa Grande",
            "PREFEITURA MUNICIPAL De Banzaê",
            "PREFEITURA MUNICIPAL De Barra",
            "PREFEITURA MUNICIPAL De Barra Da Estiva",
            "PREFEITURA MUNICIPAL De Barra Do Choça",
            "PREFEITURA MUNICIPAL De Barra Do Mendes",
            "PREFEITURA MUNICIPAL De Barra Do Rocha",
            "PREFEITURA MUNICIPAL De Barreiras",
            "PREFEITURA MUNICIPAL De Barro Alto",
            "PREFEITURA MUNICIPAL De Barro Preto (Gov. Lomanto Jr.)",
            "PREFEITURA MUNICIPAL De Barrocas",
            "PREFEITURA MUNICIPAL De Belmonte",
            "PREFEITURA MUNICIPAL De Belo Campo",
            "PREFEITURA MUNICIPAL De Biritinga",
            "PREFEITURA MUNICIPAL De Boa Nova",
            "PREFEITURA MUNICIPAL De Boa Vista Do Tupim",
            "PREFEITURA MUNICIPAL De Bom Jesus Da Lapa",
            "PREFEITURA MUNICIPAL De Bom Jesus Da Serra",
            "PREFEITURA MUNICIPAL De Boninal",
            "PREFEITURA MUNICIPAL De Bonito",
            "PREFEITURA MUNICIPAL De Boquira",
            "PREFEITURA MUNICIPAL De Botuporã",
            "PREFEITURA MUNICIPAL De Brejões",
            "PREFEITURA MUNICIPAL De Brejolândia",
            "PREFEITURA MUNICIPAL De Brotas De Macaúbas",
            "PREFEITURA MUNICIPAL De Brumado",
            "PREFEITURA MUNICIPAL De Buerarema",
            "PREFEITURA MUNICIPAL De Buritirama",
            "PREFEITURA MUNICIPAL De Caatiba",
            "PREFEITURA MUNICIPAL De Cabaceiras Do Paraguaçu",
            "PREFEITURA MUNICIPAL De Cachoeira",
            "PREFEITURA MUNICIPAL De Caculé",
            "PREFEITURA MUNICIPAL De Caém",
            "PREFEITURA MUNICIPAL De Caetanos",
            "PREFEITURA MUNICIPAL De Caetité",
            "PREFEITURA MUNICIPAL De Cafarnaum",
            "PREFEITURA MUNICIPAL De Cairu",
            "PREFEITURA MUNICIPAL De Caldeirão Grande",
            "PREFEITURA MUNICIPAL De Camacan",
            "PREFEITURA MUNICIPAL De Camaçari",
            "PREFEITURA MUNICIPAL De Camamu",
            "PREFEITURA MUNICIPAL De Campo Alegre De Lourdes",
            "PREFEITURA MUNICIPAL De Campo Formoso",
            "PREFEITURA MUNICIPAL De Canápolis",
            "PREFEITURA MUNICIPAL De Canarana",
            "PREFEITURA MUNICIPAL De Canavieiras",
            "PREFEITURA MUNICIPAL De Candeal",
            "PREFEITURA MUNICIPAL De Candeias",
            "PREFEITURA MUNICIPAL De Candiba",
            "PREFEITURA MUNICIPAL De Cândido Sales",
            "PREFEITURA MUNICIPAL De Cansanção",
            "PREFEITURA MUNICIPAL De Canudos",
            "PREFEITURA MUNICIPAL De Capela Do Alto Alegre",
            "PREFEITURA MUNICIPAL De Capim Grosso",
            "PREFEITURA MUNICIPAL De Caraíbas",
            "PREFEITURA MUNICIPAL De Caravelas",
            "PREFEITURA MUNICIPAL De Cardeal Da Silva",
            "PREFEITURA MUNICIPAL De Carinhanha",
            "PREFEITURA MUNICIPAL De Casa Nova",
            "PREFEITURA MUNICIPAL De Castro Alves",
            "PREFEITURA MUNICIPAL De Catolândia",
            "PREFEITURA MUNICIPAL De Catu",
            "PREFEITURA MUNICIPAL De Caturama",
            "PREFEITURA MUNICIPAL De Central",
            "PREFEITURA MUNICIPAL De Chorrochó",
            "PREFEITURA MUNICIPAL De Cícero Dantas",
            "PREFEITURA MUNICIPAL De Cipó",
            "PREFEITURA MUNICIPAL De Coaraci",
            "PREFEITURA MUNICIPAL De Cocos",
            "PREFEITURA MUNICIPAL De Conceição Da Feira",
            "PREFEITURA MUNICIPAL De Conceição Do Almeida",
            "PREFEITURA MUNICIPAL De Conceição Do Coité",
            "PREFEITURA MUNICIPAL De Conceição Do Jacuípe",
            "PREFEITURA MUNICIPAL De Conde",
            "PREFEITURA MUNICIPAL De Condeúba",
            "PREFEITURA MUNICIPAL De Contendas Do Sincorá",
            "PREFEITURA MUNICIPAL De Coração De Maria",
            "PREFEITURA MUNICIPAL De Cordeiros",
            "PREFEITURA MUNICIPAL De Coribe",
            "PREFEITURA MUNICIPAL De Coronel João Sá",
            "PREFEITURA MUNICIPAL De Correntina",
            "PREFEITURA MUNICIPAL De Cotegipe",
            "PREFEITURA MUNICIPAL De Cravolândia",
            "PREFEITURA MUNICIPAL De Crisópolis",
            "PREFEITURA MUNICIPAL De Cristópolis",
            "PREFEITURA MUNICIPAL De Cruz Das Almas",
            "PREFEITURA MUNICIPAL De Curaçá",
            "PREFEITURA MUNICIPAL De Dário Meira",
            "PREFEITURA MUNICIPAL De Dias Davila",
            "PREFEITURA MUNICIPAL De Dom Basílio",
            "PREFEITURA MUNICIPAL De Dom Macedo Costa",
            "PREFEITURA MUNICIPAL De Elísio Medrado",
            "PREFEITURA MUNICIPAL De Encruzilhada",
            "PREFEITURA MUNICIPAL De Entre Rios",
            "PREFEITURA MUNICIPAL De Érico Cardoso",
            "PREFEITURA MUNICIPAL De Esplanada",
            "PREFEITURA MUNICIPAL De Euclides Da Cunha",
            "PREFEITURA MUNICIPAL De Eunápolis",
            "PREFEITURA MUNICIPAL De Fátima",
            "PREFEITURA MUNICIPAL De Feira Da Mata",
            "PREFEITURA MUNICIPAL De Feira De Santana",
            "PREFEITURA MUNICIPAL De Filadélfia",
            "PREFEITURA MUNICIPAL De Firmino Alves",
            "PREFEITURA MUNICIPAL De Floresta Azul",
            "PREFEITURA MUNICIPAL De Formosa Do Rio Preto",
            "PREFEITURA MUNICIPAL De Gandu",
            "PREFEITURA MUNICIPAL De Gavião",
            "PREFEITURA MUNICIPAL De Gentio Do Ouro",
            "PREFEITURA MUNICIPAL De Glória",
            "PREFEITURA MUNICIPAL De Gongogi",
            "PREFEITURA MUNICIPAL De Governador Mangabeira",
            "PREFEITURA MUNICIPAL De Guajeru",
            "PREFEITURA MUNICIPAL De Guanambi",
            "PREFEITURA MUNICIPAL De Guaratinga",
            "PREFEITURA MUNICIPAL De Heliópolis",
            "PREFEITURA MUNICIPAL De Iaçu",
            "PREFEITURA MUNICIPAL De Ibiassucê",
            "PREFEITURA MUNICIPAL De Ibicaraí",
            "PREFEITURA MUNICIPAL De Ibicoara",
            "PREFEITURA MUNICIPAL De Ibicuí",
            "PREFEITURA MUNICIPAL De Ibipeba",
            "PREFEITURA MUNICIPAL De Ibipitanga",
            "PREFEITURA MUNICIPAL De Ibiquera",
            "PREFEITURA MUNICIPAL De Ibirapitanga",
            "PREFEITURA MUNICIPAL De Ibirapuã",
            "PREFEITURA MUNICIPAL De Ibirataia",
            "PREFEITURA MUNICIPAL De Ibitiara",
            "PREFEITURA MUNICIPAL De Ibititá",
            "PREFEITURA MUNICIPAL De Ibotirama",
            "PREFEITURA MUNICIPAL De Ichu",
            "PREFEITURA MUNICIPAL De Igaporã",
            "PREFEITURA MUNICIPAL De Igrapiúna",
            "PREFEITURA MUNICIPAL De Iguaí",
            "PREFEITURA MUNICIPAL De Ilhéus",
            "PREFEITURA MUNICIPAL De Inhambupe",
            "PREFEITURA MUNICIPAL De Ipecaetá",
            "PREFEITURA MUNICIPAL De Ipiaú",
            "PREFEITURA MUNICIPAL De Ipirá",
            "PREFEITURA MUNICIPAL De Ipupiara",
            "PREFEITURA MUNICIPAL De Irajuba",
            "PREFEITURA MUNICIPAL De Iramaia",
            "PREFEITURA MUNICIPAL De Iraquara",
            "PREFEITURA MUNICIPAL De Irará",
            "PREFEITURA MUNICIPAL De Irecê",
            "PREFEITURA MUNICIPAL De Itabela",
            "PREFEITURA MUNICIPAL De Itaberaba",
            "PREFEITURA MUNICIPAL De Itabuna",
            "PREFEITURA MUNICIPAL De Itacaré",
            "PREFEITURA MUNICIPAL De Itaeté",
            "PREFEITURA MUNICIPAL De Itagi",
            "PREFEITURA MUNICIPAL De Itagibá",
            "PREFEITURA MUNICIPAL De Itagimirim",
            "PREFEITURA MUNICIPAL De Itaguaçu Da Bahia",
            "PREFEITURA MUNICIPAL De Itaju Do Colônia",
            "PREFEITURA MUNICIPAL De Itajuípe",
            "PREFEITURA MUNICIPAL De Itamaraju",
            "PREFEITURA MUNICIPAL De Itamari",
            "PREFEITURA MUNICIPAL De Itambé",
            "PREFEITURA MUNICIPAL De Itanagra",
            "PREFEITURA MUNICIPAL De Itanhém",
            "PREFEITURA MUNICIPAL De Itaparica",
            "PREFEITURA MUNICIPAL De Itapé",
            "PREFEITURA MUNICIPAL De Itapebi",
            "PREFEITURA MUNICIPAL De Itapetinga",
            "PREFEITURA MUNICIPAL De Itapicuru",
            "PREFEITURA MUNICIPAL De Itapitanga",
            "PREFEITURA MUNICIPAL De Itaquara",
            "PREFEITURA MUNICIPAL De Itarantim",
            "PREFEITURA MUNICIPAL De Itatim",
            "PREFEITURA MUNICIPAL De Itiruçu",
            "PREFEITURA MUNICIPAL De Itiúba",
            "PREFEITURA MUNICIPAL De Itororó",
            "PREFEITURA MUNICIPAL De Ituaçu",
            "PREFEITURA MUNICIPAL De Ituberá",
            "PREFEITURA MUNICIPAL De Iuiú",
            "PREFEITURA MUNICIPAL De Jaborandi",
            "PREFEITURA MUNICIPAL De Jacaraci",
            "PREFEITURA MUNICIPAL De Jacobina",
            "PREFEITURA MUNICIPAL De Jaguaquara",
            "PREFEITURA MUNICIPAL De Jaguarari",
            "PREFEITURA MUNICIPAL De Jaguaripe",
            "PREFEITURA MUNICIPAL De Jandaíra",
            "PREFEITURA MUNICIPAL De Jequié",
            "PREFEITURA MUNICIPAL De Jeremoabo",
            "PREFEITURA MUNICIPAL De Jiquiriçá",
            "PREFEITURA MUNICIPAL De Jitaúna",
            "PREFEITURA MUNICIPAL De João Dourado",
            "PREFEITURA MUNICIPAL De Juazeiro",
            "PREFEITURA MUNICIPAL De Jucuruçú",
            "PREFEITURA MUNICIPAL De Jussara",
            "PREFEITURA MUNICIPAL De Jussari",
            "PREFEITURA MUNICIPAL De Jussiape",
            "PREFEITURA MUNICIPAL De Lafaiete Coutinho",
            "PREFEITURA MUNICIPAL De Lagoa Real",
            "PREFEITURA MUNICIPAL De Laje",
            "PREFEITURA MUNICIPAL De Lajedão",
            "PREFEITURA MUNICIPAL De Lajedinho",
            "PREFEITURA MUNICIPAL De Lajedo Do Tabocal",
            "PREFEITURA MUNICIPAL De Lamarão",
            "PREFEITURA MUNICIPAL De Lapão",
            "PREFEITURA MUNICIPAL De Lauro De Freitas",
            "PREFEITURA MUNICIPAL De Lençóis",
            "PREFEITURA MUNICIPAL De Licínio De Almeida",
            "PREFEITURA MUNICIPAL De Livramento De Nossa Senhora",
            "PREFEITURA MUNICIPAL De Luís Eduardo Magalhães",
            "PREFEITURA MUNICIPAL De Macajuba",
            "PREFEITURA MUNICIPAL De Macarani",
            "PREFEITURA MUNICIPAL De Macaúbas",
            "PREFEITURA MUNICIPAL De Macururê",
            "PREFEITURA MUNICIPAL De Madre De Deus",
            "PREFEITURA MUNICIPAL De Maetinga",
            "PREFEITURA MUNICIPAL De Maiquinique",
            "PREFEITURA MUNICIPAL De Mairi",
            "PREFEITURA MUNICIPAL De Malhada",
            "PREFEITURA MUNICIPAL De Malhada De Pedras",
            "PREFEITURA MUNICIPAL De Manoel Vitorino",
            "PREFEITURA MUNICIPAL De Mansidão",
            "PREFEITURA MUNICIPAL De Maracás",
            "PREFEITURA MUNICIPAL De Maragogipe",
            "PREFEITURA MUNICIPAL De Maraú",
            "PREFEITURA MUNICIPAL De Marcionílio Souza",
            "PREFEITURA MUNICIPAL De Mascote",
            "PREFEITURA MUNICIPAL De Mata De São João",
            "PREFEITURA MUNICIPAL De Matina",
            "PREFEITURA MUNICIPAL De Medeiros Neto",
            "PREFEITURA MUNICIPAL De Miguel Calmon",
            "PREFEITURA MUNICIPAL De Milagres",
            "PREFEITURA MUNICIPAL De Mirangaba",
            "PREFEITURA MUNICIPAL De Mirante",
            "PREFEITURA MUNICIPAL De Monte Santo",
            "PREFEITURA MUNICIPAL De Morpará",
            "PREFEITURA MUNICIPAL De Morro Do Chapéu",
            "PREFEITURA MUNICIPAL De Mortugaba",
            "PREFEITURA MUNICIPAL De Mucugê",
            "PREFEITURA MUNICIPAL De Mucuri",
            "PREFEITURA MUNICIPAL De Mulungu Do Morro",
            "PREFEITURA MUNICIPAL De Mundo Novo",
            "PREFEITURA MUNICIPAL De Muniz Ferreira",
            "PREFEITURA MUNICIPAL De Muquém De São Francisco",
            "PREFEITURA MUNICIPAL De Muritiba",
            "PREFEITURA MUNICIPAL De Mutuípe",
            "PREFEITURA MUNICIPAL De Nazaré",
            "PREFEITURA MUNICIPAL De Nilo Peçanha",
            "PREFEITURA MUNICIPAL De Nordestina",
            "PREFEITURA MUNICIPAL De Nova Canaã",
            "PREFEITURA MUNICIPAL De Nova Fátima",
            "PREFEITURA MUNICIPAL De Nova Ibiá",
            "PREFEITURA MUNICIPAL De Nova Itarana",
            "PREFEITURA MUNICIPAL De Nova Redenção",
            "PREFEITURA MUNICIPAL De Nova Soure",
            "PREFEITURA MUNICIPAL De Nova Viçosa",
            "PREFEITURA MUNICIPAL De Novo Horizonte",
            "PREFEITURA MUNICIPAL De Novo Triunfo",
            "PREFEITURA MUNICIPAL De Olindina",
            "PREFEITURA MUNICIPAL De Oliveira Dos Brejinhos",
            "PREFEITURA MUNICIPAL De Ouriçangas",
            "PREFEITURA MUNICIPAL De Ourolândia",
            "PREFEITURA MUNICIPAL De Palmas De Monte Alto",
            "PREFEITURA MUNICIPAL De Palmeiras",
            "PREFEITURA MUNICIPAL De Paramirim",
            "PREFEITURA MUNICIPAL De Paratinga",
            "PREFEITURA MUNICIPAL De Paripiranga",
            "PREFEITURA MUNICIPAL De Pau Brasil",
            "PREFEITURA MUNICIPAL De Paulo Afonso",
            "PREFEITURA MUNICIPAL De Pé De Serra",
            "PREFEITURA MUNICIPAL De Pedrão",
            "PREFEITURA MUNICIPAL De Pedro Alexandre",
            "PREFEITURA MUNICIPAL De Piatã",
            "PREFEITURA MUNICIPAL De Pilão Arcado",
            "PREFEITURA MUNICIPAL De Pindaí",
            "PREFEITURA MUNICIPAL De Pindobaçu",
            "PREFEITURA MUNICIPAL De Pintadas",
            "PREFEITURA MUNICIPAL De Piraí Do Norte",
            "PREFEITURA MUNICIPAL De Piripá",
            "PREFEITURA MUNICIPAL De Piritiba",
            "PREFEITURA MUNICIPAL De Planaltino",
            "PREFEITURA MUNICIPAL De Planalto",
            "PREFEITURA MUNICIPAL De Poções",
            "PREFEITURA MUNICIPAL De Pojuca",
            "PREFEITURA MUNICIPAL De Ponto Novo",
            "PREFEITURA MUNICIPAL De Porto Seguro",
            "PREFEITURA MUNICIPAL De Potiraguá",
            "PREFEITURA MUNICIPAL De Prado",
            "PREFEITURA MUNICIPAL De Presidente Dutra",
            "PREFEITURA MUNICIPAL De Presidente Jânio Quadros",
            "PREFEITURA MUNICIPAL De Presidente Tancredo Neves",
            "PREFEITURA MUNICIPAL De Queimadas",
            "PREFEITURA MUNICIPAL De Quijingue",
            "PREFEITURA MUNICIPAL De Quixabeira",
            "PREFEITURA MUNICIPAL De Rafael Jambeiro",
            "PREFEITURA MUNICIPAL De Remanso",
            "PREFEITURA MUNICIPAL De Retirolândia",
            "PREFEITURA MUNICIPAL De Riachão Das Neves",
            "PREFEITURA MUNICIPAL De Riachão Do Jacuípe",
            "PREFEITURA MUNICIPAL De Riacho De Santana",
            "PREFEITURA MUNICIPAL De Ribeira Do Amparo",
            "PREFEITURA MUNICIPAL De Ribeira Do Pombal",
            "PREFEITURA MUNICIPAL De Ribeirão Do Largo",
            "PREFEITURA MUNICIPAL De Rio De Contas",
            "PREFEITURA MUNICIPAL De Rio Do Antonio",
            "PREFEITURA MUNICIPAL De Rio Do Pires",
            "PREFEITURA MUNICIPAL De Rio Real",
            "PREFEITURA MUNICIPAL De Rodelas",
            "PREFEITURA MUNICIPAL De Ruy Barbosa",
            "PREFEITURA MUNICIPAL De Salinas Da Margarida",
            "PREFEITURA MUNICIPAL De Salvador",
            "PREFEITURA MUNICIPAL De Santa Bárbara",
            "PREFEITURA MUNICIPAL De Santa Brígida",
            "PREFEITURA MUNICIPAL De Santa Cruz Cabrália",
            "PREFEITURA MUNICIPAL De Santa Cruz Da Vitória",
            "PREFEITURA MUNICIPAL De Santa Inês",
            "PREFEITURA MUNICIPAL De Santa Luzia",
            "PREFEITURA MUNICIPAL De Santa Maria Da Vitória",
            "PREFEITURA MUNICIPAL De Santa Rita De Cássia",
            "PREFEITURA MUNICIPAL De Santa Terezinha",
            "PREFEITURA MUNICIPAL De Santaluz",
            "PREFEITURA MUNICIPAL De Santana",
            "PREFEITURA MUNICIPAL De Santanópolis",
            "PREFEITURA MUNICIPAL De Santo Amaro",
            "PREFEITURA MUNICIPAL De Santo Antônio De Jesus",
            "PREFEITURA MUNICIPAL De Santo Estêvão",
            "PREFEITURA MUNICIPAL De São Desidério",
            "PREFEITURA MUNICIPAL De São Domingos",
            "PREFEITURA MUNICIPAL De São Felipe",
            "PREFEITURA MUNICIPAL De São Felix",
            "PREFEITURA MUNICIPAL De São Felix Do Coribe",
            "PREFEITURA MUNICIPAL De São Francisco Do Conde",
            "PREFEITURA MUNICIPAL De São Gabriel",
            "PREFEITURA MUNICIPAL De São Gonçalo Dos Campos",
            "PREFEITURA MUNICIPAL De São José Da Vitória",
            "PREFEITURA MUNICIPAL De São José Do Jacuípe",
            "PREFEITURA MUNICIPAL De São Miguel Das Matas",
            "PREFEITURA MUNICIPAL De São Sebastião Do Passé",
            "PREFEITURA MUNICIPAL De Sapeaçu",
            "PREFEITURA MUNICIPAL De Sátiro Dias",
            "PREFEITURA MUNICIPAL De Saubara",
            "PREFEITURA MUNICIPAL De Saúde",
            "PREFEITURA MUNICIPAL De Seabra",
            "PREFEITURA MUNICIPAL De Sebastião Laranjeiras",
            "PREFEITURA MUNICIPAL De Senhor Do Bonfim",
            "PREFEITURA MUNICIPAL De Sento Sé",
            "PREFEITURA MUNICIPAL De Serra Do Ramalho",
            "PREFEITURA MUNICIPAL De Serra Dourada",
            "PREFEITURA MUNICIPAL De Serra Preta",
            "PREFEITURA MUNICIPAL De Serrinha",
            "PREFEITURA MUNICIPAL De Serrolândia",
            "PREFEITURA MUNICIPAL De Simões Filho",
            "PREFEITURA MUNICIPAL De Sítio Do Mato",
            "PREFEITURA MUNICIPAL De Sítio Do Quinto",
            "PREFEITURA MUNICIPAL De Sobradinho",
            "PREFEITURA MUNICIPAL De Souto Soares",
            "PREFEITURA MUNICIPAL De Tabocas Do Brejo Velho",
            "PREFEITURA MUNICIPAL De Tanhaçu",
            "PREFEITURA MUNICIPAL De Tanque Novo",
            "PREFEITURA MUNICIPAL De Tanquinho",
            "PREFEITURA MUNICIPAL De Taperoá",
            "PREFEITURA MUNICIPAL De Tapiramutá",
            "PREFEITURA MUNICIPAL De Teixeira De Freitas",
            "PREFEITURA MUNICIPAL De Teodoro Sampaio",
            "PREFEITURA MUNICIPAL De Teofilândia",
            "PREFEITURA MUNICIPAL De Teolândia",
            "PREFEITURA MUNICIPAL De Terra Nova",
            "PREFEITURA MUNICIPAL De Tremedal",
            "PREFEITURA MUNICIPAL De Tucano",
            "PREFEITURA MUNICIPAL De Uauá",
            "PREFEITURA MUNICIPAL De Ubaíra",
            "PREFEITURA MUNICIPAL De Ubaitaba",
            "PREFEITURA MUNICIPAL De Ubatã",
            "PREFEITURA MUNICIPAL De Uibaí",
            "PREFEITURA MUNICIPAL De Umburanas",
            "PREFEITURA MUNICIPAL De Una",
            "PREFEITURA MUNICIPAL De Urandi",
            "PREFEITURA MUNICIPAL De Uruçuca",
            "PREFEITURA MUNICIPAL De Utinga",
            "PREFEITURA MUNICIPAL De Valença",
            "PREFEITURA MUNICIPAL De Valente",
            "PREFEITURA MUNICIPAL De Varzéa Da Roça",
            "PREFEITURA MUNICIPAL De Várzea Do Poço",
            "PREFEITURA MUNICIPAL De Várzea Nova",
            "PREFEITURA MUNICIPAL De Varzedo",
            "PREFEITURA MUNICIPAL De Vera Cruz",
            "PREFEITURA MUNICIPAL De Vereda",
            "PREFEITURA MUNICIPAL De Vitória Da Conquista",
            "PREFEITURA MUNICIPAL De Wagner",
            "PREFEITURA MUNICIPAL De Wanderley",
            "PREFEITURA MUNICIPAL De Wenceslau Guimarães",
            "PREFEITURA MUNICIPAL De Xique-Xique"
        ]
        # Layout
        self.grid_columnconfigure(0, weight=1)

        self.label_titulo = ctk.CTkLabel(
            self, text="Extração de Dados SESAB", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Container Login
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.frame_login.grid_columnconfigure(0, weight=1)

        self.entry_user = ctk.CTkEntry(
            self.frame_login, placeholder_text="Usuário SIGAF", height=40)
        self.entry_user.grid(row=0, column=0, padx=20,
                             pady=(20, 10), sticky="ew")

        self.entry_pass = ctk.CTkEntry(
            self.frame_login, placeholder_text="Senha", show="*", height=40)
        self.entry_pass.grid(row=1, column=0, padx=20,
                             pady=(10, 20), sticky="ew")

        # Seleção de Pasta
        self.btn_folder = ctk.CTkButton(self, text="Escolher Pasta de Destino",
                                        fg_color="transparent", border_width=2,
                                        command=self.selecionar_pasta, height=35)
        self.btn_folder.grid(row=2, column=0, padx=30, pady=(20, 5))

        self.label_pasta = ctk.CTkLabel(
            self, text="Nenhuma pasta selecionada", font=ctk.CTkFont(size=12), text_color="gray")
        self.label_pasta.grid(row=3, column=0, padx=30, pady=0)

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=(40, 10))
        self.progress_bar.set(0)

        self.label_status = ctk.CTkLabel(
            self, text="Pronto para iniciar", font=ctk.CTkFont(size=13))
        self.label_status.grid(row=5, column=0, padx=20, pady=5)

        # Botão Iniciar
        self.btn_run = ctk.CTkButton(self, text="INICIAR AUTOMAÇÃO",
                                     font=ctk.CTkFont(size=15, weight="bold"),
                                     height=45, command=self.iniciar_thread)
        self.btn_run.grid(row=6, column=0, padx=30, pady=(30, 20))

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.diretorio_destino = pasta
            exibicao = (pasta[:40] + '...') if len(pasta) > 40 else pasta
            self.label_pasta.configure(
                text=f"Destino: {exibicao}", text_color="white")

    def iniciar_thread(self):
        if not self.entry_user.get() or not self.entry_pass.get() or not self.diretorio_destino:
            messagebox.showwarning(
                "Campos Vazios", "Por favor, preencha o login e selecione a pasta!")
            return

        self.btn_run.configure(state="disabled")
        threading.Thread(target=self.executar_robo, daemon=True).start()

    def executar_robo(self):
        user = self.entry_user.get()
        pw = self.entry_pass.get()
        caminho_excel = os.path.join(
            self.diretorio_destino, "dados_prefeituras_ba.xlsx")

        nav = webdriver.Chrome()
        try:
            self.label_status.configure(text="Iniciando Navegador...")
            nav.get('https://sigaf.sesab.ba.gov.br')

            login(nav, user, pw)
            time.sleep(3)

            total = len(self.prefeituras_ba)

            for i, pref in enumerate(self.prefeituras_ba):
                self.label_status.configure(text=f"Extraindo: {pref}")

                # CHAMADA DA FUNÇÃO DE EXTRAÇÃO
                resultado = extrair_dados(nav, pref)

                if resultado:
                    # LÓGICA DE SALVAMENTO INCREMENTAL
                    try:
                        df_existente = pd.read_excel(caminho_excel)
                        df_novo = pd.concat(
                            [df_existente, pd.DataFrame([resultado])], ignore_index=True)
                    except FileNotFoundError:
                        df_novo = pd.DataFrame([resultado])

                    df_novo.to_excel(caminho_excel, index=False)

                # Atualiza interface
                porcentagem = (i + 1) / total
                self.progress_bar.set(porcentagem)
                time.sleep(1)  # Delay amigável para o servidor

            self.label_status.configure(
                text="Processo Concluído!", text_color="#2ecc71")
            messagebox.showinfo(
                "Sucesso", f"Extração finalizada!\nArquivo: {caminho_excel}")

            # Opcional: Abre a pasta ao finalizar
            os.startfile(self.diretorio_destino)

        except Exception as e:
            self.label_status.configure(
                text="Erro detectado", text_color="#e74c3c")
            messagebox.showerror("Erro Crítico", f"Erro: {str(e)}")
        finally:
            nav.quit()
            self.btn_run.configure(state="normal")


if __name__ == "__main__":
    app = AppRobo()
    app.mainloop()
