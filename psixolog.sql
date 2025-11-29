-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 29, 2025 at 02:52 PM
-- Server version: 8.0.42
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `psixolog`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_application`
--

CREATE TABLE `app_application` (
  `id` bigint NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `psychologist_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_consultation`
--

CREATE TABLE `app_consultation` (
  `id` bigint NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `application_id` bigint NOT NULL,
  `psychologist_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_feedbackform`
--

CREATE TABLE `app_feedbackform` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `processed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_meeting`
--

CREATE TABLE `app_meeting` (
  `id` bigint NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `psychologist_id` bigint NOT NULL,
  `student_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_user`
--

CREATE TABLE `app_user` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `app_user`
--

INSERT INTO `app_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone`, `created_at`) VALUES
(1, 'pbkdf2_sha256$1000000$f4kDAMGNsatPMfMykOQNsj$KZ69mu4Rfx7FjONZu9kFf7qegU98FMnsQGJQhDf3Ub4=', '2025-11-29 14:10:49.531269', 0, 'dima', 'Дмитрий', 'Фильченков', 'dima@gmail.com', 0, 1, '2025-11-29 11:41:59.906887', 'psychologist', NULL, '2025-11-29 11:42:00.858401'),
(2, 'pbkdf2_sha256$1000000$OntRZ1u7l2ELC8SWF3YvU8$K1YR+eBM4qQ1ZZWPZhOv7F5wbltNv9b8s5lXJAevOMw=', '2025-11-29 14:37:19.491559', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-11-29 13:19:26.389870', 'user', NULL, '2025-11-29 13:19:27.105056'),
(3, 'pbkdf2_sha256$1000000$qfLQWzd4b19JdG6QAaLn6F$l0o4v57FqBwL7i+lF5tAx0HHxfKYXtSnT0gfbiaXows=', '2025-11-29 14:02:04.903950', 0, 'nastya', '', '', 'nastya@gmail.com', 0, 1, '2025-11-29 13:23:38.160770', 'user', NULL, '2025-11-29 13:23:38.956446');

-- --------------------------------------------------------

--
-- Table structure for table `app_user_groups`
--

CREATE TABLE `app_user_groups` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `app_user_user_permissions`
--

CREATE TABLE `app_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Пользователь', 6, 'add_user'),
(22, 'Can change Пользователь', 6, 'change_user'),
(23, 'Can delete Пользователь', 6, 'delete_user'),
(24, 'Can view Пользователь', 6, 'view_user'),
(25, 'Can add Заявка', 7, 'add_application'),
(26, 'Can change Заявка', 7, 'change_application'),
(27, 'Can delete Заявка', 7, 'delete_application'),
(28, 'Can view Заявка', 7, 'view_application'),
(29, 'Can add Консультация', 8, 'add_consultation'),
(30, 'Can change Консультация', 8, 'change_consultation'),
(31, 'Can delete Консультация', 8, 'delete_consultation'),
(32, 'Can view Консультация', 8, 'view_consultation'),
(33, 'Can add Обратная связь', 9, 'add_feedbackform'),
(34, 'Can change Обратная связь', 9, 'change_feedbackform'),
(35, 'Can delete Обратная связь', 9, 'delete_feedbackform'),
(36, 'Can view Обратная связь', 9, 'view_feedbackform'),
(37, 'Can add Встреча', 10, 'add_meeting'),
(38, 'Can change Встреча', 10, 'change_meeting'),
(39, 'Can delete Встреча', 10, 'delete_meeting'),
(40, 'Can view Встреча', 10, 'view_meeting');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(7, 'app', 'application'),
(8, 'app', 'consultation'),
(9, 'app', 'feedbackform'),
(10, 'app', 'meeting'),
(6, 'app', 'user'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-29 09:47:58.638524'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-11-29 09:47:58.749832'),
(3, 'auth', '0001_initial', '2025-11-29 09:47:59.072821'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-11-29 09:47:59.165375'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-11-29 09:47:59.172792'),
(6, 'auth', '0004_alter_user_username_opts', '2025-11-29 09:47:59.180015'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-11-29 09:47:59.186349'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-11-29 09:47:59.189368'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-11-29 09:47:59.196931'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-11-29 09:47:59.204882'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-11-29 09:47:59.212155'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-11-29 09:47:59.286216'),
(13, 'auth', '0011_update_proxy_permissions', '2025-11-29 09:47:59.293016'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-11-29 09:47:59.298699'),
(15, 'app', '0001_initial', '2025-11-29 09:47:59.720784'),
(16, 'admin', '0001_initial', '2025-11-29 09:47:59.900017'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-11-29 09:47:59.907562'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-29 09:47:59.917811'),
(19, 'sessions', '0001_initial', '2025-11-29 09:47:59.960880'),
(20, 'app', '0002_application', '2025-11-29 09:50:12.138460'),
(21, 'app', '0003_consultation', '2025-11-29 09:50:51.592908'),
(22, 'app', '0004_feedbackform', '2025-11-29 11:22:18.723246'),
(23, 'app', '0005_meeting', '2025-11-29 13:48:07.346140');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('al8oaw6du94llzai9ifuhwe1xmrfviuy', '.eJxVjEEOwiAQRe_C2pABBFqX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERWpx-t4j0SHUHfMd6a5JaXZc5yl2RB-1yapye18P9OyjYy7e2xsfEBEO2avSoM4Dl7IkTY1YKAEcH5D3RGTREld1gDGdwrIhMRPH-APUcOHI:1vPM4d:DnBvMgKGkLLH7qw1YJDDekpQIqWYEvLVs8UrXMnon6g', '2025-12-13 14:37:19.493316'),
('q4dlp3agrvkzji5ek5ogfo67qwmt4ui3', '.eJxVjMsOwiAQRf-FtSE8BhCX7vsNZGBQqgaS0q6M_y5NutDtOefeNwu4rSVsPS9hJnZhkp1-WcT0zHUX9MB6bzy1ui5z5HvCD9v51Ci_rkf7d1Cwl7HWwmrwt4xn0kZksGCckBLIGlIyqZgAQaURqWy1l0qhjHpQ4zU4cuzzBbUdNps:1vPLc2:5SsYyilr7x7iSt2pZVhAgc3STyyGy5E6tX278zqtaSI', '2025-12-13 14:07:46.702376'),
('y0c6jlewvmkiqar0bhzxtq7ykrc0dt8m', '.eJxVjMsOwiAQRf-FtSE8BhCX7vsNZGBQqgaS0q6M_y5NutDtOefeNwu4rSVsPS9hJnZhkp1-WcT0zHUX9MB6bzy1ui5z5HvCD9v51Ci_rkf7d1Cwl7HWwmrwt4xn0kZksGCckBLIGlIyqZgAQaURqWy1l0qhjHpQ4zU4cuzzBbUdNps:1vPLMH:cvOheDOYJOf-Lx1pLoM-FFWWZ4e-ApSnzT4zoipv3hE', '2025-12-13 13:51:29.539376');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_application`
--
ALTER TABLE `app_application`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_application_psychologist_id_6174932c_fk_app_user_id` (`psychologist_id`),
  ADD KEY `app_application_user_id_478e5788_fk_app_user_id` (`user_id`);

--
-- Indexes for table `app_consultation`
--
ALTER TABLE `app_consultation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_consultation_application_id_58002f68_fk_app_application_id` (`application_id`),
  ADD KEY `app_consultation_psychologist_id_42748d99_fk_app_user_id` (`psychologist_id`);

--
-- Indexes for table `app_feedbackform`
--
ALTER TABLE `app_feedbackform`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_meeting`
--
ALTER TABLE `app_meeting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_meeting_application_id_94cc5346_fk_app_application_id` (`application_id`),
  ADD KEY `app_meeting_psychologist_id_bc772910_fk_app_user_id` (`psychologist_id`),
  ADD KEY `app_meeting_student_id_1ecceb80_fk_app_user_id` (`student_id`);

--
-- Indexes for table `app_user`
--
ALTER TABLE `app_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_user_groups_user_id_group_id_73b8e940_uniq` (`user_id`,`group_id`),
  ADD KEY `app_user_groups_group_id_e774d92c_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_user_user_permissions_user_id_permission_id_7c8316ce_uniq` (`user_id`,`permission_id`),
  ADD KEY `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_app_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_application`
--
ALTER TABLE `app_application`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `app_consultation`
--
ALTER TABLE `app_consultation`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `app_feedbackform`
--
ALTER TABLE `app_feedbackform`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `app_meeting`
--
ALTER TABLE `app_meeting`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `app_user`
--
ALTER TABLE `app_user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `app_application`
--
ALTER TABLE `app_application`
  ADD CONSTRAINT `app_application_psychologist_id_6174932c_fk_app_user_id` FOREIGN KEY (`psychologist_id`) REFERENCES `app_user` (`id`),
  ADD CONSTRAINT `app_application_user_id_478e5788_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_consultation`
--
ALTER TABLE `app_consultation`
  ADD CONSTRAINT `app_consultation_application_id_58002f68_fk_app_application_id` FOREIGN KEY (`application_id`) REFERENCES `app_application` (`id`),
  ADD CONSTRAINT `app_consultation_psychologist_id_42748d99_fk_app_user_id` FOREIGN KEY (`psychologist_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_meeting`
--
ALTER TABLE `app_meeting`
  ADD CONSTRAINT `app_meeting_application_id_94cc5346_fk_app_application_id` FOREIGN KEY (`application_id`) REFERENCES `app_application` (`id`),
  ADD CONSTRAINT `app_meeting_psychologist_id_bc772910_fk_app_user_id` FOREIGN KEY (`psychologist_id`) REFERENCES `app_user` (`id`),
  ADD CONSTRAINT `app_meeting_student_id_1ecceb80_fk_app_user_id` FOREIGN KEY (`student_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_user_groups`
--
ALTER TABLE `app_user_groups`
  ADD CONSTRAINT `app_user_groups_group_id_e774d92c_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `app_user_groups_user_id_e6f878f6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `app_user_user_permissions`
--
ALTER TABLE `app_user_user_permissions`
  ADD CONSTRAINT `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `app_user_user_permissions_user_id_24780b52_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
