SET FOREIGN_KEY_CHECKS=0;
SELECT Concat('TRUNCATE TABLE ',table_schema,'.',TABLE_NAME, ';')
FROM INFORMATION_SCHEMA.TABLES where  table_schema in ('ssdb');
SET FOREIGN_KEY_CHECKS=1;