-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Окт 29 2025 г., 22:01
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

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `ads_review`
--
ALTER TABLE `ads_review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ads_review_listing_id_e23b0b6f_fk_ads_listing_id` (`listing_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `ads_review`
--
ALTER TABLE `ads_review`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ads_review`
--
ALTER TABLE `ads_review`
  ADD CONSTRAINT `ads_review_listing_id_e23b0b6f_fk_ads_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `ads_listing` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
