-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Окт 29 2025 г., 23:25
-- Версия сервера: 11.8.3-MariaDB-log
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `u392148004_rental`
--

-- --------------------------------------------------------

--
-- Структура таблицы `ads_booking`
--

CREATE TABLE `ads_booking` (
  `id` bigint(20) NOT NULL,
  `user_email` varchar(254) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `listing_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `ads_booking`
--

INSERT INTO `ads_booking` (`id`, `user_email`, `start_date`, `end_date`, `status`, `created_at`, `listing_id`) VALUES
(1, '', '2025-10-20', '2025-10-25', 'declined', '2025-10-10 08:00:00.000000', 1),
(2, 'newbusinessman@icloud.com', '2025-10-29', '2025-11-12', 'declined', '2025-10-28 14:19:04.657796', 3),
(3, 'moiaccde@gmail.com', '2025-10-29', '2025-10-31', 'approved', '2025-10-28 18:39:40.518122', 6),
(4, 'moiaccde@gmail.com', '2025-10-28', '2025-10-29', 'approved', '2025-10-28 22:35:47.808169', 6),
(5, 'moiaccde@gmail.com', '2025-11-02', '2025-11-06', 'declined', '2025-10-28 22:56:52.126569', 6),
(6, 'moiaccde@gmail.com', '2025-10-29', '2025-10-30', 'declined', '2025-10-28 23:39:13.421842', 6),
(7, 'moiaccde@gmail.com', '2025-10-31', '2025-11-03', 'approved', '2025-10-29 18:41:25.651274', 6),
(8, 'moiaccde@gmail.com', '2025-11-11', '2025-11-20', 'pending', '2025-10-29 18:48:56.430532', 6);

-- --------------------------------------------------------

--
-- Структура таблицы `ads_listing`
--

CREATE TABLE `ads_listing` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` longtext NOT NULL,
  `city` varchar(120) NOT NULL,
  `price_per_night` decimal(10,2) NOT NULL,
  `owner_email` varchar(254) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `ads_listing`
--

INSERT INTO `ads_listing` (`id`, `title`, `slug`, `description`, `city`, `price_per_night`, `owner_email`, `created_at`) VALUES
(1, 'Sunny apartment in Mainz', 'sunny-apartment-in-mainz', 'Close to river. Balcony, 2 rooms.', 'Mainz', 900.00, 'newbusinessman@icloud.com', '2025-01-01 12:00:00.000000'),
(2, 'Family house Wiesbaden', 'family-house-wiesbaden', 'Garden, garage, perfect for kids.', 'Wiesbaden', 1800.00, 'newbusinessman@icloud.com', '2025-01-02 12:00:00.000000'),
(3, 'Test Listing Frankfurt from user2', 'test-listing-frankfurt-from-user2', 'Description of the Test Listing Frankfurt from user2', 'Frankfurt', 300.00, 'newbusinessman@icloud.com', '2025-10-27 19:47:10.491689'),
(4, 'Test Wiesbaden', 'test-wiesbaden', 'Test Wiesbaden', 'Wiesbaden', 200.00, 'info@ironrider.de', '2025-10-28 07:49:56.935794'),
(5, 'Test Listing Mainz for Booking', 'test-listing-mainz-for-booking', 'Test Listing Mainz for Booking', 'Mainz', 50.00, 'newbusinessman@icloud.com', '2025-10-28 16:02:59.078743'),
(6, 'HelloListingtest10Host', 'hellolistingtest10host', 'HelloListingtest10Host', 'Frankfurt', 900.00, 'xhuman.alex@gmail.com', '2025-10-28 16:24:58.032203');

-- --------------------------------------------------------

--
-- Структура таблицы `ads_review`
--

CREATE TABLE `ads_review` (
  `id` bigint(20) NOT NULL,
  `user_email` varchar(254) NOT NULL,
  `rating` smallint(5) UNSIGNED NOT NULL CHECK (`rating` >= 0),
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `listing_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `ads_review`
--

INSERT INTO `ads_review` (`id`, `user_email`, `rating`, `comment`, `created_at`, `listing_id`) VALUES
(1, 'moiaccde@gmail.com', 5, 'Great place, clean and sunny!', '2025-10-11 12:00:00.000000', 1),
(2, 'moiaccde@gmail.com', 4, 'Nice garden, a bit far from center.', '2025-10-12 12:00:00.000000', 2),
(4, 'moiaccde@gmail.com', 5, 'Very good!', '2025-10-29 21:57:05.378377', 6);

-- --------------------------------------------------------

--
-- Структура таблицы `ads_viewhistory`
--

CREATE TABLE `ads_viewhistory` (
  `id` bigint(20) NOT NULL,
  `ip` char(39) DEFAULT NULL,
  `user_agent` varchar(512) NOT NULL,
  `viewed_at` datetime(6) NOT NULL,
  `listing_id` bigint(20) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `ads_viewhistory`
--

INSERT INTO `ads_viewhistory` (`id`, `ip`, `user_agent`, `viewed_at`, `listing_id`, `user_id`) VALUES
(1, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:41:58.759870', 4, NULL),
(2, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:42:02.715502', 4, NULL),
(3, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:43:52.862971', 4, NULL),
(4, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:49:52.270277', 4, NULL),
(5, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:50:25.663606', 4, NULL),
(6, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:51:42.064971', 4, NULL),
(7, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:53:31.126286', 4, NULL),
(8, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:54:03.784423', 4, NULL),
(9, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 13:59:37.350879', 4, 3),
(10, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 14:09:06.761712', 4, 3),
(11, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 14:09:10.405137', 3, 3),
(12, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 14:11:34.744443', 3, 3),
(13, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 14:17:27.628483', 3, 3),
(14, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 14:34:40.332854', 3, 3),
(15, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 15:01:45.116135', 3, 3),
(16, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 15:17:23.281095', 3, 3),
(17, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 16:24:58.682996', 6, 10),
(18, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 17:01:59.053343', 6, 10),
(19, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 17:07:40.794030', 6, 10),
(20, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 17:39:29.704826', 6, 11),
(21, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:27:24.081664', 6, 11),
(22, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:38:32.210853', 6, 11),
(23, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:39:16.316297', 6, 11),
(24, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:40:02.621008', 6, 11),
(25, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:41:19.281349', 6, 11),
(26, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:44:42.466925', 6, 11),
(27, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-28 18:46:10.374439', 6, 10),
(28, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-28 18:46:29.686405', 6, 10),
(29, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 18:57:53.288263', 6, 11),
(30, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:11:37.734720', 6, 11),
(31, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:15:52.411619', 6, 11),
(32, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:34:32.857309', 6, 11),
(33, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:34:46.118888', 6, 11),
(34, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:34:52.742591', 5, 11),
(35, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:35:02.983664', 6, 11),
(36, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:35:36.591996', 6, 11),
(37, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-28 22:35:55.986143', 6, 10),
(38, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:43:22.538774', 6, 11),
(39, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:43:29.832814', 6, 11),
(40, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:46:04.747020', 6, 11),
(41, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:46:35.149105', 6, 11),
(42, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:48:08.904826', 6, 11),
(43, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:48:18.980730', 5, 11),
(44, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:48:20.047950', 5, 11),
(45, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:53:58.587172', 6, 11),
(46, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:55:49.884336', 6, 11),
(47, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:56:41.636707', 6, 11),
(48, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 22:56:58.057098', 6, 11),
(49, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:04:15.188444', 6, 11),
(50, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:15:35.123204', 6, 11),
(51, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:16:48.522719', 4, 11),
(52, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:28:08.103420', 6, 11),
(53, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:34:39.112642', 6, 11),
(54, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:38:10.315347', 6, 11),
(55, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:39:05.171513', 6, 11),
(56, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-28 23:39:19.086532', 6, 11),
(57, '172.18.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 07:52:39.477979', 6, 11),
(58, '172.18.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 09:48:05.396898', 6, 11),
(59, '172.18.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 09:48:34.835079', 4, 11),
(60, '172.18.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 09:48:37.442939', 3, 11),
(61, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 14:59:50.675385', 6, 11),
(62, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 16:39:35.698119', 4, 11),
(63, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 16:53:11.903222', 6, 11),
(64, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:10:17.805492', 5, 11),
(65, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 17:10:56.830456', 4, 1),
(66, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:17:39.541806', 2, 11),
(67, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:18:17.136451', 6, 11),
(68, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:19:45.380230', 1, 11),
(69, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:19:50.441724', 2, 11),
(70, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:20:39.632785', 2, 11),
(71, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:22:23.167345', 2, 11),
(72, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:22:24.881541', 2, 11),
(73, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:22:29.535593', 1, 11),
(74, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:23:09.841538', 1, 11),
(75, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:33:21.305187', 1, 11),
(76, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 17:33:41.417778', 6, 11),
(77, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:16:17.417388', 2, 11),
(78, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:16:24.331342', 6, 11),
(79, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:16:42.520348', 6, 11),
(80, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:39:15.869631', 6, 11),
(81, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:39:28.391779', 2, 11),
(82, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:39:33.261839', 6, 11),
(83, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:41:07.800041', 6, 11),
(84, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:41:16.786714', 6, 11),
(85, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 18:41:51.937450', 6, 10),
(86, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:47:35.540845', 6, 11),
(87, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:48:48.628082', 6, 11),
(88, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:55:44.930326', 6, 11),
(89, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:55:49.861179', 6, 11),
(90, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 18:58:34.772739', 6, 11),
(91, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:37:14.366854', 6, 11),
(92, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 21:38:13.213568', 6, 10),
(93, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 21:38:16.730112', 2, 10),
(94, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:41:47.273036', 6, 11),
(95, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:43:00.265221', 6, 11),
(96, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 21:43:24.551300', 2, 10),
(97, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:45:03.028771', 6, 11),
(98, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:45:11.812626', 6, 11),
(99, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:45:28.083521', 6, 11),
(100, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-29 21:47:18.873499', 6, 10),
(101, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:52:22.133996', 6, 11),
(102, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:52:25.400284', 6, 11),
(103, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:52:28.932528', 6, 11),
(104, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:53:31.968452', 6, 11),
(105, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:53:43.115599', 6, 11),
(106, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:55:30.768201', 6, 11),
(107, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:55:36.966942', 6, 11),
(108, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:56:58.542027', 6, 11),
(109, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:57:05.996940', 6, 11),
(110, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 21:57:30.743130', 6, 11),
(111, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 23:02:50.757640', 6, 11),
(112, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15', '2025-10-29 23:06:26.220278', 6, 11);

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'Guest'),
(1, 'Host');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_permission`
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
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add listing', 7, 'add_listing'),
(26, 'Can change listing', 7, 'change_listing'),
(27, 'Can delete listing', 7, 'delete_listing'),
(28, 'Can view listing', 7, 'view_listing'),
(29, 'Can add booking', 8, 'add_booking'),
(30, 'Can change booking', 8, 'change_booking'),
(31, 'Can delete booking', 8, 'delete_booking'),
(32, 'Can view booking', 8, 'view_booking'),
(33, 'Can add review', 9, 'add_review'),
(34, 'Can change review', 9, 'change_review'),
(35, 'Can delete review', 9, 'delete_review'),
(36, 'Can view review', 9, 'view_review'),
(37, 'Can add view history', 10, 'add_viewhistory'),
(38, 'Can change view history', 10, 'change_viewhistory'),
(39, 'Can delete view history', 10, 'delete_viewhistory'),
(40, 'Can view view history', 10, 'view_viewhistory'),
(41, 'Can add profile', 11, 'add_profile'),
(42, 'Can change profile', 11, 'change_profile'),
(43, 'Can delete profile', 11, 'delete_profile'),
(44, 'Can view profile', 11, 'view_profile');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$AIfgNlvaCVXvUrBxLpwWDs$a2grvtmmwfihcbErEIzZsW2RXSPSyKuTm59IURdx62Q=', '2025-10-29 09:59:21.287059', 1, 'admin', '', '', 'info@ironrider.de', 1, 1, '2025-10-22 11:16:33.657880'),
(2, 'pbkdf2_sha256$720000$xYGt6KWlwHrbriG9CUEPyJ$2ABnf8C9FS6/7W8GnhfK7RWsSKX4K/f+ZzjzpV8z3RY=', NULL, 0, 'user1', '', '', '', 0, 1, '2025-10-22 11:32:59.797540'),
(3, 'pbkdf2_sha256$720000$dSfIgixYHv7SNAMjQXznV3$oDxqcP/VHpBVCTqrJr2ZzcywlvO0EEXkLnKlyUijNfA=', '2025-10-28 15:05:47.381143', 0, 'user2', 'Oleksandr', 'Kovalchuk', 'newbusinessman@icloud.com', 0, 1, '2025-10-22 12:09:05.000000'),
(4, 'pbkdf2_sha256$720000$Z6fGU9cJtnUOHoDRzWmgNy$/CVcCPtJpCI6RqRUdNl6vCGUIR+cf+3X4CblqRjqA/Q=', NULL, 0, 'user3', '', '', '', 0, 1, '2025-10-22 13:28:07.475256'),
(5, 'pbkdf2_sha256$720000$rMA7TnIYDdXOjQGqtmqzkC$qUC4RtmxfpYcEgfq6Cl+OhPSCJstgU9rxlqStsmekLM=', NULL, 0, 'user5', 'Test5', 'User5', 'xhumanalex@gmail.com', 0, 1, '2025-10-26 23:54:14.317767'),
(6, 'pbkdf2_sha256$720000$C59D6ODRGvSPumVSlTZOoL$idTtaw8FCt9sch6iutvBGIyq3QnKdiPtzKD7cLF0tTw=', NULL, 0, 'test06', 'Test06', 'Test06', 'test06@ironrider.de', 0, 1, '2025-10-27 00:05:49.950727'),
(7, 'pbkdf2_sha256$720000$OhPaYTK2dXMKqhSXkHB1iO$ZFojrIzLPnIRZxtOid1F7xhtYDnpVRP64eU8uqehXsQ=', '2025-10-27 00:15:52.529665', 0, 'test007', 'Test007', 'Test007', 'test007@ironrider.de', 0, 1, '2025-10-27 00:14:12.488814'),
(8, 'pbkdf2_sha256$720000$KUCsBQyWcRLiisrXdpMxoa$4QtS4Uh34Y2XLrHYSBNo0gSv1gty+6Hm/0B+n1VGdbY=', '2025-10-27 18:56:36.293898', 0, 'test08', 'Test08', 'Test08', 'x.humanalex@gmail.com', 0, 1, '2025-10-27 18:56:34.334990'),
(9, 'pbkdf2_sha256$720000$M78IW0Xp5c9YbSVqCTHGtt$bdPcKD+ki+y9ZQJMh1patJh4vriuxrOUHfW8d3YgO5c=', '2025-10-27 18:57:09.064942', 0, 'test09', 'test09', 'test09', 'xh.umanalex@gmail.com', 0, 1, '2025-10-27 18:57:07.012619'),
(10, 'pbkdf2_sha256$720000$rCyMZ0ekRwed34JtoF0lYQ$nvF5hjO3Aghya+qsfzUkZYYvUnd+2IVk5lUw5ZnMs5A=', '2025-10-29 18:20:02.878866', 0, 'testhost10', 'Olekandr', 'Kovalchuk', 'xhuman.alex@gmail.com', 0, 1, '2025-10-28 16:24:33.608268'),
(11, 'pbkdf2_sha256$720000$GKjg14Ion2qlGtx5cNgLUM$CErAbRVqewJUT0t7DLZMkq0Wc9GcYZGAhe8vPugIRvU=', '2025-10-29 07:48:33.325868', 0, 'TestGuest11', 'Anna', 'Yemelianova', 'moiaccde@gmail.com', 0, 1, '2025-10-28 17:08:47.159918');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 5, 2),
(2, 6, 2),
(4, 7, 1),
(3, 7, 2),
(6, 8, 1),
(5, 8, 2),
(7, 9, 2),
(10, 10, 1),
(9, 10, 2),
(11, 11, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(6, 3, 25),
(7, 3, 26),
(8, 3, 27),
(9, 3, 28),
(1, 3, 32),
(2, 3, 33),
(3, 3, 36),
(4, 3, 40),
(5, 3, 44);

-- --------------------------------------------------------

--
-- Структура таблицы `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-10-22 11:33:00.462449', '2', 'user1', 1, '[{\"added\": {}}]', 4, 1),
(2, '2025-10-22 12:09:06.368559', '3', 'user2', 1, '[{\"added\": {}}]', 4, 1),
(3, '2025-10-22 12:14:36.016800', '3', 'user2', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"User permissions\", \"Last login\"]}}]', 4, 1),
(4, '2025-10-22 12:15:07.192232', '3', 'user2', 2, '[]', 4, 1),
(5, '2025-10-22 13:28:08.301242', '4', 'user3', 1, '[{\"added\": {}}]', 4, 1),
(6, '2025-10-26 23:52:24.160088', '2', 'Family house Wiesbaden', 2, '[]', 7, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(8, 'ads', 'booking'),
(7, 'ads', 'listing'),
(9, 'ads', 'review'),
(10, 'ads', 'viewhistory'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(11, 'users', 'profile');

-- --------------------------------------------------------

--
-- Структура таблицы `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-10-20 12:34:09.028978'),
(2, 'auth', '0001_initial', '2025-10-20 12:34:10.474248'),
(3, 'admin', '0001_initial', '2025-10-20 12:34:10.795509'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-10-20 12:34:10.848575'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-20 12:34:10.901487'),
(6, 'ads', '0001_initial', '2025-10-20 12:34:11.636360'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-10-20 12:34:11.946755'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-10-20 12:34:12.063900'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-10-20 12:34:12.167036'),
(10, 'auth', '0004_alter_user_username_opts', '2025-10-20 12:34:12.219807'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-10-20 12:34:12.326164'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-10-20 12:34:12.373315'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-10-20 12:34:12.427374'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-10-20 12:34:12.533453'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-10-20 12:34:12.642491'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-10-20 12:34:12.753651'),
(17, 'auth', '0011_update_proxy_permissions', '2025-10-20 12:34:12.948786'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-10-20 12:34:13.069943'),
(19, 'sessions', '0001_initial', '2025-10-20 12:34:13.266082'),
(20, 'users', '0001_initial', '2025-10-22 12:04:22.334532'),
(21, 'users', '0002_create_host_guest_groups', '2025-10-26 23:10:38.518071'),
(22, 'users', '0003_alter_profile_role', '2025-10-26 23:10:38.573856');

-- --------------------------------------------------------

--
-- Структура таблицы `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('7gw5ivq6e6xnr5nmocciqrokqrvpsm5s', '.eJxVjEEOwiAQRe_C2hDoQMu4dO8ZyMAMtmpoUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZdXpd0uUH1J3wHeqt1nnua7LlPSu6IM2fZ1ZnpfD_TsYqY3fGl3uKWRnOxisgWLAEjrGhFBoyChivARA9NKVwn0AZiBLxnPhrmT1_gDT-jg7:1vE0zl:H8PAKG_6HoD3WqyU05PHGXwNPg9xcN1hKROP_ASx_YI', '2025-11-12 07:53:25.920958'),
('a160otp37gbh1reprtv5ydprxunbcnhi', '.eJxVjEsOwjAMBe-SNYoStw4JS_Y9Q2Q7LimgVupnhbg7VOoCtm9m3stk2taat0XnPBRzMd6Z0-_IJA8dd1LuNN4mK9O4zgPbXbEHXWw3FX1eD_fvoNJSvzVze3Y9ABAHDcihiBcXWBt0kqChJmLbY4qQUDwjuKjakk-CCIF78_4AA0U3xg:1vEAmB:zmEsQZPlApsW_TIPk9UVI39t1BUfBbDd2W0SgE98yE8', '2025-11-12 18:20:03.014482'),
('xepyavah9sz2n4x768trru0cdn3j5bx1', '.eJxVjEEOwiAQRe_C2pChhcC4dO8ZyMCAVA0kpV013t026UK3773_N-FpXYpfe5r9xOIqlBKXXxgovlI9DD-pPpqMrS7zFOSRyNN2eW-c3rez_Tso1Mu-BkRLGYGHTGp0MRoXLFqNpJzlAMowKz3CTnBImo2jzMHZhATAVovPF_f2N7k:1vE0v3:HjlgKmZRejuYl9rdDqYIfdrdW0Ep8cMvWmksejswkw0', '2025-11-12 07:48:33.464489');

-- --------------------------------------------------------

--
-- Структура таблицы `users_profile`
--

CREATE TABLE `users_profile` (
  `id` bigint(20) NOT NULL,
  `role` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users_profile`
--

INSERT INTO `users_profile` (`id`, `role`, `user_id`) VALUES
(1, 'guest', 3),
(2, 'guest', 4),
(3, 'guest', 5),
(5, 'guest', 6),
(7, 'guest', 7),
(8, 'guest', 8),
(9, 'guest', 9),
(10, 'guest', 10),
(11, 'guest', 11);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `ads_booking`
--
ALTER TABLE `ads_booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ads_booking_listing_id_9eb110c6_fk_ads_listing_id` (`listing_id`);

--
-- Индексы таблицы `ads_listing`
--
ALTER TABLE `ads_listing`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ads_listing_city_72a0b485` (`city`);

--
-- Индексы таблицы `ads_review`
--
ALTER TABLE `ads_review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ads_review_listing_id_e23b0b6f_fk_ads_listing_id` (`listing_id`);

--
-- Индексы таблицы `ads_viewhistory`
--
ALTER TABLE `ads_viewhistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ads_viewhistory_listing_id_5872dd92_fk_ads_listing_id` (`listing_id`),
  ADD KEY `ads_viewhistory_user_fk` (`user_id`);

--
-- Индексы таблицы `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индексы таблицы `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индексы таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индексы таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индексы таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Индексы таблицы `users_profile`
--
ALTER TABLE `users_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `ads_booking`
--
ALTER TABLE `ads_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `ads_listing`
--
ALTER TABLE `ads_listing`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `ads_review`
--
ALTER TABLE `ads_review`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `ads_viewhistory`
--
ALTER TABLE `ads_viewhistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT для таблицы `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT для таблицы `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT для таблицы `users_profile`
--
ALTER TABLE `users_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ads_booking`
--
ALTER TABLE `ads_booking`
  ADD CONSTRAINT `ads_booking_listing_id_9eb110c6_fk_ads_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `ads_listing` (`id`);

--
-- Ограничения внешнего ключа таблицы `ads_review`
--
ALTER TABLE `ads_review`
  ADD CONSTRAINT `ads_review_listing_id_e23b0b6f_fk_ads_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `ads_listing` (`id`);

--
-- Ограничения внешнего ключа таблицы `ads_viewhistory`
--
ALTER TABLE `ads_viewhistory`
  ADD CONSTRAINT `ads_viewhistory_listing_id_5872dd92_fk_ads_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `ads_listing` (`id`),
  ADD CONSTRAINT `ads_viewhistory_user_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `users_profile`
--
ALTER TABLE `users_profile`
  ADD CONSTRAINT `users_profile_user_id_2112e78d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
