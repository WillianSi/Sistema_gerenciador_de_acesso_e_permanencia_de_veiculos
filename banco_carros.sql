-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           8.0.22 - MySQL Community Server - GPL
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para projetocompgrafica
CREATE DATABASE IF NOT EXISTS `projetocompgrafica` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `projetocompgrafica`;

-- Copiando estrutura para tabela projetocompgrafica.carros
CREATE TABLE IF NOT EXISTS `carros` (
  `idCarros` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(45) DEFAULT NULL,
  `horaEntrada` varchar(50) DEFAULT NULL,
  `horaSaida` varchar(50) DEFAULT NULL,
  `dataEntrada` varchar(50) DEFAULT NULL,
  `dataSaida` varchar(50) DEFAULT NULL,
  `veiculoOficial` varchar(50) DEFAULT NULL,
  `veiculoProcurado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idCarros`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8;

-- Copiando dados para a tabela projetocompgrafica.carros: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `carros` DISABLE KEYS */;
INSERT INTO `carros` (`idCarros`, `placa`, `horaEntrada`, `horaSaida`, `dataEntrada`, `dataSaida`, `veiculoOficial`, `veiculoProcurado`) VALUES
	(1, 'BRA2E19', '21:26:38', '21:26:41', '2022-06-27', NULL, '0', 'Procurado'),
	(2, 'FUN-0972', '16:06:38', '20 : 38', '2022-06-28', '', 'Não autorizado', '1'),
	(4, 'BRA2E98', '15:19:11', '15:19:51', '2022-06-27', '2022-06-27', '1', '0'),
	(129, 'OJJ3984', '21 : 48', NULL, '30/06/2022', NULL, 'Autorizado', 'Procurado');
/*!40000 ALTER TABLE `carros` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
