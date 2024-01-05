CREATE TABLE cps.tbFornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    contato VARCHAR(255) NOT NULL
);

CREATE TABLE cps.tbProdutos (
    id_produto SERIAL PRIMARY KEY,
    estoque INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    id_fornecedor INT REFERENCES cps.tbFornecedor(id_fornecedor),
    id_categoria INT REFERENCES cps.tbCategoria(id_categoria)
);

CREATE TABLE cps.tbCategoria (
    id_categoria SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);


CREATE TABLE cps.tbSupermercado (
    id_supermercado SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    contato VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL
);

CREATE TABLE cps.tbPedidos (
    id_pedido SERIAL PRIMARY KEY,
    quantidade INT NOT NULL,
    id_supermercado INT REFERENCES cps.tbSupermercado(id_supermercado)
);

CREATE TABLE cps.tbPedido (
    id_pedido SERIAL PRIMARY KEY,
    quantidade INT NOT NULL
);


CREATE TABLE cps.tbPedidoProduto (
    id_produto INT REFERENCES cps.tbProdutos(id_produto),
    id_pedido INT REFERENCES cps.tbPedido(id_pedido),
    PRIMARY KEY (id_produto, id_pedido)
);

