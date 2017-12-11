DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `password` VARCHAR(100) NOT NULL,
  `email` VARCHAR(50) DEFAULT NULL UNIQUE,
  `create_at` DATETIME NOT NULL,
  `is_active` VARCHAR(1) DEFAULT 'N',
  `is_admin` VARCHAR(1) DEFAULT 'N',
  `snp_table` VARCHAR(200) DEFAULT NULL,
  `expr_table` VARCHAR(200) DEFAULT NULL,
  `desc_table` VARCHAR(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1, '佳绩正', '123', 'jiajizhen@test.com', '2017-11-30 11:38', 'Y', 'N', 'snp_mRNA_table', 'expr_gene_pos', 'locus_gene_mlocus');
UNLOCK TABLES;
/*
DROP TABLE IF EXISTS `link_table`;
CREATE TABLE `link_table`(
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(80) NOT NULL,
  `snp_table` VARCHAR(50) DEFAULT NULL,
  `expr_table` VARCHAR(50) DEFAULT NULL,
  `locus_table` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
*/

DROP TABLE IF EXISTS `test_users`;
CREATE TABLE `test_users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `password` VARCHAR(100) NOT NULL,
  `email` VARCHAR(50) DEFAULT NULL UNIQUE,
  `create_at` DATETIME NOT NULL,
  `is_active` VARCHAR(1) DEFAULT 'N',
  `is_admin` VARCHAR(1) DEFAULT 'N',
  `snp_table` VARCHAR(200) DEFAULT NULL,
  `expr_table` VARCHAR(200) DEFAULT NULL,
  `desc_table` VARCHAR(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;