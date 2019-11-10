-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 09-Nov-2019 às 18:14
-- Versão do servidor: 10.1.35-MariaDB
-- versão do PHP: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scemm`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `esta_vencido` (`data_venc` DATE) RETURNS TINYINT(1) BEGIN
	DECLARE retorno TINYINT(1);
    SET retorno=0;
	IF data_venc < CURRENT_DATE()
    THEN
		SET retorno = 1;
	END IF;
    RETURN retorno;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `valida_cnpj` (`cnpj` VARCHAR(14)) RETURNS TINYINT(4) BEGIN

	DECLARE indice, soma, dig1, dig2 INT;

	
	SET indice = 1;
	SET soma = 0;

	WHILE (indice <= 12) DO
		IF (indice <= 4) THEN
			SET soma = soma + CAST(SUBSTRING(cnpj, indice, 1) AS UNSIGNED) * (6 - indice);
			SET indice = indice + 1;
		ELSE
			SET soma = soma + CAST(SUBSTRING(cnpj, indice, 1) AS UNSIGNED) * (14 - indice);
			SET indice = indice + 1;
		END IF;
	END WHILE;

	SET dig1 = 11 - (soma % 11);
	IF dig1 > 9 THEN
		SET dig1 = 0;
	END IF;

	
	SET indice = 1;
	SET soma = 0;

 

	WHILE (indice <= 13) DO
		IF (indice <= 5) THEN
			SET soma = soma + CAST(SUBSTRING(cnpj, indice, 1) AS UNSIGNED) * (7 - indice);
			SET indice = indice + 1;
		ELSE
			SET soma = soma + CAST(SUBSTRING(cnpj, indice, 1) AS UNSIGNED) * (15 - indice);
			SET indice = indice + 1;
		END IF;
	END WHILE;

	SET dig2 = 11 - (soma % 11);
	IF dig2 > 9 THEN
		SET dig2 = 0;
	END IF;

	
	IF ((dig1 = SUBSTRING(cnpj, CHAR_LENGTH(cnpj)-1, 1))
	AND (dig2 = SUBSTRING(cnpj, CHAR_LENGTH(cnpj), 1))) THEN
		RETURN TRUE;
	ELSE
		RETURN FALSE;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `valida_cpf` (`cpf` VARCHAR(11)) RETURNS TINYINT(1) BEGIN
		DECLARE indice int;
		DECLARE soma int;
		DECLARE dig1 int;
		DECLARE dig2 int;
		DECLARE cpf_temp varchar(11);
		DECLARE digitos_iguais char(1);
		DECLARE resultado tinyint(1);
		set resultado = 0;
		set cpf_temp = SUBSTRING(cpf, 1, 1);
		set indice = 1;
		set digitos_iguais = 'S';
	WHILE (indice <= 11) DO
		IF SUBSTRING(cpf, indice, 1) <> cpf_temp THEN
			set digitos_iguais = 'N';
		END IF;
			set indice = indice + 1;
	END WHILE;
	IF digitos_iguais = 'N' THEN
		set soma = 0;
		set indice = 1;
		WHILE (indice <= 9) DO
			set soma = soma + CAST(SUBSTRING(cpf, indice, 1) AS UNSIGNED) * (11 - indice);
			set indice = indice +1;
		END WHILE;
		set dig1 = 11 - (soma % 11);
		IF dig1 > 9 THEN
			set dig1 = 0;
		END IF;
		set soma = 0;
		set indice = 1;
		WHILE (indice <= 10) DO
			set soma = soma + CAST(SUBSTRING(cpf, indice, 1) AS UNSIGNED) * (12 - indice);
			set indice = indice + 1;
		END WHILE; 
		set dig2 = 11 - (soma % 11);
		IF dig2 > 9 THEN
			set dig2 = 0;
		END IF;

		IF (dig1 = SUBSTRING(cpf, LENGTH(cpf)-1, 1)) AND (dig2 = SUBSTRING(cpf,
			LENGTH(cpf), 1)) THEN
			set resultado = 1;
		ELSE
			set resultado = 0;
		END IF;
	END IF;
 RETURN resultado;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `valida_telefone` (`tel` VARCHAR(14)) RETURNS TINYINT(1) BEGIN
	DECLARE retorno tinyint(1);
	set retorno = 0;

	IF (tel regexp'((10)|([1-9][1-9]))(([2-9][0-9]{3}[0-9]{4})|([6-9][0-9]{4}[0-9]{4}))') THEN
		set retorno = 1;
	ELSE
		set retorno = 0;
	END IF;
	RETURN retorno;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `entidade`
--

CREATE TABLE `entidade` (
  `id_entidade` int(10) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `cnpj` varchar(14) NOT NULL,
  `telefone` varchar(13) NOT NULL,
  `endereco` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `entidade`
--

INSERT INTO `entidade` (`id_entidade`, `nome`, `cnpj`, `telefone`, `endereco`) VALUES
(1, 'AAPNENSEL', '15415743000108', '4230862690', 'Rua Alguma Coisa, 1234');

--
-- Acionadores `entidade`
--
DELIMITER $$
CREATE TRIGGER `validar_entidade_insert` BEFORE INSERT ON `entidade` FOR EACH ROW BEGIN
	IF (SELECT valida_telefone(new.`telefone`))=0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone Incorreto!';
	END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `validar_entidade_update` BEFORE UPDATE ON `entidade` FOR EACH ROW BEGIN
	IF (SELECT valida_telefone(new.`telefone`))=0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Telefone Incorreto!';
	END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `entrada`
--

CREATE TABLE `entrada` (
  `entrada_id` int(10) NOT NULL,
  `data_ent` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_id` int(10) NOT NULL,
  `item_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `entrada`
--

INSERT INTO `entrada` (`entrada_id`, `data_ent`, `usuario_id`, `item_id`) VALUES
(1, '2019-09-18 08:58:26', 18, 18),
(2, '2019-09-18 08:58:26', 18, 12),
(4, '2019-09-19 12:59:22', 18, 21),
(5, '2019-09-19 12:59:30', 18, 21),
(6, '2019-09-19 13:40:06', 18, 37),
(7, '2019-09-19 13:46:20', 18, 38),
(8, '2019-09-19 13:49:27', 18, 39),
(9, '2019-09-19 13:51:49', 18, 40),
(10, '2019-09-19 13:52:45', 18, 41),
(11, '2019-09-19 13:55:38', 18, 42),
(12, '2019-09-19 13:56:56', 18, 43),
(13, '2019-09-19 14:19:24', 18, 44),
(14, '2019-09-19 16:40:56', 18, 45),
(15, '2019-09-19 16:44:17', 18, 47),
(16, '2019-09-19 21:35:35', 18, 14),
(17, '2019-09-19 22:29:30', 18, 48),
(18, '2019-09-26 19:17:12', 18, 49),
(19, '2019-09-26 19:19:15', 18, 50),
(20, '2019-10-01 11:10:55', 18, 51),
(21, '2019-10-03 09:37:00', 18, 24),
(22, '2019-10-03 09:37:01', 18, 24),
(23, '2019-10-03 10:30:03', 18, 40),
(24, '2019-10-03 16:25:42', 18, 27),
(25, '2019-10-03 16:25:54', 18, 27),
(26, '2019-10-04 14:33:20', 18, 14),
(27, '2019-10-04 18:33:18', 18, 52),
(28, '2019-10-04 18:36:51', 18, 54),
(29, '2019-10-04 18:38:53', 18, 55),
(30, '2019-10-04 18:42:59', 18, 56),
(31, '2019-10-04 18:43:50', 18, 57),
(32, '2019-10-04 18:45:45', 18, 58),
(33, '2019-10-04 18:48:02', 18, 59),
(34, '2019-10-04 18:52:43', 18, 58),
(35, '2019-10-06 10:33:15', 18, 52),
(36, '2019-10-06 10:33:45', 18, 52),
(37, '2019-10-06 10:33:48', 18, 52),
(38, '2019-10-06 10:33:50', 18, 52),
(39, '2019-10-08 11:26:25', 18, 60),
(40, '2019-10-08 11:28:09', 18, 60);

-- --------------------------------------------------------

--
-- Estrutura da tabela `item`
--

CREATE TABLE `item` (
  `item_id` int(10) NOT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `lote` varchar(30) DEFAULT NULL,
  `qtdItem` int(10) DEFAULT NULL,
  `qtdMinima` int(10) DEFAULT NULL,
  `dataVenc` date DEFAULT NULL,
  `peso` decimal(14,2) DEFAULT NULL,
  `unidade` varchar(10) DEFAULT NULL,
  `nomeFabricante` varchar(50) DEFAULT NULL,
  `fornecedor` varchar(20) DEFAULT NULL,
  `excluido` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `item`
--

INSERT INTO `item` (`item_id`, `nome`, `lote`, `qtdItem`, `qtdMinima`, `dataVenc`, `peso`, `unidade`, `nomeFabricante`, `fornecedor`, `excluido`) VALUES
(1, 'dipirona', 'abc123456', 22, 7, '2017-03-20', NULL, NULL, NULL, NULL, 0),
(10, 'omeprazol', 'o123', 19, 3, '2020-03-20', NULL, NULL, 'ems', 'fleming', 0),
(11, 'fluimucil', 'f123', 80, 4, '2020-03-20', NULL, NULL, 'ems', 'fleming', 0),
(12, 'anador', 'a123', 94, 3, '2020-03-20', NULL, NULL, 'ems', 'fleming', 0),
(13, 'anador', 'a234', 19, 3, '2020-03-20', NULL, NULL, 'ems', 'fleming', 0),
(14, 'dipirona', 'dip123', 90, 7, '2020-03-20', '150.26', 'cp', 'ems', 'fleming', 0),
(17, 'dipirona', 'dip12345', 2, 7, '2020-03-20', '150.30', 'cp', 'ems', 'fleming', 0),
(18, 'anador', 'a789', 497, 3, '2019-11-20', NULL, NULL, 'ems', 'fleming', 0),
(19, 'dipirona', 'dip789123', 50, 7, '2020-03-20', '150.00', 'mg/ml', 'ems', 'fleming', 0),
(20, 'anador', 'ana123', 500, 3, '2020-03-20', '5.00', 'ml/g', 'ems', 'fleming', 0),
(21, 'anador', 'anador123', 52, 3, '2020-02-20', '150.00', 'g', 'ems', 'fleming', 0),
(22, 'anador', 'anbc526', 6, 3, '2020-02-20', '25.00', 'g', 'ems', 'fleming', 0),
(23, 'anador', 'bdncm5256', 50, 3, '2020-02-20', '36.00', 'g', 'ems', 'fleming', 0),
(24, 'dipirona', 'kmdjbs464', 21, 7, '2019-09-17', '150.00', 'mg', 'ems', 'fleming', 1),
(25, 'dipirona', 'abcd', 603, 7, '2020-03-20', '130.00', 'mg', 'ems', 'fleming', 0),
(26, 'dipirona', 'casadajoana', 50, 7, '2020-03-20', '150.00', 'ms', 'ems', 'fleming', 0),
(27, 'dipirona', 'macarrao', 62, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(28, 'dipirona', 'pantera', 520, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(29, 'dipirona', 'kelvin', 500, 7, '2020-03-20', '150.00', 'mg', 'ems', 'Fleming', 0),
(30, 'dipirona', 'lebre', 620, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(31, 'anador', 'peroba', 620, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(32, 'anador', 'amricota', 560, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(33, 'dipirona', 'budega', 362, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(34, 'anador', 'madeira', 362, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(35, 'anador', 'montecarlo', 236, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(36, 'anador', 'casagrande', 236, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(37, 'dipirona', 'vemnemim', 653, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(38, 'diazepan', 'amd', 265, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(39, 'diazepan', 'marica', 2561, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(40, 'omeprazol', 'gigante', 20, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(41, 'omeprazol', 'mascara', 320, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(42, 'omeprazol', 'mascote', 360, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(43, 'omeprazol', 'cobeado', 315, 3, '2020-02-20', '150.00', 'mg', 'ems', 'popular', 0),
(44, 'carbomazepina', 'maxixe', 362, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(45, 'dipirona', 'dipdip', 50, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(47, 'dipirona', 'gatobranco', 22, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(48, 'dipirona', 'casabela123', 0, 7, '2020-03-20', '150.50', 'mg', 'ems', 'Fleming', 0),
(49, 'dipirona', 'dipdip123', 18, 7, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(50, 'carbomazepina', 'monteclaro', 23, 3, '2020-03-20', '150.00', 'mg', 'ems', 'fleming', 0),
(51, 'dipirona', 'remedio123', 0, 7, '2019-10-30', '125.00', 'mg', 'ams', 'nissei', 0),
(52, 'dipirona', 'lotus', 562, 7, '2020-03-20', '150.50', 'mg/ml', 'ems', 'fleming', 0),
(53, 'Dipirona', 'doidera', 563, 7, '2020-03-20', '150.65', NULL, NULL, NULL, NULL),
(54, 'anador', 'tomate', 800, 3, '2020-03-20', '0.00', '', '', '', 0),
(55, 'omeprazol', 'capivara', 62, 3, '2020-03-20', '0.00', '', '', '', 0),
(56, 'dipirona', 'viva', 54, 7, '2020-03-20', '150.60', 'mg/ml', '', '', 0),
(57, 'dipirona', 'raduque', 54, 7, '2020-03-20', '150.62', 'mg/ml', '', '', 0),
(58, 'dipirona', 'dama', 391, 7, '2020-03-20', '156.59', 'mg/ml', 'ems', 'fleming', 0),
(59, 'fluimucil', 'drivex', 63, 4, '2020-03-20', '130.25', 'mg', '', '', 0),
(60, 'dipirona', 'kilo', 50, 7, '2020-03-20', '150.00', 'mg/ml', 'ems', 'fleming', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `paciente`
--

CREATE TABLE `paciente` (
  `paciente_id` int(10) NOT NULL,
  `nome` varchar(15) NOT NULL,
  `sobrenome` varchar(40) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `rg` varchar(10) NOT NULL,
  `data_nasc` date NOT NULL,
  `entidade_id` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `paciente`
--

INSERT INTO `paciente` (`paciente_id`, `nome`, `sobrenome`, `cpf`, `rg`, `data_nasc`, `entidade_id`) VALUES
(13, 'guilherme', '', '08263576954', '555555555', '2019-10-02', NULL),
(17, 'janaina', 'silva', '41876638869', '144779347', '1991-10-30', NULL),
(20, 'oseias', 'chagas', '37972874883', '144779347', '2000-10-09', NULL);

-- --------------------------------------------------------

--
-- Estrutura da tabela `prescricao`
--

CREATE TABLE `prescricao` (
  `id_Prescrição` int(10) NOT NULL,
  `nomeItem` varchar(30) NOT NULL,
  `qtdAdm` int(10) NOT NULL,
  `fazUso` tinyint(1) NOT NULL DEFAULT '0',
  `paciente_id` int(10) NOT NULL,
  `usuario_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `prescricao`
--

INSERT INTO `prescricao` (`id_Prescrição`, `nomeItem`, `qtdAdm`, `fazUso`, `paciente_id`, `usuario_id`) VALUES
(73, 'dipirona', 50, 1, 17, 18),
(267, 'DIPIRONA', 5, 1, 13, 18),
(268, 'ANAdor', 3, 1, 13, 18),
(302, 'dipirona', 2, 1, 20, 18),
(303, 'omeprazol', 3, 1, 20, 18),
(304, 'diazepaN', 2, 0, 20, 18);

-- --------------------------------------------------------

--
-- Estrutura da tabela `saida`
--

CREATE TABLE `saida` (
  `saida_id` int(10) NOT NULL,
  `qtdPrescrita` int(10) DEFAULT NULL,
  `qtdSaida` int(10) DEFAULT NULL,
  `qtdRestante` int(11) DEFAULT NULL,
  `dataSaida` date DEFAULT NULL,
  `descarte` tinyint(1) DEFAULT NULL,
  `usuario_id` int(10) DEFAULT NULL,
  `prescricao_id` int(10) DEFAULT NULL,
  `paciente_id` int(10) DEFAULT NULL,
  `item_id` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `saida`
--

INSERT INTO `saida` (`saida_id`, `qtdPrescrita`, `qtdSaida`, `qtdRestante`, `dataSaida`, `descarte`, `usuario_id`, `prescricao_id`, `paciente_id`, `item_id`) VALUES
(42, 2, 2, 0, '2019-11-08', NULL, 18, 302, 20, 1),
(43, 3, 3, 0, '2019-11-08', NULL, 18, 303, 20, 10),
(44, 2, 2, 0, '2019-11-07', NULL, 18, 302, 20, 1),
(45, 3, 3, 0, '2019-11-07', NULL, 18, 303, 20, 10),
(47, 3, 3, 0, '2019-11-06', NULL, 18, 303, 20, 10),
(50, 2, 1, 0, '2019-11-09', NULL, 18, 302, 20, 1),
(51, 3, 1, 0, '2019-11-09', NULL, 18, 303, 20, 10),
(52, 50, 50, 0, '2019-11-09', NULL, 18, 73, 17, 1),
(53, 5, 5, 0, '2019-11-09', NULL, 18, 267, 13, 1),
(54, 3, 3, 0, '2019-11-09', NULL, 18, 268, 13, 12);

-- --------------------------------------------------------

--
-- Estrutura da tabela `usuario`
--

CREATE TABLE `usuario` (
  `usuario_id` int(10) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `senha` varchar(94) NOT NULL,
  `eadmin` tinyint(1) DEFAULT '0',
  `excluido` tinyint(1) DEFAULT '0',
  `entidade_id` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `usuario`
--

INSERT INTO `usuario` (`usuario_id`, `nome`, `senha`, `eadmin`, `excluido`, `entidade_id`) VALUES
(18, 'ADMIN', 'pbkdf2:sha256:150000$p6L2Pkow$e3eb5662d9ec968651bf5fb8a29f10f8d60cf62122465b20945297518062fe89', 1, NULL, NULL),
(19, 'MARIA', 'pbkdf2:sha256:150000$VtrRVckO$aac6fdf1720d593f39717f2f6131307946e0087e6fd3ea5f5b333194f8a7dc59', 0, 0, NULL),
(21, 'pedro', 'pbkdf2:sha256:150000$nnREElXT$49ff7f36af731799136451e37ac8d3ff6223f768c85238ed229ea93cd09e625e', 1, NULL, NULL),
(22, 'carlos', 'pbkdf2:sha256:150000$XXKb1rHg$e7ba3130a003857cb34c76ab7094592f0d8d3d31eb493bc4b5d2ad299a4bbd64', 1, NULL, NULL),
(23, 'tiago', 'pbkdf2:sha256:150000$ySSE3Ws1$70a32e85bcc5e91e9f77a08a58b761e2e18a982ab325383f647b28e1a6e501fe', 1, NULL, NULL),
(24, 'CARDOZO', 'pbkdf2:sha256:150000$0h2QWGRN$fb17e897b62bb265db2597ad2325823031bc500581f9c7c1daea687878c59dc6', 0, 1, NULL),
(26, 'carlao', 'pbkdf2:sha256:150000$5f3Z7hFT$f758cf69722b51372ea1eb35de2edf9023052d9a6922729b1f1aa7d0a70f2f5e', 1, NULL, NULL),
(27, 'marcelo', 'pbkdf2:sha256:150000$iiuoD3r4$e891d4242b693f2effcf1ca30c15b997c0d67d6d5ae3f0e1013870a99ae090e8', 1, NULL, NULL),
(28, 'maricota', 'pbkdf2:sha256:150000$HX3HaGCz$76fe09c31ae665e31f532c8d867e2bbb612ebb42dadc1ebb91b040c9b5270d25', 0, NULL, NULL),
(29, 'pedroso', 'pbkdf2:sha256:150000$Z41UvGL2$c233aa42109916459c2ecff74480d75c272070486f29d131217bb52cd910a0bb', 1, NULL, NULL),
(30, 'madalena', 'pbkdf2:sha256:150000$RZEwe3bU$9b22b2e24aa2a3de1a590753c72865ce5b2e3ad0a16537ce9a57321b7572fef4', 1, NULL, NULL),
(31, 'carlito', 'pbkdf2:sha256:150000$EBqNodwM$1c4197547f37e202ba6f726aef8441f8cc144b0e1763d6f15fc2e08861c57be9', 1, NULL, NULL),
(32, 'genoveva', 'pbkdf2:sha256:150000$RylZL4Cb$4cd3c051eabc04020d3408d9fd68f147b68a21e28725c2d71eb42f830e361bbd', 0, NULL, NULL),
(33, 'genivaldo', 'pbkdf2:sha256:150000$Y7uSeRDd$f988b9f6e35e6a8e3e34ddb7648172e7c491caa01fa15aeac973427ba7e0fb01', 0, NULL, NULL),
(34, 'marieta', 'pbkdf2:sha256:150000$xOh510Ag$d93f285b23626be328750a46ae31c5e110cb521e8035ecb75c6135f1c32e86a0', 1, NULL, NULL),
(35, 'JOAO', 'pbkdf2:sha256:150000$EHp4eifh$2250d9fad0d8acc947640e92ad7251ba267e8b0f58e27370c802542a717dd282', 0, 0, NULL),
(36, 'benedicto', 'pbkdf2:sha256:150000$eRL9lRPG$428884b0fdefef5e35ee31b29d19bc9b95f08f98adcb8b1ce62b694d5fcc0deb', 1, NULL, NULL),
(37, 'joao2536', 'pbkdf2:sha256:150000$kGPDYBvJ$a09c9d50827292e2e6aa573c1ba09b9448dcd57087275f21644ed98f5d73f21d', 1, NULL, NULL),
(38, 'joao25635', 'pbkdf2:sha256:150000$Ho6FpzzZ$9786bd1e90960891f9eb35ea6f8f4037f706fc3f21ea99ca34558a065932d93f', 1, NULL, NULL),
(39, 'casebrino', 'pbkdf2:sha256:150000$GpweSznl$9c96e3bd7149c8c886f433036c4aabe025bc8f5f6b6992403d13772e8f665756', 1, NULL, NULL),
(40, 'LUISFERNANDO', 'pbkdf2:sha256:150000$6cfKs1p8$6c8ef8c3e70a50e4080ddac341adb592c309fc0739081fe265614c0dcfe7ff10', 1, 0, NULL),
(41, 'JOAODAVI', 'pbkdf2:sha256:150000$PBKC6O6K$9182d611f4bec876f6f932afc7b3bc8018e8b9f54161ecfc69533bc5b8435e8e', 1, NULL, NULL),
(42, 'JOAOMARIA', 'pbkdf2:sha256:150000$JGt4hCiD$9f845603b8ce8b5bb0b959c523988676aea796690d4e60fc02b897336ec6e0c9', 1, 1, NULL),
(43, 'MARIONETE', 'pbkdf2:sha256:150000$bIiAWaWf$8e492bed8220faa8d2166f4228ed2028ab5de87240cbbbcadea2e98d84be474b', 0, 0, NULL),
(44, 'idomar', 'pbkdf2:sha256:150000$Q2Jtc82a$91b3a33afc48ca922d5a3d3be13362403e1039ac35862243b442eec2130b2db8', 1, NULL, NULL),
(45, 'ANA123', 'pbkdf2:sha256:150000$uSkYlP6o$acba5353c77bc34a6440f4dfd4f359a7dd4fb85991b89a6315081ecaac1e26a9', 0, NULL, NULL),
(46, 'INDOMAR', 'pbkdf2:sha256:150000$EMfdzBsi$8cfe7cea63452b4514c7bf20a32c685a91a4b64d4f69488ac09e8f332cd90232', 0, NULL, NULL),
(47, 'mariaCareta', 'pbkdf2:sha256:150000$uoErjy3g$1f6fc12f5fa102dcb79c247fc13d26ee77074dd0b3b9ddd00fe72befb2d1009f', 1, NULL, NULL),
(49, 'maqiavel', 'pbkdf2:sha256:150000$WIcJuCll$ab403b54be3cdb7f94d83d3254391149389183686fef3d997c97d88af45985d7', 1, 0, NULL),
(50, 'oseias', 'pbkdf2:sha256:150000$3WP9EGGP$b8a4ad0f0d679edcbbb5944b392d65df5d6ada7ee3eb5f0d13c5e8845c7e5734', 1, 0, NULL),
(51, 'mariaTereza', 'pbkdf2:sha256:150000$30o8HCoX$9df99dad4057e58b472830e79298d24ace75fbd7bdd3ca98bcb47726d46a5bcb', 1, 0, NULL),
(52, 'carlosferreira', 'pbkdf2:sha256:150000$GPrJhAwo$82ccc04cc31afd0286c8327eeb9483e2c75267752c5525b11c57365547b8c196', 0, 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `entidade`
--
ALTER TABLE `entidade`
  ADD PRIMARY KEY (`id_entidade`);

--
-- Indexes for table `entrada`
--
ALTER TABLE `entrada`
  ADD PRIMARY KEY (`entrada_id`),
  ADD KEY `fk_1` (`usuario_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`item_id`),
  ADD UNIQUE KEY `lote` (`lote`);

--
-- Indexes for table `paciente`
--
ALTER TABLE `paciente`
  ADD PRIMARY KEY (`paciente_id`),
  ADD UNIQUE KEY `cpf` (`cpf`),
  ADD UNIQUE KEY `entidade_id` (`entidade_id`);

--
-- Indexes for table `prescricao`
--
ALTER TABLE `prescricao`
  ADD PRIMARY KEY (`id_Prescrição`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `paciente_id` (`paciente_id`);

--
-- Indexes for table `saida`
--
ALTER TABLE `saida`
  ADD PRIMARY KEY (`saida_id`),
  ADD KEY `prescricao_id` (`prescricao_id`),
  ADD KEY `paciente_id` (`paciente_id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `usuario_id` (`usuario_id`) USING BTREE;

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`usuario_id`),
  ADD UNIQUE KEY `nome` (`nome`),
  ADD KEY `entidade_id` (`entidade_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `entidade`
--
ALTER TABLE `entidade`
  MODIFY `id_entidade` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `entrada`
--
ALTER TABLE `entrada`
  MODIFY `entrada_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `item`
--
ALTER TABLE `item`
  MODIFY `item_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `paciente`
--
ALTER TABLE `paciente`
  MODIFY `paciente_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `prescricao`
--
ALTER TABLE `prescricao`
  MODIFY `id_Prescrição` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=305;

--
-- AUTO_INCREMENT for table `saida`
--
ALTER TABLE `saida`
  MODIFY `saida_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `usuario_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `entrada`
--
ALTER TABLE `entrada`
  ADD CONSTRAINT `entrada_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`),
  ADD CONSTRAINT `fk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`usuario_id`);

--
-- Limitadores para a tabela `paciente`
--
ALTER TABLE `paciente`
  ADD CONSTRAINT `entidade_id` FOREIGN KEY (`entidade_id`) REFERENCES `entidade` (`id_entidade`);

--
-- Limitadores para a tabela `prescricao`
--
ALTER TABLE `prescricao`
  ADD CONSTRAINT `prescricao_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`usuario_id`),
  ADD CONSTRAINT `prescricao_ibfk_3` FOREIGN KEY (`paciente_id`) REFERENCES `paciente` (`paciente_id`);

--
-- Limitadores para a tabela `saida`
--
ALTER TABLE `saida`
  ADD CONSTRAINT `saida_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`usuario_id`),
  ADD CONSTRAINT `saida_ibfk_4` FOREIGN KEY (`prescricao_id`) REFERENCES `prescricao` (`id_Prescrição`),
  ADD CONSTRAINT `saida_ibfk_5` FOREIGN KEY (`paciente_id`) REFERENCES `paciente` (`paciente_id`),
  ADD CONSTRAINT `saida_ibfk_6` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`);

--
-- Limitadores para a tabela `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`entidade_id`) REFERENCES `entidade` (`id_entidade`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
