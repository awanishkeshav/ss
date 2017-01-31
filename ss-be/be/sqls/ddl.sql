# API DB
drop database ssdb;
CREATE SCHEMA `ssdb` CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON `ssdb`.* TO `root`@localhost IDENTIFIED BY 'ss_dev';
FLUSH PRIVILEGES;


# Simulator DB
drop database simdb;
CREATE SCHEMA `simdb` CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON `simdb`.* TO `root`@localhost IDENTIFIED BY 'ss_dev';
FLUSH PRIVILEGES;