CREATE SCHEMA IF NOT EXISTS agriculturas;

USE agriculturas;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    ciudad VARCHAR(255) NOT NULL,
    provincia VARCHAR(255) NOT NULL,
    recinto VARCHAR(255) NOT NULL,
    nombre_finca VARCHAR(255) NOT NULL,
    canton VARCHAR(255) NOT NULL,
    parroquia VARCHAR(255) NOT NULL,
    ct_prepa_suelo VARCHAR(3) NOT NULL,
    ct_k510ha FLOAT NOT NULL,
    ct_k511ha FLOAT NOT NULL,
    ct_afecta_prod VARCHAR(3) NOT NULL,
    ct_riego VARCHAR(3) NOT NULL,
    su_fertilizada FLOAT NOT NULL,
    ct_fqui VARCHAR(3) NOT NULL,
    ct_fqui_npk FLOAT NOT NULL,
    ct_pqui VARCHAR(3) NOT NULL,
    su_plaguicidas FLOAT NOT NULL,
    ventas FLOAT NOT NULL,
    resultado_prediccion FLOAT NOT NULL
);


SELECT * from usuarios;


ALTER TABLE usuarios MODIFY COLUMN ct_afecta_prod VARCHAR(100);