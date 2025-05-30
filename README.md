# AgendaMed
> Status do projeto: Em andamento

> Esse projeto nos foi proposto no 6º Semestre na disciplina de Tópicos Avançados de Banco de Dados

> Realizamos esse projeto juntos durante as aulas

### Tópicos
🔹[Explicação do tema escolhido](#pushpin-explicação-do-tema-escolhido)

🔹[Justificativa para cada banco usado no projeto e como S2 será implementado](#pencil2-justificativa-para-cada-banco-usado-no-projeto-e-como-S2-será-implementado)

🔹[Como executar o código](#space_invader-como-executar-o-código)

🔹[Desenvolvedores](#busts_in_silhouette-desenvolvedores)

## :pushpin: Explicação do tema escolhido
Escolhemos como tema o desenvolvimento de um Sistema de Gerenciamento de Consultas Médicas, destinado a clínicas médicas para gerenciar de forma eficiente agendamentos de pacientes, histórico de atendimentos, disponibilidade de médicos, dados de pacientes e médicos, entre outras funcionalidades essenciais para o funcionamento de uma clínica.

Após uma análise cuidadosa e várias discussões em grupo, decidimos seguir com essa ideia, pois ela nos permitiu explorar algo novo e inovador fora do contexto financeiro, que é uma área mais comum. O sistema de agendamento de consultas nos chamou a atenção pela complexidade e pela riqueza dos dados que iríamos manipular, além dos desafios interessantes envolvidos no processo de criação.

Um dos aspectos mais atrativos do projeto é a gestão de disponibilidade de médicos, que varia de acordo com cada paciente, além do controle de histórico de consultas, permitindo o acompanhamento da evolução de cada paciente ao longo do tempo. Isso inclui a verificação de situações específicas, como consultas passadas, agendamentos futuros, exames realizados e o gerenciamento completo das informações relacionadas a cada atendimento médico. A maneira como lidaremos com esses dados, de forma segura e eficiente, é um dos principais desafios e motivadores do projeto.

## :pencil2: Justificativa para cada banco usado no projeto e como S2 será implementado

### Justificativa para cada banco

**Banco Relacional (RDB): Supabase (PostgreSQL)**
Já trabalhamos com o Supabase e gostamos muito da nossa experiência, além de, ser fácil e didático de usar. No nosso sistema iremos integrar com Python, e como temos experiência já sabemos mais ou menos como usar e sua integração é bem simples utilizando bibliotecas.

**Banco Não Relacional 1 (Documentos): MongoDB Atlas**
O MongoDB Atlas é uma excelente opção para armazenar dados não estruturados ou dados em formato de documentos (JSON-like). Isso é útil para dados como históricos médicos ou consultas de pacientes que podem ter um formato variado e crescer de maneira dinâmica.

**Banco Não Relacional 2 (Colunas): Astra DB (Cassandra)**
Escolhemos o Cassandra depois de algumas pesquisas e concluímos que é excelente para cenários de grande volume de dados distribuídos e acesso rápido. Enxergamos nesse projeto que poderia ser usada para armazenar dados que precisam ser consultados em larga escala ou rapidamente (ex: registros de horários de consultas, disponibilidade de médicos, etc.). Além disso, será a nossa primeira vez com o Cassandra e queriamos tentar algo novo também nesse projeto.

**Armazenamento de Mensagens: SQLite**
SQLite é um banco de dados relacional leve e embutido, perfeito para armazenar mensagens temporárias ou registros de eventos durante o processamento de tarefas.
Ele é fácil de configurar, não exige servidor e pode ser utilizado diretamente no backend sem necessidade de infraestrutura adicional. Isso ajuda a salvar o estado das mensagens processadas pelo RabbitMQ e garantir que todas as mensagens sejam tratadas corretamente.

**Mensageria: RabbitMQ Cloud**
RabbitMQ é uma das melhores opções de mensageria para sistemas distribuídos, permitindo comunicação assíncrona entre serviços. Ele ajuda a gerenciar as interações entre os serviços de agendamento de consultas, atualizações de status, geração de dados fictícios, etc.

### Como S2 será implementado
Iremos utilizar quatro módulos, um simples para direcionamento, onde dado a mensagem ele encaminhará para o módulo específico, e os outros três para tratamento de dados um para cada banco que iremos utilizar.

## :space_invader: Como executar o código
Para executar nosso código o usuário precisa seguir as seguintes etapas:
1. Fazer cadastro nas plataformas que estamos utilizando para acessar o banco de dados, como o Supabase para o SQL, o DataStax Astra para o Cassandra e o ____ para o MongoDB.
2. Ao fazer cadastro nesses sites você pode colocar a massa de dados que disponibilizamos ou inserir os dados manualmente nesses bancos. Atenção, os dados no Cassandra são colocados ao adicionar ou editar uma disponibilidade de um médico enquanto está rodando o código.
3. Ao ter os sites dos bancos abertos com o banco de dados, você precisa ter o Docker instalado na sua máquina para conseguir rodar a mensageria que estamos utilizando no caso o RabbitMQ.
4. Ao instalar o Docker acesse [http://localhost:15672/#/queues](http://localhost:15672/#/queues) para ver o funcionamento das filas.
5. Com os passos a cima concluídos só rodar em um terminal o consumidor e em outro a main como explicamos no tópico **Iniciando Produtor e Consumidor**

Os passos a cima são apenas uma explicação rápida de como se orientar, também sugerimos uma leitura nos seguintes tópicos para se orientar melhor.

### Incluindo massa de dados

#### Supabase 
Acesse o site [https://supabase.com](https://supabase.com) e utilize os arquivos `medicos.csv` e `pacientes.csv` disponíveis no repositório para importar os dados nas tabelas correspondentes.  
Nos prints abaixo, mostramos onde fazer o upload desses arquivos para importar os dados diretamente no Supabase, sem necessidade de alterações.

![Imagem do WhatsApp de 2025-05-29 à(s) 21 24 28_98ea0ab5](https://github.com/user-attachments/assets/e2436e1f-702e-4816-a989-17acba61fa8f)

![Imagem do WhatsApp de 2025-05-29 à(s) 21 25 40_3b504d00](https://github.com/user-attachments/assets/755cbff5-b70b-4038-91e0-12e271a096c1)

#### Mongo Atlas  
Acesse o site [https://cloud.mongodb.com](https://cloud.mongodb.com) e utilize os arquivos `exames_mongo.json` e `laudos_mongo.json` disponíveis no repositório para importar os dados nas coleções correspondentes.  
Nos prints abaixo, mostramos onde inserir o conteúdo desses arquivos. Basta copiar (Ctrl + C) e colar (Ctrl + V) diretamente, sem necessidade de alterações.

![insertMongo1](https://github.com/user-attachments/assets/6f8b71d8-a14a-4b76-860b-cc7ea9adae58)

![insertMongo2](https://github.com/user-attachments/assets/21abc42f-eb58-46a3-901c-5e87f41c4eda)

### Instalando e Iniciando o Docker

1. Acesse o site oficial do Docker e baixe a versão correspondente ao seu sistema operacional:
   [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Após o download, instale o Docker Desktop normalmente, seguindo as instruções do instalador.

3. Finalizada a instalação, **reinicie o computador** se for solicitado.

4. Abra o Docker Desktop e aguarde até que o serviço seja inicializado completamente (ícone na bandeja do sistema deve indicar que está rodando).

5. Para verificar se o Docker está funcionando corretamente, abra um terminal e digite:

   ```bash
   docker --version
   ```

   Se tudo estiver certo, o terminal exibirá a versão do Docker instalada.

### Iniciando Produtor e Consumidor

Abra o terminal do seu computador (PowerShell, terminal do VS Code, etc.) e siga os passos abaixo:
1. Inicie o **consumidor** em uma aba, executando o comando:
   ```bash
   python -m src.s2.consumidor
   ```
2. Mantenha essa aba aberta e, em uma nova aba do terminal, inicie o **produtor** com o comando:
   ```bash
   python -m src.s1.main
   ```
O produtor será responsável por exibir os menus do sistema e permitir a execução das operações disponíveis.


## :busts_in_silhouette: Desenvolvedores
| [<img loading="lazy" src="https://github.com/Mariah-Gomes/ProjetoCompMovel1/assets/141663285/e6827fd1-d8fe-4740-b6fc-fbbfccd05752" width=115><br><sub>Mariah Santos Gomes</sub>](https://github.com/Mariah-Gomes) | [<img loading="lazy" src="https://github.com/Mariah-Gomes/ProjetoCompMovel1/assets/141663285/66d7e656-b9e4-43b7-94fa-931b736df881" width=115><br><sub>Iago Rosa de Oliveira</sub>](https://github.com/iagorosa28) |
| :---: | :---: |

### Dados dos Desenvolvedores
Iago Rosa de Oliveira R.A.: 22.224.027-7

Mariah Santos Gomes R.A.: 22.224.026-8

