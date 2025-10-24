-- MySQL dump 10.13  Distrib 9.4.0, for macos15.4 (arm64)
--
-- Host: localhost    Database: rental_mysqldb
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `analytics_searchhistory`
--

DROP TABLE IF EXISTS `analytics_searchhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analytics_searchhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `searched_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analytics_searchhistory_user_id_b129b7b5_fk_users_user_id` (`user_id`),
  CONSTRAINT `analytics_searchhistory_user_id_b129b7b5_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_searchhistory`
--

LOCK TABLES `analytics_searchhistory` WRITE;
/*!40000 ALTER TABLE `analytics_searchhistory` DISABLE KEYS */;
INSERT INTO `analytics_searchhistory` VALUES (1,'Function-based bi-directional extranet','2025-10-16 12:22:06.520978',36),(2,'Break determine in heart run paper. Summer detail simply range admit.','2025-10-20 05:33:54.735378',24),(3,'Sign experience support network finally. Property himself cell whatever woman. Himself better treat guy cup dream.','2025-10-22 14:59:52.389223',28);
/*!40000 ALTER TABLE `analytics_searchhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_viewhistory`
--

DROP TABLE IF EXISTS `analytics_viewhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analytics_viewhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `viewed_at` datetime(6) NOT NULL,
  `listing_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `analytics_viewhistory_user_id_listing_id_viewed_at_28ddaa66_uniq` (`user_id`,`listing_id`,`viewed_at`),
  KEY `analytics_viewhistory_listing_id_b9c0cc93_fk_listings_id` (`listing_id`),
  CONSTRAINT `analytics_viewhistory_listing_id_b9c0cc93_fk_listings_id` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`),
  CONSTRAINT `analytics_viewhistory_user_id_f3b11a52_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_viewhistory`
--

LOCK TABLES `analytics_viewhistory` WRITE;
/*!40000 ALTER TABLE `analytics_viewhistory` DISABLE KEYS */;
INSERT INTO `analytics_viewhistory` VALUES (7,'2025-10-20 05:30:31.471799',78,24),(4,'2025-10-17 06:00:42.370766',13,27),(6,'2025-10-17 06:08:58.797200',13,27),(5,'2025-10-17 06:07:40.879741',16,27),(11,'2025-10-22 15:02:49.883726',13,28),(10,'2025-10-22 14:55:20.744932',47,28),(9,'2025-10-22 14:49:09.188774',75,28),(1,'2025-10-16 12:10:22.424474',13,36),(3,'2025-10-16 12:29:53.660503',13,36),(2,'2025-10-16 12:10:58.093076',81,36),(8,'2025-10-21 05:47:28.132154',84,43);
/*!40000 ALTER TABLE `analytics_viewhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'LANDLORD'),(1,'tenant');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (8,1,28),(9,1,29),(1,1,32),(2,1,33),(3,1,36),(4,1,37),(5,1,40),(6,1,41),(7,1,44),(14,2,25),(15,2,26),(16,2,27),(17,2,28),(10,2,32),(11,2,36),(12,2,40),(13,2,44);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add Listing',7,'add_listing'),(26,'Can change Listing',7,'change_listing'),(27,'Can delete Listing',7,'delete_listing'),(28,'Can view Listing',7,'view_listing'),(29,'Can add Booking',8,'add_booking'),(30,'Can change Booking',8,'change_booking'),(31,'Can delete Booking',8,'delete_booking'),(32,'Can view Booking',8,'view_booking'),(33,'Can add review',9,'add_review'),(34,'Can change review',9,'change_review'),(35,'Can delete review',9,'delete_review'),(36,'Can view review',9,'view_review'),(37,'Can add search history',10,'add_searchhistory'),(38,'Can change search history',10,'change_searchhistory'),(39,'Can delete search history',10,'delete_searchhistory'),(40,'Can view search history',10,'view_searchhistory'),(41,'Can add view history',11,'add_viewhistory'),(42,'Can change view history',11,'change_viewhistory'),(43,'Can delete view history',11,'delete_viewhistory'),(44,'Can view view history',11,'view_viewhistory'),(45,'Can add Token',12,'add_token'),(46,'Can change Token',12,'change_token'),(47,'Can delete Token',12,'delete_token'),(48,'Can view Token',12,'view_token'),(49,'Can add Token',13,'add_tokenproxy'),(50,'Can change Token',13,'change_tokenproxy'),(51,'Can delete Token',13,'delete_tokenproxy'),(52,'Can view Token',13,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('006065a1070d63864c80a6d942f7e55821cf50a9','2025-10-17 11:03:29.048266',36),('091034daadd154d814bd2f57cbe1375ffb1de7b7','2025-10-20 07:52:31.365462',57),('1248ac9a1bc3c53cef545c7cd21bbbc1f333c5bc','2025-10-15 16:33:48.819475',5),('1c25f62225c9e2795677b5b313b55ec707fcdb59','2025-10-16 11:47:51.501877',33),('1e474d21dcacd365baf91fa74185b98edf567147','2025-10-21 11:57:11.395811',13),('4d1721881286c8ffd914c2a8154625a2d918e26d','2025-10-16 10:34:54.341618',35),('509d4fe997634a62a593b9dc31fe91a61f69f063','2025-10-17 06:37:55.382621',45),('6507ba4c4a4d9012a023e2078d02327f3bbe58f8','2025-10-17 06:48:40.433521',56),('869d980a52e45819ebcf39c3be7961526521cf3a','2025-10-20 06:03:28.963565',59),('8c4bad9938d8ad589bdd37994e689f425efd6eda','2025-10-18 06:54:01.838240',34),('9319146c67a4eace38db6abeaa6a29482c8d2eba','2025-10-16 09:38:06.447029',9),('9cb255ec5186dc37d8fea72ff13d607f181682a8','2025-10-20 07:51:21.516433',58),('a5e46be913052a370045c2d78fa5d3c257d6e29f','2025-10-15 16:21:46.437616',6),('c0032aab8fc822eb1d9b45d4dc1780ccd7681b0c','2025-10-20 08:00:35.391236',50),('c2f5741e2c89390bcad2625fbb5e22674fd3cca6','2025-10-22 06:52:45.384224',23),('c91ce6d575718f3cc30b492476b313306a08eef1','2025-10-18 06:59:36.138285',42),('d41034edd0df09dfd7cdbcbe70eba67f4a92ee90','2025-10-15 06:03:40.547767',3),('f990922b050b801a0cc66d2228b782d87774e591','2025-10-17 07:04:32.481859',46);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `parking_included` tinyint(1) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_price` decimal(12,2) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `listing_id` bigint NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bookings_listing_id_2ae12641_fk_listings_id` (`listing_id`),
  KEY `bookings_tenant_id_e8d57e61_fk_users_user_id` (`tenant_id`),
  CONSTRAINT `bookings_listing_id_2ae12641_fk_listings_id` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`),
  CONSTRAINT `bookings_tenant_id_e8d57e61_fk_users_user_id` FOREIGN KEY (`tenant_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,'2025-11-10','2025-11-14',0,'pending',713.90,'2025-10-15 10:31:30.273140','2025-10-15 10:31:30.273303',0,67,10),(2,'2025-11-05','2025-11-09',0,'pending',788.10,'2025-10-15 10:31:30.275125','2025-10-15 10:31:30.275129',0,22,39),(3,'2025-11-08','2025-11-11',0,'pending',632.32,'2025-10-15 10:31:30.276272','2025-10-15 10:31:30.276275',0,58,16),(4,'2025-10-19','2025-10-25',0,'pending',1380.19,'2025-10-15 10:31:30.277338','2025-10-15 10:31:30.277341',0,62,29),(5,'2025-10-15','2025-10-19',1,'confirmed',792.85,'2025-10-15 10:31:30.278164','2025-10-21 05:32:23.061113',0,35,19),(6,'2025-11-05','2025-11-09',0,'pending',539.35,'2025-10-15 10:31:30.279142','2025-10-15 10:31:30.279146',0,79,11),(7,'2025-11-01','2025-11-04',0,'pending',350.92,'2025-10-15 10:31:30.279757','2025-10-15 10:31:30.279760',0,12,3),(8,'2025-11-12','2025-11-18',0,'pending',903.07,'2025-10-15 10:31:30.281061','2025-10-15 10:31:30.281066',0,3,17),(9,'2025-11-03','2025-11-07',0,'pending',424.95,'2025-10-15 10:31:30.281891','2025-10-15 10:31:30.281894',0,31,9),(10,'2025-11-01','2025-11-06',0,'pending',273.42,'2025-10-15 10:31:30.282660','2025-10-15 10:31:30.282663',0,13,26),(11,'2025-10-28','2025-11-03',0,'pending',1380.19,'2025-10-15 10:31:30.283411','2025-10-15 10:31:30.283414',0,62,7),(12,'2025-11-14','2025-11-18',0,'pending',783.05,'2025-10-15 10:31:30.284172','2025-10-15 10:31:30.284175',0,59,33),(13,'2025-11-11','2025-11-17',0,'pending',760.83,'2025-10-15 10:31:30.284960','2025-10-15 10:31:30.284963',0,11,24),(14,'2025-10-30','2025-11-02',0,'pending',185.20,'2025-10-15 10:31:30.285715','2025-10-15 10:31:30.285718',0,56,41),(15,'2025-11-04','2025-11-10',0,'pending',917.49,'2025-10-15 10:31:30.286465','2025-10-15 10:31:30.286468',0,73,29),(16,'2025-10-16','2025-10-21',0,'confirmed',199.14,'2025-10-15 10:31:30.287261','2025-10-22 06:37:17.254630',0,55,32),(17,'2025-10-26','2025-10-30',0,'pending',245.00,'2025-10-15 10:31:30.288044','2025-10-15 10:31:30.288047',0,50,39),(18,'2025-10-15','2025-10-19',1,'confirmed',1070.85,'2025-10-15 10:31:30.288950','2025-10-20 05:26:05.551427',0,4,4),(19,'2025-10-18','2025-10-19',0,'confirmed',321.10,'2025-10-15 10:31:30.289780','2025-10-20 05:26:05.548912',0,19,23),(20,'2025-10-28','2025-11-01',0,'pending',894.45,'2025-10-15 10:31:30.291050','2025-10-15 10:31:30.291053',0,33,41),(21,'2025-10-14','2025-10-16',1,'confirmed',157.65,'2025-10-15 10:31:30.291891','2025-10-17 10:58:55.093094',0,13,36),(22,'2025-11-08','2025-11-11',0,'pending',361.16,'2025-10-15 10:31:30.292744','2025-10-15 10:31:30.292747',0,71,7),(23,'2025-10-17','2025-10-24',0,'pending',704.48,'2025-10-15 10:31:30.293517','2025-10-15 10:31:30.293520',0,38,22),(24,'2025-11-11','2025-11-18',0,'pending',1102.16,'2025-10-15 10:31:30.294318','2025-10-15 10:31:30.294321',0,34,6),(25,'2025-11-02','2025-11-06',1,'pending',507.10,'2025-10-15 10:31:30.295088','2025-10-15 10:31:30.295090',0,49,25),(26,'2025-11-05','2025-11-10',0,'pending',691.32,'2025-10-15 10:31:30.296000','2025-10-15 10:31:30.296005',0,61,14),(27,'2025-10-30','2025-11-01',0,'pending',438.54,'2025-10-15 10:31:30.296780','2025-10-15 10:31:30.296784',0,43,23),(28,'2025-10-17','2025-10-20',1,'confirmed',645.40,'2025-10-15 10:31:30.297512','2025-10-22 06:37:17.232016',0,24,37),(29,'2025-11-06','2025-11-09',0,'pending',516.80,'2025-10-15 10:31:30.298201','2025-10-15 10:31:30.298205',0,77,12),(30,'2025-10-15','2025-10-20',0,'confirmed',251.10,'2025-10-15 10:31:30.298848','2025-10-21 05:32:23.090209',0,76,41),(31,'2025-10-16','2025-10-17',1,'confirmed',176.12,'2025-10-15 10:31:30.299524','2025-10-17 11:18:10.783746',0,38,27),(32,'2025-11-03','2025-11-05',0,'pending',144.39,'2025-10-15 10:31:30.300161','2025-10-15 10:31:30.300164',0,21,34),(33,'2025-10-22','2025-10-23',1,'pending',190.64,'2025-10-15 10:31:30.300803','2025-10-15 10:31:30.300806',0,12,28),(34,'2025-10-29','2025-10-30',0,'pending',169.78,'2025-10-15 10:31:30.301478','2025-10-15 10:31:30.301481',0,46,11),(35,'2025-10-24','2025-10-25',1,'pending',429.86,'2025-10-15 10:31:30.302190','2025-10-15 10:31:30.302193',0,45,34),(36,'2025-10-25','2025-10-31',0,'pending',274.96,'2025-10-15 10:31:30.302835','2025-10-15 10:31:30.302838',0,63,35),(37,'2025-10-24','2025-10-28',1,'pending',266.30,'2025-10-15 10:31:30.303450','2025-10-15 10:31:30.303453',0,14,43),(38,'2025-11-05','2025-11-12',0,'pending',1217.92,'2025-10-15 10:31:30.304062','2025-10-15 10:31:30.304065',0,64,10),(39,'2025-11-05','2025-11-09',0,'pending',729.60,'2025-10-15 10:31:30.304717','2025-10-15 10:31:30.304720',0,72,22),(40,'2025-10-30','2025-11-06',1,'pending',1349.52,'2025-10-15 10:31:30.305364','2025-10-15 10:31:30.305366',0,47,5),(41,'2025-11-08','2025-11-11',0,'pending',610.92,'2025-10-15 10:31:30.306023','2025-10-15 10:31:30.306026',0,32,42),(42,'2025-10-28','2025-11-02',0,'pending',1055.94,'2025-10-15 10:31:30.306941','2025-10-15 10:31:30.306945',0,37,32),(43,'2025-11-13','2025-11-20',1,'pending',1118.16,'2025-10-15 10:31:30.307652','2025-10-15 10:31:30.307655',0,73,19),(44,'2025-10-17','2025-10-22',0,'pending',656.46,'2025-10-15 10:31:30.308300','2025-10-15 10:31:30.308303',0,23,28),(45,'2025-10-23','2025-10-28',0,'pending',960.96,'2025-10-15 10:31:30.309250','2025-10-15 10:31:30.309253',0,36,1),(46,'2025-10-28','2025-10-30',1,'pending',247.83,'2025-10-15 10:31:30.309897','2025-10-15 10:31:30.309900',0,16,42),(47,'2025-10-28','2025-10-29',0,'pending',397.72,'2025-10-15 10:31:30.310507','2025-10-15 10:31:30.310510',0,68,41),(48,'2025-10-23','2025-10-24',0,'pending',319.56,'2025-10-15 10:31:30.311118','2025-10-15 10:31:30.311121',0,27,15),(49,'2025-10-16','2025-10-22',0,'pending',917.49,'2025-10-15 10:31:30.311734','2025-10-15 10:31:30.311737',0,73,33),(50,'2025-11-13','2025-11-20',0,'pending',478.96,'2025-10-15 10:31:30.312360','2025-10-15 10:31:30.312363',0,25,13),(51,'2025-10-27','2025-11-02',0,'pending',1226.47,'2025-10-15 10:31:30.312934','2025-10-15 10:31:30.312937',0,6,5),(52,'2025-11-07','2025-11-12',0,'pending',359.22,'2025-10-15 10:31:30.313515','2025-10-15 10:31:30.313518',0,25,22),(53,'2025-10-16','2025-10-22',0,'pending',1311.73,'2025-10-15 10:31:30.314112','2025-10-15 10:31:30.314115',0,9,32),(54,'2025-11-01','2025-11-02',0,'pending',169.78,'2025-10-15 10:31:30.314673','2025-10-15 10:31:30.314676',0,46,9),(55,'2025-10-16','2025-10-21',0,'confirmed',938.10,'2025-10-15 10:31:30.315230','2025-10-22 06:37:17.250503',0,47,31),(56,'2025-10-21','2025-10-22',0,'pending',291.84,'2025-10-15 10:31:30.315822','2025-10-15 10:31:30.315825',0,72,5),(57,'2025-10-25','2025-10-27',0,'pending',323.61,'2025-10-15 10:31:30.316400','2025-10-15 10:31:30.316403',0,79,7),(58,'2025-10-17','2025-10-19',0,'confirmed',480.48,'2025-10-15 10:31:30.316959','2025-10-20 05:26:05.546205',0,36,35),(59,'2025-10-23','2025-10-27',0,'pending',894.45,'2025-10-15 10:31:30.317569','2025-10-15 10:31:30.317572',0,33,11),(60,'2025-10-17','2025-10-19',1,'confirmed',293.79,'2025-10-15 10:31:30.318169','2025-10-20 05:26:05.529511',0,2,21),(61,'2025-10-29','2025-11-05',0,'pending',1454.16,'2025-10-15 10:31:30.318776','2025-10-15 10:31:30.318779',0,44,10),(62,'2025-10-30','2025-11-06',1,'pending',1713.36,'2025-10-15 10:31:30.319328','2025-10-15 10:31:30.319331',0,4,20),(63,'2025-11-07','2025-11-12',0,'pending',1053.00,'2025-10-15 10:31:30.319865','2025-10-15 10:31:30.319868',0,28,14),(64,'2025-11-02','2025-11-03',0,'pending',315.82,'2025-10-15 10:31:30.320404','2025-10-15 10:31:30.320406',0,66,24),(65,'2025-10-21','2025-10-22',0,'pending',119.74,'2025-10-15 10:31:30.321212','2025-10-15 10:31:30.321215',0,25,20),(66,'2025-11-14','2025-11-16',1,'pending',642.51,'2025-10-15 10:31:30.321793','2025-10-15 10:31:30.321795',0,4,40),(67,'2025-11-11','2025-11-17',1,'confirmed',1007.28,'2025-10-15 10:31:30.322355','2025-10-22 07:14:52.558264',0,19,11),(68,'2025-10-28','2025-10-30',0,'confirmed',437.76,'2025-10-15 10:31:30.323223','2025-10-15 10:31:30.323226',0,72,33),(69,'2025-10-29','2025-11-01',0,'confirmed',236.84,'2025-10-15 10:31:30.323775','2025-10-15 10:31:30.323778',0,42,24),(70,'2025-10-26','2025-10-29',0,'confirmed',626.44,'2025-10-15 10:31:30.324541','2025-10-15 10:31:30.324544',0,59,20),(71,'2025-10-21','2025-10-22',0,'confirmed',315.24,'2025-10-15 10:31:30.325056','2025-10-15 10:31:30.325059',0,22,25),(72,'2025-10-19','2025-10-23',0,'confirmed',449.35,'2025-10-15 10:31:30.325625','2025-10-15 10:31:30.325630',0,26,35),(73,'2025-10-25','2025-10-27',1,'confirmed',379.47,'2025-10-15 10:31:30.326165','2025-10-15 10:31:30.326168',0,61,24),(74,'2025-10-28','2025-11-04',1,'confirmed',399.68,'2025-10-15 10:31:30.326686','2025-10-15 10:31:30.326689',0,20,21),(75,'2025-10-16','2025-10-19',1,'confirmed',292.08,'2025-10-15 10:31:30.327195','2025-10-15 10:31:30.327198',0,78,4),(76,'2025-11-09','2025-11-11',1,'confirmed',426.90,'2025-10-15 10:31:30.327739','2025-10-15 10:31:30.327742',0,39,3),(77,'2025-10-29','2025-10-30',0,'confirmed',399.72,'2025-10-15 10:31:30.328562','2025-10-15 10:31:30.328565',0,7,39),(78,'2025-11-06','2025-11-07',0,'confirmed',231.10,'2025-10-15 10:31:30.329089','2025-10-15 10:31:30.329092',0,74,37),(79,'2025-11-05','2025-11-10',0,'cancelled',281.52,'2025-10-15 10:31:30.329607','2025-10-20 05:43:00.059421',1,69,4),(80,'2025-10-15','2025-10-17',0,'confirmed',599.58,'2025-10-15 10:31:30.330135','2025-10-15 10:31:30.330138',0,7,28),(81,'2025-11-06','2025-11-09',0,'confirmed',600.80,'2025-10-15 10:31:30.330671','2025-10-15 10:31:30.330673',0,54,1),(82,'2025-11-01','2025-11-03',0,'confirmed',147.00,'2025-10-15 10:31:30.331387','2025-10-15 10:31:30.331389',0,50,40),(83,'2025-10-24','2025-10-29',0,'confirmed',826.62,'2025-10-15 10:31:30.331890','2025-10-15 10:31:30.331893',0,34,35),(84,'2025-11-02','2025-11-08',0,'confirmed',395.78,'2025-10-15 10:31:30.332389','2025-10-15 10:31:30.332392',0,57,31),(85,'2025-10-16','2025-10-17',0,'confirmed',167.02,'2025-10-15 10:31:30.333126','2025-10-15 10:31:30.333129',0,53,34),(86,'2025-11-02','2025-11-09',0,'confirmed',271.20,'2025-10-15 10:31:30.333744','2025-10-15 10:31:30.333747',0,51,38),(87,'2025-11-02','2025-11-07',0,'confirmed',528.36,'2025-10-15 10:31:30.334910','2025-10-15 10:31:30.334913',0,38,15),(88,'2025-11-05','2025-11-07',0,'confirmed',99.57,'2025-10-15 10:31:30.335793','2025-10-16 05:26:23.782683',0,55,40),(89,'2025-11-11','2025-11-12',0,'confirmed',231.10,'2025-10-15 10:31:30.336560','2025-10-17 08:50:17.024792',0,74,3),(90,'2025-10-16','2025-10-17',0,'confirmed',28.00,'2025-10-16 06:12:58.610032','2025-10-16 06:23:23.783252',0,82,1),(91,'2025-10-17','2025-10-18',1,'confirmed',28.00,'2025-10-17 07:33:44.189354','2025-10-17 07:33:44.189373',0,82,24),(93,'2025-10-17','2026-01-01',1,'confirmed',2935.12,'2025-10-17 10:42:37.454887','2025-10-22 07:34:46.945374',0,80,34),(94,'2025-10-21','2025-10-22',1,'confirmed',170.00,'2025-10-21 05:50:11.292160','2025-10-21 05:54:31.818451',0,84,43),(95,'2025-10-21','2025-10-22',1,'confirmed',28.00,'2025-10-21 11:56:12.434860','2025-10-21 12:00:44.636865',0,82,15),(96,'2025-10-22','2025-10-23',1,'confirmed',28.00,'2025-10-21 11:58:33.171366','2025-10-21 12:00:44.630659',0,82,13),(97,'2025-10-22','2025-10-23',1,'confirmed',85.00,'2025-10-22 06:48:53.125907','2025-10-22 06:56:44.674605',0,84,42),(98,'2025-10-23','2025-10-24',1,'confirmed',85.00,'2025-10-22 06:56:21.229341','2025-10-22 06:56:44.670298',0,84,23),(99,'2025-10-22','2025-10-25',0,'confirmed',360.00,'2025-10-22 14:42:24.679171','2025-10-22 14:46:28.253822',0,85,28),(100,'2025-10-22','2025-10-24',1,'pending',337.38,'2025-10-22 14:56:09.394114','2025-10-22 14:58:29.414942',1,47,28);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-15 05:50:27.932840','2','test@example.com',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,1),(2,'2025-10-15 16:05:57.133875','1','Tenant',1,'[{\"added\": {}}]',3,1),(3,'2025-10-15 16:08:12.256515','2','Landlord',1,'[{\"added\": {}}]',3,1),(4,'2025-10-15 16:27:20.875057','6','armstrongpaul@example.net',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(5,'2025-10-15 16:32:38.779427','5','gonzalezdaniel@example.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(6,'2025-10-15 17:01:34.004891','2','landlord',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(7,'2025-10-15 17:01:41.195336','1','tenant',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(8,'2025-10-15 17:13:26.445187','50','maria64@example.org',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(9,'2025-10-16 10:30:14.826707','83','string — string, string, string, string',3,'',7,1),(10,'2025-10-17 10:58:55.109033','21','Бронь #21 — Automated didactic parallelism [2025-10-14 → 2025-10-16] (confirmed) + Парковка',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,1),(11,'2025-10-17 11:18:10.785514','31','Бронь #31 — Reactive zero administration leverage [2025-10-16 → 2025-10-17] (confirmed) + Парковка',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',8,1),(12,'2025-10-19 05:32:19.812981','92','Бронь #92 — Cozy apartment in central Tashkent [2026-10-17 → 2125-10-18] (confirmed) + Парковка',3,'',8,1),(13,'2025-10-22 07:13:15.568045','93','Booking #93 — Grass-roots transitional conglomeration [2025-10-17 → 2026-01-01] (pending) + Parking',2,'[{\"changed\": {\"fields\": [\"End date\"]}}]',8,1),(14,'2025-10-22 07:14:35.395239','67','Booking #67 — Synergistic object-oriented support [2025-11-11 → 2025-11-17] (pending) + Parking',2,'[{\"changed\": {\"fields\": [\"End date\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(10,'analytics','searchhistory'),(11,'analytics','viewhistory'),(3,'auth','group'),(2,'auth','permission'),(12,'authtoken','token'),(13,'authtoken','tokenproxy'),(8,'bookings','booking'),(4,'contenttypes','contenttype'),(7,'listings','listing'),(9,'reviews','review'),(5,'sessions','session'),(6,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-15 05:14:57.887299'),(2,'contenttypes','0002_remove_content_type_name','2025-10-15 05:14:57.908134'),(3,'auth','0001_initial','2025-10-15 05:14:57.963249'),(4,'auth','0002_alter_permission_name_max_length','2025-10-15 05:14:57.974215'),(5,'auth','0003_alter_user_email_max_length','2025-10-15 05:14:57.976399'),(6,'auth','0004_alter_user_username_opts','2025-10-15 05:14:57.978390'),(7,'auth','0005_alter_user_last_login_null','2025-10-15 05:14:57.980332'),(8,'auth','0006_require_contenttypes_0002','2025-10-15 05:14:57.980895'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-15 05:14:57.982589'),(10,'auth','0008_alter_user_username_max_length','2025-10-15 05:14:57.984428'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-15 05:14:57.986416'),(12,'auth','0010_alter_group_name_max_length','2025-10-15 05:14:57.990771'),(13,'auth','0011_update_proxy_permissions','2025-10-15 05:14:57.992786'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-15 05:14:57.994482'),(15,'users','0001_initial','2025-10-15 05:14:58.046268'),(16,'admin','0001_initial','2025-10-15 05:14:58.076039'),(17,'admin','0002_logentry_remove_auto_add','2025-10-15 05:14:58.079960'),(18,'admin','0003_logentry_add_action_flag_choices','2025-10-15 05:14:58.083556'),(19,'listings','0001_initial','2025-10-15 05:14:58.106584'),(20,'analytics','0001_initial','2025-10-15 05:14:58.114241'),(21,'analytics','0002_initial','2025-10-15 05:14:58.155232'),(22,'bookings','0001_initial','2025-10-15 05:14:58.159639'),(23,'bookings','0002_initial','2025-10-15 05:14:58.175818'),(24,'bookings','0003_initial','2025-10-15 05:14:58.196399'),(25,'listings','0002_initial','2025-10-15 05:14:58.258723'),(26,'reviews','0001_initial','2025-10-15 05:14:58.275584'),(27,'reviews','0002_initial','2025-10-15 05:14:58.301618'),(28,'sessions','0001_initial','2025-10-15 05:14:58.307684'),(29,'authtoken','0001_initial','2025-10-15 05:42:02.024287'),(30,'authtoken','0002_auto_20160226_1747','2025-10-15 05:42:02.037930'),(31,'authtoken','0003_tokenproxy','2025-10-15 05:42:02.063312'),(32,'authtoken','0004_alter_tokenproxy_options','2025-10-15 05:42:02.078076'),(33,'reviews','0003_review_is_approved','2025-10-15 15:47:12.925895'),(34,'listings','0003_listing_views_count','2025-10-16 12:25:15.531400'),(35,'analytics','0003_alter_searchhistory_options_and_more','2025-10-16 12:25:15.553303'),(36,'bookings','0004_alter_booking_options','2025-10-16 12:25:15.556528'),(37,'bookings','0005_alter_booking_options','2025-10-18 06:40:02.170642'),(38,'listings','0004_alter_listing_landlord','2025-10-20 09:12:47.659642'),(39,'bookings','0006_alter_booking_listing_alter_booking_tenant','2025-10-20 09:12:47.667509'),(40,'reviews','0004_alter_review_listing_alter_review_tenant','2025-10-20 09:12:47.674269'),(41,'analytics','0004_alter_searchhistory_user','2025-10-20 09:57:59.965388'),(42,'bookings','0007_alter_booking_total_price','2025-10-21 09:56:56.826025'),(43,'listings','0005_alter_listing_parking_price_per_day_and_more','2025-10-21 10:06:07.970170'),(44,'reviews','0005_alter_review_unique_together_and_more','2025-10-21 10:06:08.046236'),(45,'analytics','0005_alter_viewhistory_listing_alter_viewhistory_user','2025-10-21 10:27:59.740729'),(46,'users','0002_alter_user_phone_number','2025-10-22 08:37:38.435531'),(47,'listings','0006_alter_listing_bathroom_type_alter_listing_created_at_and_more','2025-10-22 14:05:36.659562'),(48,'reviews','0006_alter_review_comment_alter_review_is_approved_and_more','2025-10-22 14:05:36.670865');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dtfqmiuma2v2moi1knqvfopv905hxdou','.eJxVjDsOwjAQRO_iGln-JWso6TmDtV6vcQDZUpxUiLuTSCmgGmnem3mLgOtSwtp5DlMSF6HF6beLSE-uO0gPrPcmqdVlnqLcFXnQLm8t8et6uH8HBXvZ1oCAjrzRmdE7gDiM5CEZy0bZgRBBZa0zKKY8bmE1UzSJMGp3RiDx-QLshDiB:1vB4y1:sTSl38DYxMaWUJ0mEHeGLAnhS0GP-6o-cJOopGxzG04','2025-11-04 05:31:29.518446'),('kngrnwg68r2c8x6k53oqixsvn5kty4kz','.eJxVjDsOwjAQRO_iGln-JWso6TmDtV6vcQDZUpxUiLuTSCmgGmnem3mLgOtSwtp5DlMSF6HF6beLSE-uO0gPrPcmqdVlnqLcFXnQLm8t8et6uH8HBXvZ1oCAjrzRmdE7gDiM5CEZy0bZgRBBZa0zKKY8bmE1UzSJMGp3RiDx-QLshDiB:1v8tuC:5wJkw2g_qH2femkWwiQhsfl4LvMS8QVMCfrkr8O85AE','2025-10-29 05:18:32.789360');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listings`
--

DROP TABLE IF EXISTS `listings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `house_number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `property_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rooms` int unsigned DEFAULT NULL,
  `floor` int unsigned DEFAULT NULL,
  `has_elevator` tinyint(1) NOT NULL,
  `has_terrace` tinyint(1) NOT NULL,
  `has_balcony` tinyint(1) NOT NULL,
  `bathroom_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `has_internet` tinyint(1) NOT NULL,
  `has_parking` tinyint(1) NOT NULL,
  `daily_enabled` tinyint(1) NOT NULL,
  `price_per_day` decimal(10,2) DEFAULT NULL,
  `parking_price_per_day` decimal(10,2) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `main_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `landlord_id` bigint NOT NULL,
  `views_count` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `listings_city_675a5cce` (`city`),
  KEY `listings_is_active_75def8d1` (`is_active`),
  KEY `listings_landlord_id_668b53ec_fk_users_user_id` (`landlord_id`),
  KEY `listings_price_p_30e02a_idx` (`price_per_day`),
  KEY `listings_city_67a231_idx` (`city`),
  KEY `listings_is_acti_fd46bf_idx` (`is_active`),
  CONSTRAINT `listings_landlord_id_668b53ec_fk_users_user_id` FOREIGN KEY (`landlord_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `listings_chk_1` CHECK ((`rooms` >= 0)),
  CONSTRAINT `listings_chk_2` CHECK ((`floor` >= 0)),
  CONSTRAINT `listings_chk_3` CHECK ((`views_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listings`
--

LOCK TABLES `listings` WRITE;
/*!40000 ALTER TABLE `listings` DISABLE KEYS */;
INSERT INTO `listings` VALUES (1,'Cozy Apartment','Nice apartment in the city center','Greece','Athens','Main Street','12A',37.983800,23.727500,'apartment',2,3,1,1,1,'shower',1,1,1,50.00,5.00,0,0,'','2025-10-15 06:30:48.466272','2025-10-15 06:32:22.075423',1,0),(2,'Optimized didactic customer loyalty','Agency next idea product personal nor. Administration read law hospital provide baby interview. Listen place management result lose include size. Focus citizen side. Tv none run strategy generation meet north.','Germany','Spencerhaven','Melanie Cliffs','25767',45.690780,29.999571,'studio',5,8,1,1,0,'shower',0,1,1,86.67,11.26,1,0,'listing_images/IMG_001.jpg','2025-10-15 10:14:52.356622','2025-10-15 10:14:52.359460',63,0),(3,'Right-sized disintermediate protocol','Weight meet guess part main discover. Politics own adult water though gas. Next mouth actually work pass size age. Book number member federal candidate really. Different short attorney weight.','Germany','West Annettemouth','Wilson Locks','4305',54.778902,23.291303,'house',5,5,1,0,0,'bathtub',1,0,1,129.01,NULL,1,0,'listing_images/IMG_002.jpg','2025-10-15 10:14:52.361724','2025-10-15 10:14:52.363917',56,0),(4,'Versatile contextually-based adapter','Trip than throughout most single fear help. Like sell politics age return south per. Smile professor important see course. Article maintain wrong about. Too carry data.','Germany','South David','Amy Prairie','41659',54.417953,22.701175,'house',5,11,0,0,0,'bathtub',0,1,1,196.64,17.53,1,0,'listing_images/IMG_003.jpg','2025-10-15 10:14:52.365798','2025-10-15 10:14:52.367128',58,0),(5,'Business-focused bi-directional paradigm','Movie it often our final herself. Describe reality group head. Not rock letter material. Receive question investment wide far. Focus condition all various seem. You consider professional watch involve executive.','Germany','Dannyport','Silva Shores','113',51.316214,29.260996,'house',2,3,1,0,0,'bathtub',1,0,1,179.13,NULL,1,0,'listing_images/IMG_004.jpg','2025-10-15 10:14:52.368470','2025-10-15 10:14:52.369526',47,0),(6,'Secured interactive migration','Media might research. Stand political course though. Dark create from sell. Evidence player girl newspaper now heavy base.','Germany','Lake Rebeccaland','John Mill','472',53.053774,27.390909,'apartment',5,13,0,1,1,'shower',0,1,1,175.21,14.18,1,0,'listing_images/IMG_005.jpg','2025-10-15 10:14:52.370920','2025-10-15 10:14:52.372576',63,0),(7,'Progressive analyzing system engine','Site yes entire whether range almost visit. Simply process you matter cold prevent. Room get deep own. Always up property left than. Perform like pull manage. Campaign art during know far though wind focus.','Germany','South Lori','Harold Manor','341',47.321400,18.338262,'studio',5,9,1,0,0,'shower',0,0,1,199.86,NULL,1,0,'listing_images/IMG_006.jpg','2025-10-15 10:14:52.374013','2025-10-15 10:14:52.375342',54,0),(8,'Expanded client-server algorithm','Relate agent easy begin prepare represent late. Machine blue want culture much identify. Reflect color no hand doctor home section. Item charge store. Commercial movement campaign only instead. Company arrive southern prove mean treatment.','Germany','Smallchester','Rodriguez Field','748',53.891986,14.197967,'house',4,10,1,1,0,'bathtub',1,1,1,158.89,13.15,1,0,'listing_images/IMG_007.jpg','2025-10-15 10:14:52.376604','2025-10-15 10:14:52.377538',53,0),(9,'Future-proofed didactic groupware','Attack hit avoid hold show break. Have actually writer friend chair ability certainly. Choice economic wonder.','Germany','South Marcusville','Hannah Locks','23628',53.296579,19.326133,'apartment',4,11,1,1,1,'shower',1,0,1,187.39,NULL,1,0,'listing_images/IMG_008.jpg','2025-10-15 10:14:52.378701','2025-10-15 10:14:52.379649',59,0),(10,'Monitored needs-based neural-net','Floor note mention spend issue. Much buy seat involve able. Financial small financial none executive. Eye apply training trial specific. Behavior final cost she. Her talk space interesting.','Germany','Houstonton','Lopez Village','3117',50.994883,21.038367,'house',4,6,1,1,1,'shower',0,0,1,79.28,NULL,1,0,'listing_images/IMG_009.jpg','2025-10-15 10:14:52.380776','2025-10-15 10:14:52.381749',48,0),(11,'Seamless transitional methodology','Option author game news unit. After party wife public candidate able foreign. Carry blood go environment since off. And production hour.','Germany','Lisaview','Nichols Passage','418',45.465891,28.421191,'apartment',5,7,1,1,1,'bathtub',0,1,1,108.69,9.67,1,0,'listing_images/IMG_010.jpg','2025-10-15 10:14:52.382846','2025-10-15 10:14:52.383738',53,0),(12,'Advanced needs-based structure','Financial center price window few almost. Sense by lot address imagine against body. Mother blue party part wrong.','Germany','Cookchester','Peter Center','3307',51.048899,11.787845,'apartment',1,6,1,0,0,'bathtub',0,1,1,87.73,7.59,1,0,'listing_images/IMG_011.jpg','2025-10-15 10:14:52.384807','2025-10-15 10:14:52.385726',49,0),(13,'Automated didactic parallelism','Fast student truth clearly economy successful sell. Itself race wish own or attorney finish. Friend billion factor prepare.','Germany','Port Cheryl','Miller Avenue','8892',52.774809,10.209550,'apartment',1,12,0,1,1,'shower',0,1,1,45.57,6.98,1,0,'listing_images/IMG_012.jpg','2025-10-15 10:14:52.386793','2025-10-15 10:14:52.387663',52,4),(14,'Automated bottom-line artificial intelligence','Left accept receive while table wind. Rather play decision. Left green such in. Result parent church matter.','Germany','Newtonmouth','Richard Terrace','309',50.638668,13.624410,'apartment',5,13,0,1,1,'shower',1,1,1,45.70,7.56,1,0,'listing_images/IMG_013.jpg','2025-10-15 10:14:52.388723','2025-10-15 10:14:52.389594',56,0),(15,'Integrated attitude-oriented portal','Child stage win real key claim list kitchen. Gun fund across lead sport. Thank father them clearly nearly daughter wrong put. Term rather red fine agree.','Germany','Lauraville','Jason Branch','21884',48.904924,18.502284,'studio',4,10,1,1,0,'bathtub',1,0,1,55.00,NULL,1,0,'listing_images/IMG_014.jpg','2025-10-15 10:14:52.390650','2025-10-15 10:14:52.391554',60,0),(16,'Seamless methodical budgetary management','Still on wife under old game. Pretty avoid point. Worry strategy cut. Hear performance purpose PM. Skin election behavior knowledge identify together. Art former fire if.','Germany','New Gregory','Whitehead Club','8132',50.891151,13.043365,'house',5,10,0,0,0,'bathtub',1,1,1,72.82,9.79,1,0,'listing_images/IMG_015.jpg','2025-10-15 10:14:52.392707','2025-10-15 10:14:52.394015',63,1),(17,'Advanced holistic implementation','Great sign over performance. Half scientist usually none. Down fish west improve role station.','Germany','Sharonchester','Robert Passage','92952',50.224556,25.733171,'apartment',3,12,1,0,0,'bathtub',0,0,1,165.02,NULL,1,0,'listing_images/IMG_016.jpg','2025-10-15 10:14:52.395217','2025-10-15 10:14:52.396296',56,0),(18,'Networked dynamic encoding','Billion board need science. Friend democratic office. Next moment worker far benefit anything. Type since white effort your. Prove thousand difficult capital would over. Exactly painting social mouth.','Germany','New Susanmouth','Courtney Lake','7605',46.924725,23.424319,'studio',2,11,0,1,0,'shower',0,0,1,105.43,NULL,1,0,'listing_images/IMG_017.jpg','2025-10-15 10:14:52.397744','2025-10-15 10:14:52.398797',45,0),(19,'Synergistic object-oriented support','Open window up want teacher explain often theory. Their save spend let. Different can significant especially admit. Financial approach executive. Thought world as think color late.','Germany','New Elizabeth','Spencer Corner','668',52.454953,23.137139,'house',5,4,1,0,1,'shower',1,1,1,160.55,7.33,1,0,'listing_images/IMG_018.jpg','2025-10-15 10:14:52.400038','2025-10-15 10:14:52.400969',48,0),(20,'Organized cohesive encryption','Street into glass society travel dark. Executive assume evidence realize claim. Across usually trial sort mouth. Last system edge just generation try up.','Germany','New Brandyshire','Michael Viaduct','3456',51.357563,25.811686,'house',1,3,0,0,0,'bathtub',1,1,1,44.37,5.59,1,0,'listing_images/IMG_019.jpg','2025-10-15 10:14:52.402015','2025-10-15 10:14:52.402925',50,0),(21,'Public-key background utilization','Ground series find court message give. Energy these event training sing dog relationship. Five development weight hot true identify step.','Germany','Carterton','Amanda Inlet','71765',52.494191,16.063789,'apartment',4,12,0,1,0,'shower',0,1,1,48.13,11.03,1,0,'listing_images/IMG_020.jpg','2025-10-15 10:14:52.404033','2025-10-15 10:14:52.405046',61,0),(22,'Persevering 24/7 website','Action learn blue quickly beautiful yard. Player sound mean until sing event. Standard Mrs when writer appear system production. Listen drug family prove question police create. Nation less might area common lose arm at. Member long hundred during direction trouble experience around.','Germany','North Kristopher','Jennifer Run','8846',48.277576,22.092821,'apartment',5,15,1,0,1,'shower',1,1,1,157.62,17.64,1,0,'listing_images/IMG_021.jpg','2025-10-15 10:14:52.406411','2025-10-15 10:14:52.407851',60,0),(23,'Multi-lateral contextually-based Graphic Interface','Around ok campaign race without drop. Week sing customer sea else region need. Result hour cost cup economy discover nature. Half subject participant pressure knowledge.','Germany','Lisahaven','Chavez Green','2751',46.193554,13.367167,'apartment',2,8,1,0,1,'bathtub',1,0,1,109.41,NULL,1,0,'listing_images/IMG_022.jpg','2025-10-15 10:14:52.409609','2025-10-15 10:14:52.410890',59,0),(24,'Advanced discrete analyzer','Tend society prove home fire. Democrat describe occur center pay. Market modern prevent others buy while sort.','Germany','South Justin','Jennifer Light','7187',46.983804,20.858503,'house',3,10,0,1,0,'shower',0,1,1,155.15,6.20,1,0,'listing_images/IMG_023.jpg','2025-10-15 10:14:52.412306','2025-10-15 10:14:52.413503',2,0),(25,'Organized neutral hierarchy','Program fear agent budget organization ok along. Cell case go box kid street. Author heart notice think. Service project among author small do. Near base manager better throw write sister sure. Major have media community suggest exist.','Germany','East Audrey','Olson Union','1019',50.509628,24.614812,'apartment',2,10,0,1,0,'shower',0,0,1,59.87,NULL,1,0,'listing_images/IMG_024.jpg','2025-10-15 10:14:52.415148','2025-10-15 10:14:52.416218',51,0),(26,'Distributed encompassing data-warehouse','Sing century organization law. Both recent this table energy. Its economy politics. Be decade require tax. Better sit article when find.','Germany','Kristinafurt','Brown Station','0822',45.458489,16.734917,'house',2,15,1,1,1,'bathtub',0,0,1,89.87,NULL,1,0,'listing_images/IMG_025.jpg','2025-10-15 10:14:52.417677','2025-10-15 10:14:52.418898',45,0),(27,'Assimilated background encoding','Break determine in heart run paper. Summer detail simply range admit. Amount agreement the teach woman democratic. Vote new rise education born do trouble blood. Serious couple true serve federal find cold series.','Germany','North Tammymouth','Sherry Light','84002',51.588415,23.774655,'apartment',3,7,0,1,0,'bathtub',1,1,1,159.78,15.38,1,0,'listing_images/IMG_026.jpg','2025-10-15 10:14:52.420331','2025-10-15 10:14:52.421619',61,0),(28,'Profit-focused background initiative','Imagine news almost. Republican up resource middle. Central example across Democrat much. Tough former popular almost size street. Already past country. Job phone bit receive country beyond total.','Germany','South Jesse','Manuel Neck','767',52.997823,12.092098,'studio',3,6,0,1,1,'bathtub',0,0,1,175.50,NULL,1,0,'listing_images/IMG_027.jpg','2025-10-15 10:14:52.423248','2025-10-15 10:14:52.424353',54,0),(29,'Customizable multi-tasking open system','Factor sell fly high. Section TV bed peace term apply. Role of event control everyone institution hope. Debate necessary list knowledge. Measure recent bring. Look reality school strong since raise represent.','Germany','Timothyshire','Lisa Roads','82450',53.011181,11.381331,'house',1,11,0,0,0,'bathtub',0,0,1,45.71,NULL,1,0,'listing_images/IMG_028.jpg','2025-10-15 10:14:52.425555','2025-10-15 10:14:52.426564',46,0),(30,'Open-source fresh-thinking success','Early help site evening. So race who difference strategy. Painting even interest trade. Increase present stop perhaps. Population dream thousand spend million none be. Fill hope ahead second.','Germany','North Judithtown','Bowman Light','98726',49.811560,24.830018,'house',4,7,1,0,1,'shower',0,0,1,145.63,NULL,1,0,'listing_images/IMG_029.jpg','2025-10-15 10:14:52.427930','2025-10-15 10:14:52.429190',44,0),(31,'Function-based bi-directional extranet','Discussion people word investment woman TV. Develop hospital already recently. Environmental film statement point hotel.','Germany','South Janicehaven','Curtis Meadow','728',50.726489,27.745010,'house',5,3,1,0,0,'bathtub',0,0,1,84.99,NULL,1,0,'listing_images/IMG_030.jpg','2025-10-15 10:14:52.430733','2025-10-15 10:14:52.432008',56,0),(32,'Focused mobile complexity','Happen provide decision need project still wonder. Street attention measure big according senior particular. Attack administration product notice admit plant culture. Serious scientist quite customer. Her four last floor. Call they central foreign western nature reality.','Germany','South Danielmouth','Matthew Dam','791',49.729200,11.058587,'house',5,12,0,1,0,'bathtub',0,0,1,152.73,NULL,1,0,'listing_images/IMG_031.jpg','2025-10-15 10:14:52.433630','2025-10-15 10:14:52.434920',60,0),(33,'Programmable 24hour focus group','Tough kitchen against anything record. Various decide open it. Western child night consumer image. Pm kid change deep.','Germany','Lake Gerald','Tonya Shoals','7209',45.303068,13.913528,'house',3,3,0,1,1,'bathtub',0,0,1,178.89,NULL,1,0,'listing_images/IMG_032.jpg','2025-10-15 10:14:52.436424','2025-10-15 10:14:52.437999',63,0),(34,'Diverse coherent challenge','Stage such blood trial along bill price. Along along firm. Perhaps Congress picture teacher actually add speech. Writer reflect memory act.','Germany','Port Michaelberg','Hendrix Corner','6563',48.114173,19.338116,'apartment',1,14,0,0,0,'shower',1,1,1,137.77,11.18,1,0,'listing_images/IMG_033.jpg','2025-10-15 10:14:52.439671','2025-10-15 10:14:52.441418',58,0),(35,'Profound asymmetric emulation','Go center maintain but against east laugh. Stage prepare act nation. Can keep be quite question building data.','Germany','South Nicholas','Medina Rue','4470',45.310957,10.222398,'studio',3,7,1,1,0,'shower',1,1,1,143.11,15.46,1,0,'listing_images/IMG_034.jpg','2025-10-15 10:14:52.443137','2025-10-15 10:14:52.444624',2,0),(36,'Profit-focused value-added website','War such order morning nice. Reveal middle news feeling key property. Meeting month performance let rest. Current remain watch threat threat.','Germany','Briggsside','Jeffrey Haven','2866',47.720889,28.716728,'apartment',1,11,0,1,0,'bathtub',0,0,1,160.16,NULL,1,0,'listing_images/IMG_035.jpg','2025-10-15 10:14:52.446336','2025-10-15 10:14:52.447756',53,0),(37,'Total fault-tolerant time-frame','Oil risk produce huge music them wall. Social new war also. Lawyer organization budget majority side chair care certainly. Stock something green reduce. Practice growth professor anyone piece stage professional.','Germany','Port Derrick','Stephen Drive','277',53.255956,25.509685,'apartment',3,6,1,1,1,'shower',1,0,1,175.99,NULL,1,0,'listing_images/IMG_036.jpg','2025-10-15 10:14:52.449260','2025-10-15 10:14:52.450385',53,0),(38,'Reactive zero administration leverage','True Democrat nearly question talk fly. Size bad include pull house make future. Suffer of detail financial loss show cost. Perhaps may coach should exist nice shoulder message. Dog make phone.','Germany','Robertsberg','Caitlyn Knoll','75050',49.165477,11.772109,'studio',1,5,1,0,0,'bathtub',1,0,1,88.06,NULL,1,0,'listing_images/IMG_037.jpg','2025-10-15 10:14:52.451691','2025-10-15 10:14:52.452977',58,0),(39,'Enhanced non-volatile instruction set','How your rest himself. By shoulder enter. Spring let hotel send treat especially mind. Market degree main bill husband.','Germany','Simpsonfort','Stephen Ford','564',54.346883,22.687955,'studio',4,1,1,1,0,'bathtub',1,1,1,126.29,16.01,1,0,'listing_images/IMG_038.jpg','2025-10-15 10:14:52.454456','2025-10-15 10:14:52.456941',55,0),(40,'Public-key bi-directional access','Run surface strategy woman fine daughter offer. Key audience far somebody military character. Policy season mind phone point unit view. Car care possible sort interview magazine who local. Current save resource officer him church surface environmental. Member if tend expert reality walk.','Germany','West Rachel','Wright Meadows','0185',49.257688,15.353792,'apartment',1,3,0,1,0,'shower',0,1,1,137.75,13.84,1,0,'listing_images/IMG_039.jpg','2025-10-15 10:14:52.459296','2025-10-15 10:14:52.461169',44,0),(41,'Digitized intangible product','Choice hope hot describe forward. Care lay local probably model environmental firm. Reach cause hear. All environment start according group until. Respond goal federal story.','Germany','Schneiderfort','Hudson Grove','3316',54.929279,10.668465,'apartment',2,10,1,1,0,'shower',0,1,1,108.97,9.21,1,0,'listing_images/IMG_040.jpg','2025-10-15 10:14:52.462956','2025-10-15 10:14:52.464756',60,0),(42,'Switchable incremental moratorium','Step picture leave receive computer. Last east none enjoy whole spring peace. Dream true yes candidate. Leg term not former.','Germany','North Nicolebury','Audrey Squares','753',51.726859,25.227999,'studio',1,15,0,1,1,'shower',0,0,1,59.21,NULL,1,0,'listing_images/IMG_041.jpg','2025-10-15 10:14:52.467398','2025-10-15 10:14:52.471264',44,0),(43,'Reactive bifurcated methodology','Trip fire Mr customer see son area. Deep wall begin plan bill move. Service certain effect none. Tax dream hour subject store identify actually.','Germany','Greenfurt','Harris Neck','33528',45.418870,22.855819,'house',2,12,0,1,0,'bathtub',0,0,1,146.18,NULL,1,0,'listing_images/IMG_042.jpg','2025-10-15 10:14:52.473307','2025-10-15 10:14:52.475019',59,0),(44,'Fully-configurable scalable customer loyalty','My guess from front pressure candidate society. Hospital explain line present late performance. But art score impact. Question should would authority bank. Pretty can how need be week open performance.','Germany','New David','Powers Club','662',52.075471,24.293089,'studio',1,6,1,1,1,'bathtub',0,0,1,181.77,NULL,1,0,'listing_images/IMG_043.jpg','2025-10-15 10:14:52.476583','2025-10-15 10:14:52.479036',49,0),(45,'Self-enabling high-level application','Word commercial word history. Stop century cup idea goal soon. Between theory until. Owner successful audience structure more. Benefit increase growth attorney others entire.','Germany','Jennifermouth','Phillips Union','454',51.437445,10.387218,'apartment',1,6,1,0,0,'bathtub',0,1,1,195.81,19.12,1,0,'listing_images/IMG_044.jpg','2025-10-15 10:14:52.480529','2025-10-15 10:14:52.482431',62,0),(46,'Programmable impactful help-desk','Admit suddenly west wall. Least lose will final who any. Company future level this food help. Real capital have put. Truth remain finish company star upon.','Germany','New Jackson','Cody Way','47442',52.670194,29.268335,'apartment',2,2,1,0,0,'bathtub',1,0,1,84.89,NULL,1,0,'listing_images/IMG_045.jpg','2025-10-15 10:14:52.484122','2025-10-15 10:14:52.485822',50,0),(47,'Integrated hybrid archive','Name interest Democrat need happen share. Five early member hundred alone wrong person stuff. Know language land mind why address apply. Discover increase huge exactly. Machine view center. Ready art the.','Germany','Williamtown','Sandra Avenue','7487',48.915813,27.422899,'studio',4,3,0,0,1,'bathtub',1,1,1,156.35,12.34,1,0,'listing_images/IMG_046.jpg','2025-10-15 10:14:52.487440','2025-10-15 10:14:52.489297',45,1),(48,'Enhanced logistical application','Sign experience support network finally. Property himself cell whatever woman. Himself better treat guy cup dream.','Germany','Crystalview','Hall Vista','5354',51.146389,21.004135,'apartment',4,13,1,0,0,'bathtub',0,0,1,71.17,NULL,1,0,'listing_images/IMG_047.jpg','2025-10-15 10:14:52.491030','2025-10-15 10:14:52.493024',61,0),(49,'Open-architected 24/7 circuit','As compare suffer student likely trouble. Accept consider more standard. Leave decade seem become plan eye. Account themselves fear rest cup point. Old reason here today reality most past development.','Germany','Brownmouth','Bethany Island','395',46.402529,28.944571,'studio',1,14,1,0,1,'shower',0,1,1,87.39,14.03,1,0,'listing_images/IMG_048.jpg','2025-10-15 10:14:52.494663','2025-10-15 10:14:52.496299',62,0),(50,'Streamlined executive interface','Approach her page sport health share. Ahead teacher report rock. Finally people paper candidate. Son staff necessary environmental bad. Help early buy responsibility cold. Make on require voice doctor message.','Germany','Erikafort','Hicks Fords','7405',49.738508,29.284161,'house',2,3,0,1,1,'shower',0,0,1,49.00,NULL,1,0,'listing_images/IMG_049.jpg','2025-10-15 10:14:52.497896','2025-10-16 05:14:14.448519',63,0),(51,'Robust 24hour process improvement','Reduce program what become half area hour. Water thank instead financial recognize expert give including. Health despite member. Maybe scene look southern. Fast answer follow news.','Germany','Camposhaven','Frey Station','8073',53.962099,24.034009,'house',1,13,1,1,0,'bathtub',1,0,1,33.90,NULL,1,0,'listing_images/IMG_050.jpg','2025-10-15 10:14:52.501502','2025-10-15 10:14:52.503056',49,0),(52,'Operative zero administration hierarchy','Environmental follow result ball baby really. Us spring board quite. Operation happy attention receive. Girl morning ahead detail personal speak ball. Learn heart claim these both street theory. Television thing build image wrong evidence kitchen.','Germany','South Cliffordtown','Mills Villages','603',50.682494,11.568261,'apartment',3,2,1,1,1,'bathtub',1,1,1,48.73,14.58,1,0,'listing_images/IMG_001_9DtAxCp.jpg','2025-10-15 10:14:52.504757','2025-10-15 10:14:52.506922',47,0),(53,'Digitized 6thgeneration knowledgebase','Choose know enough sort. Before success heavy bring probably collection of simply. Law forget rock since around.','Germany','Debrahaven','Danielle Track','7399',52.345407,17.100536,'studio',3,13,1,1,0,'shower',1,1,1,83.51,6.92,1,0,'listing_images/IMG_002_lG7F8bX.jpg','2025-10-15 10:14:52.508909','2025-10-15 10:14:52.511995',48,0),(54,'Multi-channeled intermediate focus group','Door produce imagine group. Page seem particular raise number month share heart. Far argue night sound according tonight actually. Attack artist indicate. Again trial term avoid can husband. If source street here hit cold.','Germany','Rivasside','Page Springs','38038',47.431193,24.100087,'house',1,7,0,0,0,'shower',0,1,1,150.20,5.51,1,0,'listing_images/IMG_003_jLcdAxN.jpg','2025-10-15 10:14:52.514749','2025-10-15 10:14:52.516665',44,0),(55,'Intuitive well-modulated data-warehouse','Official improve at ball large would. Green effort large tax two show child. Everybody recognize position finally red response.','Germany','East Jordanside','Mark Fort','7691',54.143876,10.889618,'apartment',2,3,1,1,1,'bathtub',0,0,1,33.19,NULL,1,0,'listing_images/IMG_004_T16G1P1.jpg','2025-10-15 10:14:52.518256','2025-10-16 05:13:00.588103',50,0),(56,'Decentralized high-level paradigm','Study somebody responsibility hit easy. Which father picture suddenly people. Decide investment finish staff PM real five.','Germany','Caseyshire','Joshua Throughway','83278',53.799663,12.501147,'house',1,2,0,0,0,'bathtub',0,0,1,46.30,NULL,1,0,'listing_images/IMG_005_4dgGpiH.jpg','2025-10-15 10:14:52.522254','2025-10-15 10:14:52.525001',59,0),(57,'Cross-group empowering Local Area Network','Business able into court single material late. Audience at rate left. Per summer statement beautiful eat. Tend then word own boy challenge. Site eye science major. Actually spend subject particularly similar pick.','Germany','New Crystal','Johnson Viaduct','0725',54.899866,29.559150,'house',2,6,1,0,1,'bathtub',0,0,1,56.54,NULL,1,0,'listing_images/IMG_006_2Yq76VQ.jpg','2025-10-15 10:14:52.527628','2025-10-15 10:14:52.530466',56,0),(58,'Fully-configurable mission-critical toolset','Family security one somebody trial stuff call. Quickly contain usually team break usually shoulder. Close reduce media guess appear commercial culture. Light society ever than. Most fish however father.','Germany','South Brianna','Williams Street','66470',52.329819,14.149314,'apartment',5,8,1,1,0,'shower',1,1,1,158.08,17.88,1,0,'listing_images/IMG_007_nTfePNY.jpg','2025-10-15 10:14:52.532842','2025-10-15 10:14:52.535586',60,0),(59,'Ameliorated maximized Local Area Network','Effect really memory new laugh different. Sure investment almost. Traditional only perform Mr everybody. Teacher cold skin happen see old sell right.','Germany','East Katie','Brady Trail','810',49.169103,20.572259,'studio',5,2,1,0,1,'shower',0,0,1,156.61,NULL,1,0,'listing_images/IMG_008_AeLN3ST.jpg','2025-10-15 10:14:52.537972','2025-10-15 10:14:52.541034',49,0),(60,'Robust neutral algorithm','Everyone decade media always stuff. Organization drug purpose day administration. Practice team simply job onto green eye. Middle approach trade interview however material consider husband.','Germany','Williamfort','Hester Ridges','65392',45.996510,15.316567,'studio',1,11,1,1,1,'bathtub',0,1,1,148.95,7.71,1,0,'listing_images/IMG_009_QUQzEu1.jpg','2025-10-15 10:14:52.543221','2025-10-15 10:14:52.545685',45,0),(61,'Fundamental value-added capacity','North agent enough. Control offer material everyone continue. Most bring involve hundred bring employee summer. Former add study leg somebody.','Germany','North Brandon','Andrews Vista','1388',46.007687,21.789611,'studio',4,8,0,1,1,'bathtub',0,1,1,115.22,11.27,1,0,'listing_images/IMG_010_jRlqZgj.jpg','2025-10-15 10:14:52.547583','2025-10-15 10:14:52.550339',63,0),(62,'Configurable well-modulated website','Thousand probably central safe nearly. Answer professor alone resource. Between international we save agency question better. Moment stand cut. Shoulder third believe enough left. Total painting save ahead call.','Germany','Lorimouth','Kevin Motorway','136',51.194746,14.290861,'house',4,8,1,0,0,'bathtub',0,1,1,197.17,14.43,1,0,'listing_images/IMG_011_xmGAHZQ.jpg','2025-10-15 10:14:52.552669','2025-10-15 10:14:52.555294',61,0),(63,'Integrated global paradigm','Answer much visit itself dark already. Develop reason day note hundred particular. Smile year thought material decade. Buy contain ever positive. Live safe benefit agent brother whatever. Health else weight energy outside can whose.','Germany','Silvaside','Michael Lake','52860',47.659467,25.837261,'house',5,3,0,1,1,'shower',0,0,1,39.28,NULL,1,0,'listing_images/IMG_012_Az7tQ8g.jpg','2025-10-15 10:14:52.557321','2025-10-15 10:14:52.559746',58,0),(64,'Diverse multimedia project','Determine manager how type difference think either. Have sell imagine purpose hope smile set. Item out war true night. Agreement key figure born write. Fire task idea food serious article close. Born street chair approach scientist.','Germany','Garciamouth','Cook Forges','6685',48.578750,29.741070,'apartment',5,12,0,0,0,'bathtub',0,0,1,152.24,NULL,1,0,'listing_images/IMG_013_eFMkYEx.jpg','2025-10-15 10:14:52.561892','2025-10-15 10:14:52.564491',58,0),(65,'Profit-focused contextually-based encoding','Beautiful but begin player should federal southern grow. Even almost democratic whatever hard. Structure clear who true bad. Beat mother child also. Recently left wide necessary company. Team chance those main.','Germany','Sawyerfort','Gray Parks','6137',54.924154,20.288058,'house',4,7,1,0,0,'bathtub',0,1,1,70.26,15.79,1,0,'listing_images/IMG_014_8mM6bsn.jpg','2025-10-15 10:14:52.567022','2025-10-15 10:14:52.569745',57,0),(66,'Synchronized bandwidth-monitored solution','Box money letter movie along look red. Building any cold structure. Perform even past fund night from.','Germany','North Robertview','Michael Valleys','15690',45.395780,15.929183,'house',5,7,0,0,1,'shower',0,0,1,157.91,NULL,1,0,'listing_images/IMG_015_QRfxqIg.jpg','2025-10-15 10:14:52.571190','2025-10-15 10:14:52.572480',45,0),(67,'Multi-layered client-driven function','Over indicate customer. Theory newspaper fact seat population politics. Maybe party inside service sound month. Significant difference activity billion. Paper year beat next day age. Whom each break pressure send large.','Germany','New Dawn','David Tunnel','12993',45.898911,27.075576,'house',1,6,1,1,1,'shower',1,0,1,142.78,NULL,1,0,'listing_images/IMG_016_3HiXoX7.jpg','2025-10-15 10:14:52.573776','2025-10-15 10:14:52.575326',51,0),(68,'Business-focused stable contingency','Visit policy become. Charge could author eye sing. Always laugh PM help center forward ground. You provide could create agreement control. Half order sea table try room read.','Germany','Chapmanview','Cynthia Summit','3686',50.911795,27.406053,'studio',5,5,0,0,0,'shower',0,0,1,198.86,NULL,1,0,'listing_images/IMG_017_rv9bki7.jpg','2025-10-15 10:14:52.577026','2025-10-15 10:14:52.578797',53,0),(69,'Exclusive intangible service-desk','Your base strong worry few. Television town off task represent. Tv born wonder event nice region. Fill run government different here. Citizen ability factor return on ago near.','Germany','West Natasha','Dean Stream','8162',54.154274,21.958219,'house',4,6,0,1,1,'shower',0,1,1,46.92,9.70,1,0,'listing_images/IMG_018_ptb9LwA.jpg','2025-10-15 10:14:52.580680','2025-10-15 10:14:52.582296',58,0),(70,'Implemented asymmetric installation','Beautiful or grow ok each friend beyond. Everybody doctor tend everything gas. Live rather ahead understand. Since away will since loss.','Germany','Annaburgh','Thomas Land','6605',53.061745,19.624813,'apartment',3,1,0,1,0,'shower',0,0,1,196.82,NULL,1,0,'listing_images/IMG_019_uRO1Lb1.jpg','2025-10-15 10:14:52.583474','2025-10-15 10:14:52.584909',53,0),(71,'Public-key leadingedge challenge','Sea management finish. Start write join music because theory. Seek wife ask. Thank drive television ability. Bed compare drive. Believe treatment reach strategy.','Germany','Murphymouth','Obrien Rapid','25392',53.929130,10.041701,'studio',4,11,0,1,0,'bathtub',0,0,1,90.29,NULL,1,0,'listing_images/IMG_020_gCgp7rW.jpg','2025-10-15 10:14:52.586527','2025-10-15 10:14:52.588034',59,0),(72,'Quality-focused didactic open architecture','Speak garden speech assume reveal floor. Dog professional this return where mention. Network theory hospital. Large poor life always.','Germany','Jesseville','Richard Union','99302',51.408033,26.599019,'studio',2,6,0,0,0,'shower',1,0,1,145.92,NULL,1,0,'listing_images/IMG_021_Lo0F8kL.jpg','2025-10-15 10:14:52.589798','2025-10-15 10:14:52.591179',44,0),(73,'Sharable interactive implementation','Receive senior look value manager community. Green week face only here image. Hear life heart indicate. Think artist he situation stage top speech. City significant movie act theory. Able stock official admit one region.','Germany','Barbaramouth','Desiree Circle','4674',50.880184,19.032799,'studio',5,14,0,0,1,'bathtub',0,1,1,131.07,8.70,1,0,'listing_images/IMG_022_J2FkPou.jpg','2025-10-15 10:14:52.593372','2025-10-15 10:14:52.595621',58,0),(74,'Customizable incremental solution','Oil good guy account clearly door. Join most bit. Only would hospital watch throughout decision knowledge. South local food instead window grow public. Population worry fact at become measure.','Germany','New Mikaylafurt','Ellis Club','1878',46.768482,28.176391,'studio',3,13,1,1,0,'shower',1,0,1,115.55,NULL,1,0,'listing_images/IMG_023_31sjQZn.jpg','2025-10-15 10:14:52.597542','2025-10-15 10:14:52.598713',54,0),(75,'Grass-roots tertiary methodology','Tough pass strong other suffer action I. Wait result every door wonder affect will baby. Ok give address school business space. Near fly machine else see close never sister. Food structure win attorney sit whatever. Clearly cause rate mother bank.','Germany','Lake Garyfurt','Chung Trafficway','916',50.627284,22.354578,'house',2,3,0,0,1,'bathtub',0,0,1,198.20,NULL,1,0,'listing_images/IMG_024_spftuzA.jpg','2025-10-15 10:14:52.600327','2025-10-15 10:14:52.601710',61,1),(76,'Programmable bottom-line forecast','Already take source popular cut certain. Particular Mr international himself. Term clearly marriage discussion teach party field. Until their type today care central. Window use knowledge stop future unit. Similar discuss each take.','Germany','Kimberlyborough','Thomas Islands','0103',52.530778,21.515986,'house',1,6,1,0,0,'shower',1,0,1,41.85,NULL,1,0,'listing_images/IMG_025_1rwqRd4.jpg','2025-10-15 10:14:52.603060','2025-10-15 10:14:52.604457',44,0),(77,'Profound user-facing system engine','Able prove budget major. Price per avoid for. Majority experience other including after for lot. True course generation west.','Germany','Kristieland','Page Roads','9623',46.187681,27.109030,'apartment',5,1,1,1,1,'bathtub',1,1,1,129.20,16.09,1,0,'listing_images/IMG_026_S10Nw2d.jpg','2025-10-15 10:14:52.606088','2025-10-15 10:14:52.607369',52,0),(78,'Versatile regional project','Cover bag able natural. Glass stay special sea push him. Nearly energy contain mother understand.','Germany','Amandaville','Christopher Junctions','3151',47.859140,14.021391,'studio',5,4,1,1,1,'shower',1,1,1,62.17,10.85,1,0,'listing_images/IMG_027_n05ng3Z.jpg','2025-10-15 10:14:52.608907','2025-10-15 10:14:52.610073',52,1),(79,'Synergized logistical access','Newspaper who forget drug realize. Hospital exactly industry consumer wonder however TV. Local common white source central brother staff. Official turn minute. President window fall base defense. And federal expert country speak.','Germany','Courtneyton','Rich Landing','34198',48.484473,11.852202,'apartment',4,11,1,1,0,'bathtub',1,0,1,107.87,NULL,1,0,'listing_images/IMG_028_SGAIkpL.jpg','2025-10-15 10:14:52.611881','2025-10-15 10:14:52.613174',54,0),(80,'Grass-roots transitional conglomeration','Court police relationship any. Like agree help along. Option industry whose floor network. Star west order husband. Any feeling level consider bad.','Germany','Port Thomas','Rogers Forks','837',50.316980,23.499469,'apartment',4,13,0,0,1,'shower',1,0,1,38.62,NULL,1,0,'listing_images/IMG_029_rpQO2xU.jpg','2025-10-15 10:14:52.614594','2025-10-15 10:14:52.615601',63,0),(81,'Triple-buffered client-server parallelism','Standard catch one building laugh. Consider work teach everything. News Mr change manage gun five friend. Main base usually natural heart. Every help plant around total.','Germany','West Jeffrey','Laurie Radial','9398',54.004212,28.301307,'apartment',5,14,0,0,0,'shower',0,1,1,39.83,18.60,1,0,'listing_images/IMG_030_UFeWLkU.jpg','2025-10-15 10:14:52.617318','2025-10-15 10:14:52.618634',57,0),(82,'Cozy apartment in central Tashkent','Spacious apartment with modern renovation, close to the metro and shops.','Uzbekistan','Tashkent','Shota Rustaveli','12A',41.311081,69.240562,'apartment',3,5,1,1,0,'bathtub',1,0,1,14.00,NULL,1,0,'','2025-10-16 06:02:36.380199','2025-10-16 06:12:39.680979',1,0),(84,'Affordable apartment in the heart of Hamburg','A bright and cozy apartment located in the city center of Hamburg, ideal for both short and medium stays. The property features a modern shower bathroom, balcony and terrace, high-speed internet, and convenient on-site parking. Suitable for students, travelers, or professionals visiting the city.','Germany','Hamburg','Jungfernstieg','14',53.553406,9.992196,'apartment',4,3,1,1,1,'shower',1,1,1,75.00,10.00,1,0,'','2025-10-21 05:39:49.162751','2025-10-21 05:41:54.725340',54,1),(85,'Cozy Apartment in Vienna Center','A modern and comfortable apartment located in the heart of Vienna, close to public transport and major attractions.','Austria','Vienna','Mariahilfer Strasse','25',48.200000,16.366700,'apartment',2,3,1,0,1,'shower',1,0,1,120.00,0.00,1,0,'','2025-10-22 14:38:14.000276','2025-10-22 14:38:14.000320',63,0);
/*!40000 ALTER TABLE `listings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_review`
--

DROP TABLE IF EXISTS `reviews_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` smallint unsigned NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `listing_id` bigint NOT NULL,
  `tenant_id` bigint NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_review_per_listing_tenant` (`listing_id`,`tenant_id`),
  KEY `reviews_review_tenant_id_146c76a8_fk_users_user_id` (`tenant_id`),
  KEY `reviews_review_listing_id_dc99369e` (`listing_id`),
  CONSTRAINT `reviews_review_listing_id_dc99369e_fk_listings_id` FOREIGN KEY (`listing_id`) REFERENCES `listings` (`id`),
  CONSTRAINT `reviews_review_tenant_id_146c76a8_fk_users_user_id` FOREIGN KEY (`tenant_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `reviews_review_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_review`
--

LOCK TABLES `reviews_review` WRITE;
/*!40000 ALTER TABLE `reviews_review` DISABLE KEYS */;
INSERT INTO `reviews_review` VALUES (1,5,'Alles ok!!! Super!!!','2025-10-17 11:04:24.763557',13,36,1),(2,5,'It was great! Great host!','2025-10-18 05:59:40.964823',53,34,1),(3,4,'Rating 4 because we had to wait 30 minutes for the owner to check in.','2025-10-18 06:05:40.721944',7,28,1),(4,5,'Everything was wonderful! The view from the window was great. I especially loved the coffee machine! It was absolutely fantastic!!!','2025-10-18 06:10:38.039587',38,27,1),(5,3,'It was very cold!!!','2025-10-19 05:35:36.154740',82,24,1),(6,5,'Super!!! Great urlaub!!!','2025-10-20 05:45:04.162863',78,4,1),(7,4,'Very noisy neighbors','2025-10-22 06:40:32.071909',76,41,1);
/*!40000 ALTER TABLE `reviews_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `username` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone_number` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$1000000$o18IuKWfmsXwuYmOVTMQUk$IIMMO3ZvsCulvwuf2O0Lu3wuzpYXoIYTGkIwBU4VLww=','2025-10-21 05:31:29.517315',1,'','',1,1,'admin','example@example.com','tenant','2025-10-15 05:17:54.666113',NULL),(2,'pbkdf2_sha256$1000000$kW2v79Obzlth6Qxkh79KRM$cEa2biR1CjPIT9fZtDN1Jf69cZRHyO5eHR7PX6CmsaM=',NULL,0,'John','Doe',0,1,NULL,'test@example.com','landlord','2025-10-15 05:39:58.063291','8573936376'),(3,'pbkdf2_sha256$1000000$iLWsCuqujqDmqsl7hvNTJ7$yy09ojmrSzQGFGidCNk+G5Lz0VMD2W3iK3QttmYu3Q4=',NULL,0,'John','Doe',0,1,NULL,'landlord@example.com','tenant','2025-10-15 06:03:40.404367',NULL),(4,'pbkdf2_sha256$1000000$V6xAAfUKnHjbKLYveSPWuC$RcbYTPN8kba7vn0KOJABcHGKp+60i5s4IV0CrY77qcY=',NULL,0,'Richard','Robinson',0,1,'jonesmichael','masontiffany@example.com','tenant','2025-10-15 09:40:39.849062','+1-873-532-0789'),(5,'pbkdf2_sha256$1000000$c0vbgMnrtTVzHYRMNAndzY$/4Aek8y9g0r52FkRlJmXxKJYNwIeJFth2ZXxzkYA2ek=',NULL,0,'Christopher','Simmons',0,1,'richardslaurie','gonzalezdaniel@example.com','tenant','2025-10-15 09:40:39.976133','5783207871'),(6,'pbkdf2_sha256$1000000$23H3Mh9aL1c7I9B3vUPYnM$mQc5mMRKkuehLlAQnwOg2nQAstMu9T5jpr7nc/H5ZTo=',NULL,0,'Kimberly','Munoz',0,1,'brittany54','armstrongpaul@example.net','tenant','2025-10-15 09:40:40.102998','001-588-488-356'),(7,'pbkdf2_sha256$1000000$UktzWjHrw0IelEeQuIXPCB$Y4/Cx2eWFB4BZPc2iFpnwAE6ySENKcOaAVN6V4yl7vs=',NULL,0,'Daniel','Roberts',0,1,'deborahhawkins','john74@example.com','tenant','2025-10-15 09:40:40.231119','(287)289-3196x6'),(8,'pbkdf2_sha256$1000000$iUA4ygSzkFpCaTPOzKwW7l$M/R3dz9MWBK0omivVk3RHjbr1F8TA425hdmP9OABlww=',NULL,0,'Lauren','Snyder',0,1,'melanieberry','michaelsmith@example.net','tenant','2025-10-15 09:40:40.361421','+1-382-298-2559'),(9,'pbkdf2_sha256$1000000$LSSQJV68TLdL6PateAVfJN$ePsPusST72N283LHI9FUFhghRSDmdB62AlOQmzzO1kA=',NULL,0,'Paul','Blair',0,1,'john50','corey86@example.com','tenant','2025-10-15 09:40:40.490371','001-437-522-076'),(10,'pbkdf2_sha256$1000000$JJNvX4Fwj7ydZ8lzKBWYJP$MHrlMwQtxIQPRZQgGWtMHh2h8j/X55LjqG+3KeqBm58=',NULL,0,'Miguel','Mason',0,1,'jamesbutler','ugonzales@example.com','tenant','2025-10-15 09:40:40.618289','+1-524-278-5216'),(11,'pbkdf2_sha256$1000000$R7S4r3Fo236L815WxvHMyz$6QqknnCZcOZSGRqlO1Js2y0h6V8cOdXakn7KJ7CnBpI=',NULL,0,'Ryan','Allen',0,1,'christopher14','kellysusan@example.com','tenant','2025-10-15 09:40:40.747290','(297)965-9646x9'),(12,'pbkdf2_sha256$1000000$EAns9tHP7gdymESDx3u4pT$KooB+rKifpnssbhm6zABHsJx0U8WMMxwgVSZ41X94+k=',NULL,0,'James','Day',0,1,'boneal','emilyclark@example.com','tenant','2025-10-15 09:40:40.879192','788-757-1284x37'),(13,'pbkdf2_sha256$1000000$KDRlPcXz6aKxtSlX3Cjg9f$Mky+tMhlYY3ye34gCKoJBm4IffDFL/zwHY0knaHcFHY=',NULL,0,'Brenda','Soto',0,1,'angela12','bernardashley@example.org','tenant','2025-10-15 09:40:41.012647','001-581-773-875'),(14,'pbkdf2_sha256$1000000$G9j8vRugiwFdGjkW8h3UBi$GroxCwS4W36m87NUPfJ3HluiYK8PyttdAMsRyTJWKAU=',NULL,0,'John','Walker',0,1,'hernandezsarah','melinda14@example.net','tenant','2025-10-15 09:40:41.144766','001-853-538-661'),(15,'pbkdf2_sha256$1000000$4CaJ2qYKk0N9R9nbK8Krsm$yE8w+eRwe4Pp5PLSWW7tydsaNWbXh5cx/fSF65vxrJI=',NULL,0,'Terry','Miller',0,1,'teresaowen','michaelsmith@example.org','tenant','2025-10-15 09:40:41.272834','001-635-871-493'),(16,'pbkdf2_sha256$1000000$lBesc2ryBPOeOr0AAcHSuh$BMalwDjjqjjT8CG+KUYb9dCuPr3IguSThHgoxAk1q2s=',NULL,0,'Brian','Anderson',0,1,'margaret76','clinebrandy@example.com','tenant','2025-10-15 09:40:41.402087','2268933366'),(17,'pbkdf2_sha256$1000000$uSuBvzoiOkZJS6xZohlfB7$tbdYBjXA64KExXRFeQKl/hyKoSSW/F5v/yWKBcIEgiE=',NULL,0,'Wendy','Brown',0,1,'jeremiah87','mdavis@example.com','tenant','2025-10-15 09:40:41.529313','+1-548-361-1409'),(18,'pbkdf2_sha256$1000000$yPx7MmDsx10DDlqp1xuQ4I$menzpaIVKtpnSxrgZ9s8DhU+X37cOJ+VK7MZXAaMNcs=',NULL,0,'Debra','Perez',0,1,'rosederek','george52@example.org','tenant','2025-10-15 09:40:41.659489','2396718281'),(19,'pbkdf2_sha256$1000000$Imlohszq6D0VemNbdSjzdd$NwOscaMhGxGtk42BO5KBccS4z90/B7WCs9F1nBa3/BA=',NULL,0,'James','Smith',0,1,'cpayne','mariaray@example.net','tenant','2025-10-15 09:40:41.787396','(976)298-6609'),(20,'pbkdf2_sha256$1000000$xlWmgPztQTlypMBtoRAEJO$hHZRk09527s+Y8G+KN7j6qJ7XSTT2sZSc0IgAXN+Fhg=',NULL,0,'Dylan','Guzman',0,1,'karenhernandez','fitzpatrickcolleen@example.org','tenant','2025-10-15 09:40:41.918185','001-828-275-916'),(21,'pbkdf2_sha256$1000000$UHkvYVk6jwsyNWr3zX2JdN$kJht5IjhbGAYgnoiO4ZBW8emACYoR0rTT/tYKzbyZzE=',NULL,0,'Jessica','Santiago',0,1,'orozcojennifer','pcarter@example.com','tenant','2025-10-15 09:40:42.046772','001-675-806-584'),(22,'pbkdf2_sha256$1000000$k2ghgbzaj95oqe4nOtsNm0$vgceNBeWSfRdYpdNusew1eKR2TVgcPFoc1zRGxOLnuQ=',NULL,0,'Courtney','Carpenter',0,1,'jonesmarc','christinemarsh@example.com','tenant','2025-10-15 09:40:42.176673','5415066202'),(23,'pbkdf2_sha256$1000000$xtR3h3F4LRGzFGCKi2nnfS$RuA94YltzkWeqWHyatzADAxSJLB45BFxXsyZ3jglh/w=',NULL,0,'Sean','Cook',0,1,'bradley56','shughes@example.org','tenant','2025-10-15 09:40:42.304462','3804307688'),(24,'pbkdf2_sha256$1000000$DvqSfy9RIcaplNgqnHXu9e$74pzxViPafukn8m8+pPqVen0k8LW7kg195Hqmcuce3Y=',NULL,0,'Martha','Pearson',0,1,'qgates','vmcpherson@example.net','tenant','2025-10-15 09:40:42.433317','(524)543-5406x4'),(25,'pbkdf2_sha256$1000000$oF85yi2sjCMjwua3pMoUjU$55m/tQc1dyXv6oT5I0SVH1EnJMsOXBhY8/hixBTq0l0=',NULL,0,'Traci','Jimenez',0,1,'allison67','wardchristopher@example.net','tenant','2025-10-15 09:40:42.560556','589.763.1825x92'),(26,'pbkdf2_sha256$1000000$zPPGd8aHn4vG7QugVfyKPB$xSHUJfYQGnQ5Pm2/S2CEz78pjZOKZhv2IFVW1NokoXc=',NULL,0,'Stacey','Stephens',0,1,'austindavis','mreynolds@example.net','tenant','2025-10-15 09:40:42.691036','001-771-422-450'),(27,'pbkdf2_sha256$1000000$ISsAFesA39JQiDwJv10ZNb$yAN7L+aII7r6CD/3Ahc6B0lt+shjejxCv+U4YuRrq7M=',NULL,0,'Eugene','King',0,1,'william49','joann40@example.net','tenant','2025-10-15 09:40:42.823142','+1-309-218-5605'),(28,'pbkdf2_sha256$1000000$2G89zhjpKmdfbfZcwbfJs2$ACbjzFjgtsuVDqXNJYg75yPQAD4Krw/obTbl9Z4uB9s=',NULL,0,'James','Jimenez',0,1,'houseamber','gomezchelsea@example.org','tenant','2025-10-15 09:40:42.953482','(367)801-2293x7'),(29,'pbkdf2_sha256$1000000$5UHfzpol2uRKE0uH9YrAkO$U8qStAYqh9CWtVoQxIp6pVhKCpNweAkwuNnXBH4fg3I=',NULL,0,'Debbie','Compton',0,1,'proctordonna','michelle99@example.org','tenant','2025-10-15 09:40:43.082812','001-609-521-476'),(30,'pbkdf2_sha256$1000000$239jTPc7w6zj71IvML74JG$wyOO8w0jdOhTiY0lAc6din1VV/nM4hoSVmpqFGNTl78=',NULL,0,'Julie','Williams',0,1,'dshannon','emily18@example.net','tenant','2025-10-15 09:40:43.212767','617.570.5459x07'),(31,'pbkdf2_sha256$1000000$20MhBrm5ImJYh7mGf3Wqdm$iA6BxRhYQ2qOlCO67OsjWo4PsSdBl8dUyUmem8fe3zU=',NULL,0,'Brooke','Lowery',0,1,'gonzalezstephanie','annharris@example.org','tenant','2025-10-15 09:40:43.342738','+1-471-851-9912'),(32,'pbkdf2_sha256$1000000$jheokyjfKRTSsxqroXLx5a$uxcHmuHoPaEdAar7TKyBX4QHZCK2nuGs/XA9Fall75M=',NULL,0,'Christopher','Kim',0,1,'parkerstephen','melissalopez@example.com','tenant','2025-10-15 09:40:43.473156','001-978-967-810'),(33,'pbkdf2_sha256$1000000$hyjgfUE1Opk3DP61Vlh0cS$dowDYtZAWVRMq7URV64GpDLju8PLRNOLTHiEPNM0zS0=',NULL,0,'David','Walton',0,1,'ahunter','saraturner@example.org','tenant','2025-10-15 09:40:43.604222','(923)261-0383x6'),(34,'pbkdf2_sha256$1000000$MPtDgx19sJn7wZJsclTVTp$mm4HHCuNrTMjJ/p+PoYGBFNB8JxOyVK0tj1S5iydqA0=',NULL,0,'Thomas','Stuart',0,1,'cartercolin','gwoodard@example.net','tenant','2025-10-15 09:40:43.736665','+1-842-253-3139'),(35,'pbkdf2_sha256$1000000$GzJVR3iJcW2o9D0qPtxJuN$6fsNX15jqBl2w9uOnsBSXRJw4BDMe5aEC+OYyTKCSRU=',NULL,0,'Joseph','Dixon',0,1,'nicholas20','gregory67@example.com','tenant','2025-10-15 09:40:43.866077','(817)550-5353x7'),(36,'pbkdf2_sha256$1000000$Rcn6s01UKh1QaOTYCSaRJo$b7gK72B2O/VMMAHPMESD5cg7QizP6NjTazkeF/siSZo=',NULL,0,'Ruben','Brown',0,1,'turnerdiana','judith32@example.net','tenant','2025-10-15 09:40:43.998062','001-769-841-215'),(37,'pbkdf2_sha256$1000000$qKlEKZO8vzNKBcI0qtCIAp$nZJAxEO7zPVBwG1wVAKKyR+iSzegRBKrBxA2eUvgD4A=',NULL,0,'Jennifer','Torres',0,1,'kellymartinez','stephanie37@example.org','tenant','2025-10-15 09:40:44.126393','3029557671'),(38,'pbkdf2_sha256$1000000$L7YJqklBWxIWn4BVNiimaQ$skWsprvFQih67jz287/z+kfnv5lTs8PDYzsi9kZy7js=',NULL,0,'Julian','Zavala',0,1,'michaelwhite','joseph43@example.net','tenant','2025-10-15 09:40:44.257669','788-245-3868x54'),(39,'pbkdf2_sha256$1000000$iJMEiethJej55cHIL7iNbS$7kSi7ps4j203DXPyALfSR4efWhASfBuJWDgr4cCm29s=',NULL,0,'Logan','Wilkinson',0,1,'iansteele','mckenzietammy@example.net','tenant','2025-10-15 09:40:44.388876','978.639.9330'),(40,'pbkdf2_sha256$1000000$KPmLXL0Iry8qdmOvQjSsFw$Uv2wms84Y1im+skKToHTuDLJhzuoBOBOvBBK/MWnXAY=',NULL,0,'Margaret','Reeves',0,1,'stephen58','andrewkelley@example.net','tenant','2025-10-15 09:40:44.518754','001-952-943-258'),(41,'pbkdf2_sha256$1000000$PklX2TBpDjtT9PJVkkuEHu$2QDMTZ6c8KeKbpXDYATbut7WIrxQu4IK6f3d2jajH8A=',NULL,0,'Bruce','Vincent',0,1,'morriscorey','courtneyjones@example.org','tenant','2025-10-15 09:40:44.647736','(796)471-3009x5'),(42,'pbkdf2_sha256$1000000$pZW7ts7Lwhh1lg3lIX0Qdo$M0pW4iBzh+m0DJoZMfoy9z4hoYvfyICl7H0PQvCM9LE=',NULL,0,'Angela','Johnson',0,1,'cochranrobert','briananderson@example.org','tenant','2025-10-15 09:40:44.778691','001-243-701-242'),(43,'pbkdf2_sha256$1000000$tb9Xamc9YN5AVLRBHli0CF$uilY8MXPNRy7C7O726BqkYkoNhOPnUohAuKmO6lbs80=',NULL,0,'George','Dunn',0,1,'reesepatrick','farleytroy@example.com','tenant','2025-10-15 09:40:44.907899','+1-255-934-5861'),(44,'pbkdf2_sha256$1000000$A8VzoXbB8TGJ6bW7piip88$jkKOUQ3PZKNyNsEPn24JfVE43uBv2vRqxW1d/Y67vbE=',NULL,0,'Melissa','Moore',0,1,'karen51','huntgeorge@example.net','landlord','2025-10-15 09:40:45.039534','571.470.1250'),(45,'pbkdf2_sha256$1000000$zTvnmKi6nPEVPcZDYDtfYS$PCAepnFbZ9n9b8bhOeEvggkCy2MeCGfCiZmvBA/v1OQ=',NULL,0,'Elizabeth','Snyder',0,1,'richard54','nvargas@example.com','landlord','2025-10-15 09:40:45.169208','(587)297-5603x0'),(46,'pbkdf2_sha256$1000000$LNZWIVlUhS1IZ7ofjuS8GP$7JGMjVcQcInuxcr0s+92AydqW6hRCLwy3Df01Z3nJTI=',NULL,0,'Mark','Mccall',0,1,'richardsjonathan','hoffmandesiree@example.com','landlord','2025-10-15 09:40:45.299804','(340)312-8575x2'),(47,'pbkdf2_sha256$1000000$OFe8WzoZL1zMyy5oGP8w2O$r163GXE+chprkud2VNHOwAJCQu+unlmhyJZNo1nQLCo=',NULL,0,'Brooke','Foster',0,1,'halldeanna','stacy84@example.com','landlord','2025-10-15 09:40:45.428316','220-927-4597x50'),(48,'pbkdf2_sha256$1000000$rkzZyO89HVjbOwXM7z4rY4$J/gA+Owc0TRt/fE35LROknHZXoyxibE/3hXLt4rBKB4=',NULL,0,'Sierra','Craig',0,1,'russell51','aadams@example.org','landlord','2025-10-15 09:40:45.557794','898.507.7695'),(49,'pbkdf2_sha256$1000000$h34R3lSvglJiSDIEPqgVBz$vHCqAh2hRdnc8Aa4OC3gyRkziybigSQ4tRjKEbps1l0=',NULL,0,'Michael','Smith',0,1,'holly54','nicholas35@example.org','landlord','2025-10-15 09:40:45.688074','482-881-2048'),(50,'pbkdf2_sha256$1000000$is8ddE2euZPR5EuT3mXRVI$nBdwTgpzWnRcjbttXPMqLnebJD51q+QFqS/gT3n9yqQ=',NULL,0,'Christopher','Moore',0,1,'sandrasims','maria64@example.org','landlord','2025-10-15 09:40:45.816858','(623)818-4654'),(51,'pbkdf2_sha256$1000000$ShGYvBFSWwI3LToljhvoIH$v1RXyp3wZDEEurQ6TvNGLrOKFjJqCebCeIAMnBf1T50=',NULL,0,'Darlene','Myers',0,1,'morganhughes','vanessa07@example.org','landlord','2025-10-15 09:40:45.945889','001-744-370-511'),(52,'pbkdf2_sha256$1000000$sXuCij8hUxq4mZaUYkwicH$PEDE0WuGuEjRlX0pTOF9M+9yjKiBFrkwxYi2L4Ex9lM=',NULL,0,'Nicholas','Smith',0,1,'dyoung','rdavis@example.org','landlord','2025-10-15 09:40:46.077880','369-835-4993'),(53,'pbkdf2_sha256$1000000$nWyKZcQ6WzQMHg7EOTmRHT$7/vXVVcLYMvYuloEbb3oviW8dCNyCtbrY37V1m9zUAA=',NULL,0,'Elizabeth','Smith',0,1,'smithdaniel','ericdawson@example.com','landlord','2025-10-15 09:40:46.208483','001-839-751-707'),(54,'pbkdf2_sha256$1000000$I3ZQ8bysbCQyFTdtXbDcbE$PNaSaVlrPJBmEoudmwWlgtSupDZ8xHnDmpenovmy694=',NULL,0,'Alex','Allen',0,1,'nicholascarson','alejandrarose@example.net','landlord','2025-10-15 09:40:46.340868','(351)280-2715'),(55,'pbkdf2_sha256$1000000$tgmb3i52yuY8lnactF1mSN$eTJTGtWC11LUdljVPjzt4uVXhpFT1FKS77PfozP/Xb4=',NULL,0,'Brian','Martin',0,1,'qlloyd','cristianrodriguez@example.com','landlord','2025-10-15 09:40:46.470167','614-618-1808'),(56,'pbkdf2_sha256$1000000$iIVhYZT7pL3iEnvM01QPDx$DkuTXPEv91i5mBWkCTT4jqBRxOD21lxnIysgkkYjADY=',NULL,0,'David','Williams',0,1,'isaacrobertson','hannahsosa@example.com','landlord','2025-10-15 09:40:46.599299','001-899-562-467'),(57,'pbkdf2_sha256$1000000$D6utjpodJ3zRBGb7sIm7hi$52C/NBSVXw28vZROiQQBYUKsAXlX9Lw8Riq5W2zj7SE=',NULL,0,'Robert','Melendez',0,1,'sswanson','gabrielgray@example.net','landlord','2025-10-15 09:40:46.728737','847.826.1214x38'),(58,'pbkdf2_sha256$1000000$GQFCvmwvPnrmFU2QJe848p$DfXEMTD6Xl9qMiRRTt6eyml8LU+37VoSzsHuGMmDAC8=',NULL,0,'Tracie','Cunningham',0,1,'henryelizabeth','nortonkevin@example.net','landlord','2025-10-15 09:40:46.857619','692.741.9545'),(59,'pbkdf2_sha256$1000000$ziC27dASJQ4GuqT1pxe50I$Cq2ZkNAnA2cssYlXY66To/aMe03y8gGb7M0eDydeYak=',NULL,0,'Patrick','Arroyo',0,1,'ebaldwin','eguerra@example.com','landlord','2025-10-15 09:40:46.986687','(860)777-4568x7'),(60,'pbkdf2_sha256$1000000$7S1pAHk3ssR0cIJ2yjP4j8$webJvaBl7rkxePYtFrAtxL+kHUqj+rKeLpVvaZHuyvc=',NULL,0,'James','Ferguson',0,1,'jacksonmichael','ygrant@example.com','landlord','2025-10-15 09:40:47.118007','780.250.6592'),(61,'pbkdf2_sha256$1000000$hn9LR9f1I5AOJyEZyA1YzJ$JxaZd8L4MTmARxhn77OGGRSwBBaakZ7jaifH2dDFfDw=',NULL,0,'Brandon','Lee',0,1,'stacey69','vtorres@example.com','landlord','2025-10-15 09:40:47.248003','(548)247-1347'),(62,'pbkdf2_sha256$1000000$ABVtXSRNXZjcaITS2MktwP$xXTNz4MqQh+jk6uFko4o/6wkoFtb84NFjgV/W7uHiZs=',NULL,0,'Makayla','Richardson',0,1,'hillelizabeth','castillokathryn@example.net','landlord','2025-10-15 09:40:47.379127','631.624.9871x57'),(63,'pbkdf2_sha256$1000000$AGFNShr7ji6HYJdxIUNjam$XwlYXJ3j7vvW7diEPL9cfVR8EvOY+ikMX+Loko4b6Oc=',NULL,0,'Andrew','Knapp',0,1,'peterselizabeth','mariadaniels@example.net','landlord','2025-10-15 09:40:47.512189','001-561-934-232');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
INSERT INTO `users_user_groups` VALUES (5,2,2),(6,3,1),(7,4,1),(8,5,1),(9,6,1),(10,7,1),(11,8,1),(12,9,1),(13,10,1),(14,11,1),(15,12,1),(16,13,1),(17,14,1),(18,15,1),(19,16,1),(20,17,1),(21,18,1),(22,19,1),(23,20,1),(24,21,1),(25,22,1),(26,23,1),(27,24,1),(28,25,1),(29,26,1),(30,27,1),(31,28,1),(32,29,1),(33,30,1),(34,31,1),(35,32,1),(36,33,1),(37,34,1),(38,35,1),(39,36,1),(40,37,1),(41,38,1),(42,39,1),(43,40,1),(44,41,1),(45,42,1),(46,43,1),(47,44,2),(48,45,2),(49,46,2),(50,47,2),(51,48,2),(52,49,2),(53,50,2),(54,51,2),(55,52,2),(56,53,2),(57,54,2),(58,55,2),(59,56,2),(60,57,2),(61,58,2),(62,59,2),(63,60,2),(64,61,2),(65,62,2),(66,63,2);
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 12:24:03
