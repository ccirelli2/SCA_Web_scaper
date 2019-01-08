-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: SCA_SCRAPER
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `SCA_DATA3_TEST`
--

DROP TABLE IF EXISTS `SCA_DATA3_TEST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SCA_DATA3_TEST` (
  `page_number` varchar(255) NOT NULL,
  `defendant_name` varchar(255) DEFAULT NULL,
  `case_status` varchar(25) DEFAULT NULL,
  `filling_date` date DEFAULT NULL,
  `close_date` date DEFAULT NULL,
  `case_summary` longtext,
  `Sector` varchar(25) DEFAULT NULL,
  `Industry` varchar(225) DEFAULT NULL,
  `Symbol` varchar(25) DEFAULT NULL,
  `Status_2` varchar(25) DEFAULT NULL,
  `Headquarters` varchar(225) DEFAULT NULL,
  `Company_market` varchar(25) DEFAULT NULL,
  `Court` varchar(25) DEFAULT NULL,
  `Docket` varchar(25) DEFAULT NULL,
  `Judge` varchar(255) DEFAULT NULL,
  `Date_Filed` date DEFAULT NULL,
  `Class_Period_Start` date DEFAULT NULL,
  `Class_Period_End` date DEFAULT NULL,
  `Plaintiff_firm` varchar(2225) DEFAULT NULL,
  `Ref_court` varchar(255) DEFAULT NULL,
  `Ref_docket` varchar(255) DEFAULT NULL,
  `Ref_judge` varchar(255) DEFAULT NULL,
  `Ref_date_filed` date DEFAULT NULL,
  `Ref_class_period_start` date DEFAULT NULL,
  `Ref_class_period_end` date DEFAULT NULL,
  `YEAR_FILED` int(4) DEFAULT NULL,
  `Breach_Fiduciary_Duties` smallint(6) DEFAULT NULL,
  `Merger` smallint(6) DEFAULT NULL,
  `Proxy_violation` smallint(6) DEFAULT NULL,
  `Related_parties` smallint(6) DEFAULT NULL,
  `Stock_Drop` smallint(6) DEFAULT NULL,
  `Cash_Flow` smallint(6) DEFAULT NULL,
  `Revenue_Rec` smallint(6) DEFAULT NULL,
  `Net_Income` smallint(6) DEFAULT NULL,
  `Customers` smallint(6) DEFAULT NULL,
  `Fourth_Quarter` smallint(6) DEFAULT NULL,
  `Third_Quarter` smallint(6) DEFAULT NULL,
  `Second_Quarter` smallint(6) DEFAULT NULL,
  `Press_Release` smallint(6) DEFAULT NULL,
  `10K_Filling` smallint(6) DEFAULT NULL,
  `10Q_Filling` smallint(6) DEFAULT NULL,
  `Corporate_Governance` smallint(6) DEFAULT NULL,
  `Conflicts_Interest` smallint(6) DEFAULT NULL,
  `Accounting` smallint(6) DEFAULT NULL,
  `Fees` smallint(6) DEFAULT NULL,
  `Failed_disclose` smallint(6) DEFAULT NULL,
  `False_misleading` smallint(6) DEFAULT NULL,
  `Commissions` smallint(6) DEFAULT NULL,
  `Bankruptcy` smallint(6) DEFAULT NULL,
  `Secondary_Offering` smallint(6) DEFAULT NULL,
  `IPO` smallint(6) DEFAULT NULL,
  `1934_Exchange_Act` smallint(6) DEFAULT NULL,
  `Derivative` smallint(6) DEFAULT NULL,
  `10b5` smallint(6) DEFAULT NULL,
  `1933_Act` smallint(6) DEFAULT NULL,
  `Heavy_trading` smallint(6) DEFAULT NULL,
  `class_action` smallint(6) DEFAULT NULL,
  `SEC_Investigation` smallint(6) DEFAULT NULL,
  `Proxy` smallint(6) DEFAULT NULL,
  `ERISA` smallint(6) DEFAULT NULL,
  `FCPA` smallint(6) DEFAULT NULL,
  `Sexual_Misconduct` smallint(6) DEFAULT NULL,
  `Data_breach` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`page_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-05 19:30:56
