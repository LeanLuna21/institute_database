-- database: resources/Alas_test.db

UPDATE alumnos
SET dni = REPLACE(dni, '-', '') + 0
WHERE dni LIKE '%-%';

UPDATE pagos
SET January = 0;

UPDATE pagos
SET February = 0;

UPDATE pagos
SET fotocs = 4000;

SELECT * from pagos RIGHT JOIN alumnos 
ON alumnos.curso_id = pagos.curso_id
WHERE alumnos.legajo = 1001
GROUP BY alumnos.legajo;

UPDATE pagos
SET fotocs = 4000 
WHERE legajo = 1000;

SELECT April from pagos
WHERE legajo = 1000;

