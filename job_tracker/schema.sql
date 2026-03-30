-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
--
-- Host: 127.0.0.1    Database: job_tracker
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'c40304ec-f235-11f0-bd7b-3e80c86bbc71:1-104';

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `application_date` date NOT NULL,
  `status` varchar(30) DEFAULT 'Applied',
  `resume_version` varchar(50) DEFAULT NULL,
  `cover_letter_sent` tinyint(1) DEFAULT '0',
  `response_date` date DEFAULT NULL,
  `interview_date` datetime DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `interview_data` json DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  KEY `job_id` (`job_id`),
  KEY `idx_app_status` (`status`),
  CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (26,1,'2025-01-16','Applied','v2.1',1,NULL,NULL,NULL,'2026-02-02 02:13:20',NULL),(27,3,'2025-01-13','Interview Scheduled','v2.1',1,NULL,NULL,NULL,'2026-02-02 02:13:20',NULL),(29,5,'2025-01-15','Applied','v2.1',1,NULL,NULL,NULL,'2026-02-02 02:13:20',NULL),(30,7,'2025-01-12','Phone Screen','v2.1',1,NULL,NULL,NULL,'2026-02-02 02:13:20',NULL),(31,6,'2026-02-16','Applied','v3.0',1,NULL,NULL,NULL,'2026-02-16 17:35:03',NULL),(33,8,'2026-03-23','Offer Received','70.1',1,NULL,NULL,NULL,'2026-03-25 01:24:05',NULL);
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `industry` varchar(50) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`company_id`),
  KEY `idx_company_industry` (`industry`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (1,'Tech Solutions Inc','Technology','www.techsolutions.com','Miami','Florida',NULL,'2026-02-02 00:21:26'),(2,'Data Analytics Corp','Data Science','www.dataanalytics.com','Austin','Texas',NULL,'2026-02-02 00:21:26'),(3,'Cloud Systems LLC','Cloud Computing','www.cloudsystems.com','Seattle','Washington',NULL,'2026-02-02 00:21:26'),(4,'Digital Innovations','Software','www.digitalinnovations.com','San Francisco','California','Applied to Senior Developer position on 2026-02-16','2026-02-02 00:21:26'),(5,'Smart Tech Group','AI/ML','www.smarttech.com','Boston','Massachusetts',NULL,'2026-02-02 00:21:26'),(7,'New Tech Corp','Technology',NULL,'Denver','Colorado',NULL,'2026-02-16 16:43:30'),(8,'Python Solutions LLC','Software Development','www.pythonsolutions.com','Miami','Florida',NULL,'2026-02-17 04:35:05'),(10,'Apple','Sales','https://www.apple.com','San Bernadino','Cali','Iphone','2026-03-25 02:10:21');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `job_title` varchar(100) DEFAULT NULL,
  `linkedin_url` varchar(200) DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`contact_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (1,1,'Sarah','Johnson','sjohnson@techsolutions.com',NULL,'HR Manager',NULL,NULL,'2026-02-02 02:45:05'),(2,2,'Michael','Chen','mchen@dataanalytics.com',NULL,'TechnicalRecruiter',NULL,NULL,'2026-02-02 02:45:05'),(3,3,'Emily','Williams','ewilliams@cloudsystems.com',NULL,'HiringManager',NULL,NULL,'2026-02-02 02:45:05'),(4,4,'David','Brown',NULL,NULL,'Senior Developer',NULL,NULL,'2026-02-02 02:45:05'),(5,5,'Lisa','Garcia','lgarcia@smarttech.com',NULL,'Talent Acquisition',NULL,NULL,'2026-02-02 02:45:05'),(7,4,'Robert','Tim','rkim@digitalinnovations.com','None','Engineering Manager','','None','2026-02-16 17:48:32');
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `job_description` text,
  `salary_min` decimal(10,2) DEFAULT NULL,
  `salary_max` decimal(10,2) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `posting_url` varchar(500) DEFAULT NULL,
  `date_posted` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `requirements` json DEFAULT NULL,
  PRIMARY KEY (`job_id`),
  KEY `idx_job_title` (`job_title`),
  KEY `idx_company_type` (`company_id`,`job_type`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,1,'Software Developer',NULL,70000.00,90000.00,'Full-time',NULL,'2025-01-15',1,'2026-02-02 02:12:30','{\"education\": \"Bachelor in CS or related field\", \"remote_option\": true, \"required_skills\": [\"Python\", \"SQL\", \"Git\"], \"experience_years\": 2, \"preferred_skills\": [\"Flask\", \"Docker\", \"AWS\"]}'),(2,1,'Database Administrator',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-10',1,'2026-02-02 02:12:30',NULL),(3,2,'Data Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-12',1,'2026-02-02 02:12:30','{\"education\": \"Bachelor degree\", \"remote_option\": false, \"required_skills\": [\"SQL\", \"Excel\", \"Tableau\"], \"experience_years\": 1, \"preferred_skills\": [\"Python\", \"R\"]}'),(4,3,'Cloud Engineer',NULL,80000.00,100000.00,'Full-time',NULL,'2025-01-08',1,'2026-02-02 02:12:30',NULL),(5,4,'Junior Developer',NULL,55000.00,70000.00,'Full-time',NULL,'2025-01-14',1,'2026-02-02 02:12:30',NULL),(6,4,'Senior Developer',NULL,95000.00,120000.00,'Full-time',NULL,'2025-01-14',1,'2026-02-02 02:12:30',NULL),(7,5,'ML Engineer',NULL,90000.00,115000.00,'Full-time',NULL,'2025-01-11',1,'2026-02-02 02:12:30',NULL),(8,1,'QA Engineer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-05',1,'2026-02-09 17:55:16',NULL),(9,2,'Business Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-06',1,'2026-02-09 17:55:16',NULL),(10,2,'Data Scientist',NULL,85000.00,110000.00,'Full-time',NULL,'2025-01-07',1,'2026-02-09 17:55:16',NULL),(11,3,'DevOps Engineer',NULL,80000.00,105000.00,'Full-time',NULL,'2025-01-08',1,'2026-02-09 17:55:16',NULL),(12,3,'Security Analyst',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-09',1,'2026-02-09 17:55:16',NULL),(13,4,'UI/UX Designer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-10',1,'2026-02-09 17:55:16',NULL),(14,5,'Product Manager',NULL,90000.00,120000.00,'Full-time',NULL,'2025-01-11',1,'2026-02-09 17:55:16',NULL),(15,1,'Technical Writer',NULL,55000.00,75000.00,'Contract',NULL,'2025-01-12',1,'2026-02-09 17:55:16',NULL),(16,2,'Intern - Data',NULL,30000.00,40000.00,'Internship',NULL,'2025-01-13',1,'2026-02-09 17:55:16',NULL),(17,4,'Intern - Development',NULL,32000.00,42000.00,'Internship',NULL,'2025-01-14',1,'2026-02-09 17:55:16',NULL),(24,1,'Backend Engineer',NULL,85000.00,110000.00,'Full-Time','https://www.example.com/careers/backend-engineer','2026-03-24',1,'2026-03-24 16:08:37','{\"required_skills\": [\"Python\", \"SQL\", \"Go\", \"Docker\"]}'),(25,1,'Backend Engineer',NULL,85000.00,110000.00,'Full-Time','https://www.google.com/search?q=https://www.example.com/careers/backend-engineer&authuser=1','2026-03-24',1,'2026-03-24 16:09:53','{\"required_skills\": [\"Python\", \"SQL\", \"Go\", \"Docker\"]}');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 11:09:54