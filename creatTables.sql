CREATE SEQUENCE medico_id_seq;
CREATE TABLE medico (
  id INT PRIMARY KEY DEFAULT nextval('medico_id_seq'),
  nome VARCHAR NOT NULL,
  crm VARCHAR UNIQUE NOT NULL,
  especializacao VARCHAR NOT NULL
);

CREATE SEQUENCE paciente_id_seq;
CREATE TABLE paciente (
  id INT PRIMARY KEY DEFAULT nextval('paciente_id_seq'),
  nome VARCHAR NOT NULL,
  cpf VARCHAR UNIQUE NOT NULL,
  data_de_nascimento DATE NOT NULL,
  sexo CHAR(1) NOT NULL
);