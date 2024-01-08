INSERT INTO cps.tbFornecedor (nome, contato)
SELECT 'x', 'x'
FROM cps.tbFornecedor
GROUP BY nome, contato
HAVING COUNT(*) = 0;

INSERT INTO cps.tbProdutos (estoque, nome, valor, id_fornecedor, id_categoria) VALUES 
(100, 'Produto1', 10.99, 1, 1);

INSERT INTO cps.tbCategoria (nome) VALUES 
('Categoria1');

INSERT INTO cps.tbSupermercado (nome, contato, endereco) VALUES 
('Supermercado1', 'Contato1', 'Endereco1');

INSERT INTO cps.tbPedido (quantidade) VALUES 
(5);

select * from cps.tbProdutos


DELETE FROM cps.tbFornecedor WHERE id_fornecedor = 1;
DELETE FROM cps.tbProdutos WHERE id_produto = X;
DELETE FROM cps.tbCategoria WHERE id_categoria = X;

DELETE FROM cps.tbFornecedor
WHERE NOT EXISTS (
    SELECT 1
    FROM cps.tbProdutos
    WHERE cps.tbProdutos.id_fornecedor = cps.tbFornecedor.id_fornecedor
); 

DELETE FROM cps.tbProdutos
WHERE estoque < 1; 


UPDATE cps.tbProdutos
SET estoque = 0
WHERE id_categoria = (
    SELECT id_categoria
    FROM cps.tbProdutos
    GROUP BY id_categoria
    HAVING MAX(estoque) < 5
)
AND estoque < 5; 


UPDATE cps.tbFornecedor
SET contato = 'NovoContato'
WHERE id_fornecedor = 2; 



SELECT *
FROM cps.tbFornecedor
WHERE id_fornecedor IN (
    SELECT id_fornecedor
    FROM cps.tbProdutos
    GROUP BY id_fornecedor
    HAVING COUNT(*) > x
); 

SELECT *
FROM cps.tbFornecedor
WHERE id_fornecedor IN (
    SELECT id_fornecedor
    FROM cps.tbProdutos
    WHERE estoque < x
); 

SELECT *
FROM cps.tbProdutos
WHERE valor > (
    SELECT AVG(valor)
    FROM cps.tbProdutos
); 

SELECT *
FROM cps.tbSupermercado
WHERE id_supermercado IN (
    SELECT id_supermercado
    FROM cps.tbPedidos
    GROUP BY id_supermercado
    HAVING COUNT(*) > 1); 

