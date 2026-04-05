DROP TABLE IF exists orcamento;
DROP TABLE IF exists invest_compra;
DROP TABLE IF exists invest_venda;


CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.ref = current_date;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE orcamento (id SERIAL PRIMARY KEY,
                    ref timestamp default current_date,
                    descricao varchar(60) not null,
                    preco money not null
                    );

CREATE TABLE invest_compra (id SERIAL PRIMARY KEY,
                        ref  timestamp default current_date,
                        ativo varchar(60) NOT NULL,
                        quant int NOT NULL,
                        preco money NOT NULL
                        );
CREATE TABLE invest_venda (id SERIAL PRIMARY KEY,
                        ref  timestamp default current_date,
                        ativo varchar(60) NOT NULL,
                        quant int NOT NULL,
                        preco money NOT NULL
                        );

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON orcamento
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON invest_compra
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON invest_venda
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();
