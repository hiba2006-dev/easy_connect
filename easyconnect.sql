-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 16 mars 2026 à 15:55
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `easyconnect`
--

-- --------------------------------------------------------

--
-- Structure de la table `activity_history`
--

CREATE TABLE `activity_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `activity_type` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `activity_type` varchar(64) NOT NULL,
  `detail` text NOT NULL,
  `meta_info` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `user_id`, `activity_type`, `detail`, `meta_info`, `created_at`) VALUES
(1, 11, 'course_start', 'Début du cours \"Alphabet ASL\"', '{\"course_id\": 1}', '2026-03-12 00:27:16'),
(2, 11, 'course_item', 'Complété objective_1 dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"objective_1\"}', '2026-03-12 00:27:17'),
(3, 11, 'course_item', 'Complété objective_2 dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"objective_2\"}', '2026-03-12 00:27:20'),
(4, 11, 'course_item', 'Complété objective_3 dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"objective_3\"}', '2026-03-12 00:27:21'),
(5, 11, 'course_item', 'Complété alphabet_A dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_A\"}', '2026-03-12 00:27:22'),
(6, 11, 'course_item', 'Complété alphabet_B dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_B\"}', '2026-03-12 00:27:26'),
(7, 11, 'course_item', 'Complété alphabet_C dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_C\"}', '2026-03-12 00:27:28'),
(8, 11, 'course_item', 'Complété alphabet_D dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_D\"}', '2026-03-12 00:27:29'),
(9, 11, 'course_item', 'Complété alphabet_E dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_E\"}', '2026-03-12 00:27:30'),
(10, 11, 'course_item', 'Complété alphabet_F dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_F\"}', '2026-03-12 00:27:30'),
(11, 11, 'course_item', 'Complété alphabet_G dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_G\"}', '2026-03-12 00:27:31'),
(12, 11, 'course_item', 'Complété alphabet_H dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_H\"}', '2026-03-12 00:27:32'),
(13, 11, 'course_item', 'Complété alphabet_I dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_I\"}', '2026-03-12 00:27:33'),
(14, 11, 'course_item', 'Complété alphabet_J dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_J\"}', '2026-03-12 00:27:34'),
(15, 11, 'course_item', 'Complété alphabet_K dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_K\"}', '2026-03-12 00:27:36'),
(16, 11, 'course_item', 'Complété alphabet_L dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_L\"}', '2026-03-12 00:27:36'),
(17, 11, 'course_item', 'Complété alphabet_M dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_M\"}', '2026-03-12 00:27:37'),
(18, 11, 'course_item', 'Complété alphabet_N dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_N\"}', '2026-03-12 00:27:38'),
(19, 11, 'course_item', 'Complété alphabet_O dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_O\"}', '2026-03-12 00:27:38'),
(20, 11, 'course_item', 'Complété alphabet_P dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_P\"}', '2026-03-12 00:27:39'),
(21, 11, 'course_item', 'Complété alphabet_Q dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_Q\"}', '2026-03-12 00:27:40'),
(22, 11, 'course_item', 'Complété alphabet_R dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_R\"}', '2026-03-12 00:27:41'),
(23, 11, 'course_item', 'Complété alphabet_S dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_S\"}', '2026-03-12 00:27:42'),
(24, 11, 'course_item', 'Complété alphabet_T dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_T\"}', '2026-03-12 00:27:43'),
(25, 11, 'course_item', 'Complété alphabet_U dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_U\"}', '2026-03-12 00:27:43'),
(26, 11, 'course_item', 'Complété alphabet_V dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_V\"}', '2026-03-12 00:27:44'),
(27, 11, 'course_item', 'Complété alphabet_W dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_W\"}', '2026-03-12 00:27:45'),
(28, 11, 'course_item', 'Complété alphabet_X dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_X\"}', '2026-03-12 00:27:46'),
(29, 11, 'course_item', 'Complété alphabet_Y dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_Y\"}', '2026-03-12 00:27:47'),
(30, 11, 'course_item', 'Complété alphabet_Z dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"alphabet_Z\"}', '2026-03-12 00:27:48'),
(31, 11, 'course_item', 'Complété video_1 dans \"Alphabet ASL\"', '{\"course_id\": 1, \"item_id\": \"video_1\"}', '2026-03-12 00:27:49'),
(32, 11, 'quiz_completion', 'Quiz terminé 14/20 (70%)', '{\"score\": 14, \"total\": 20, \"percent\": 70}', '2026-03-14 01:55:25'),
(33, 11, 'quiz_completion', 'Quiz terminé 12/20 (60%)', '{\"score\": 12, \"total\": 20, \"percent\": 60}', '2026-03-14 02:17:04'),
(34, 11, 'quiz_completion', 'Quiz terminé 7/20 (35%)', '{\"score\": 7, \"total\": 20, \"percent\": 35}', '2026-03-14 03:04:20'),
(35, 11, 'course_start', 'Started course \"Salutations ASL\"', '{\"course_id\": 2}', '2026-03-14 22:53:41'),
(36, 11, 'course_item', 'Completed objective_1 in \"Salutations ASL\"', '{\"course_id\": 2, \"item_id\": \"objective_1\"}', '2026-03-14 22:53:41'),
(37, 11, 'course_item', 'Completed objective_2 in \"Salutations ASL\"', '{\"course_id\": 2, \"item_id\": \"objective_2\"}', '2026-03-14 22:54:06'),
(38, 11, 'course_item', 'Completed objective_3 in \"Salutations ASL\"', '{\"course_id\": 2, \"item_id\": \"objective_3\"}', '2026-03-14 22:54:07'),
(39, 11, 'course_item', 'Completed vocab_hello in \"Salutations ASL\"', '{\"course_id\": 2, \"item_id\": \"vocab_hello\"}', '2026-03-14 22:54:08'),
(40, 11, 'course_start', 'Started course \"Daily Conversation\"', '{\"course_id\": 3}', '2026-03-14 23:00:20'),
(41, 11, 'course_item', 'Completed objective_1 in \"Daily Conversation\"', '{\"course_id\": 3, \"item_id\": \"objective_1\"}', '2026-03-14 23:00:20'),
(42, 11, 'course_item', 'Completed objective_2 in \"Daily Conversation\"', '{\"course_id\": 3, \"item_id\": \"objective_2\"}', '2026-03-14 23:00:42'),
(43, 11, 'course_item', 'Completed objective_3 in \"Daily Conversation\"', '{\"course_id\": 3, \"item_id\": \"objective_3\"}', '2026-03-14 23:00:43'),
(44, 11, 'course_item', 'Completed daily_hungry in \"Daily Conversation\"', '{\"course_id\": 3, \"item_id\": \"daily_hungry\"}', '2026-03-14 23:00:44');

-- --------------------------------------------------------

--
-- Structure de la table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `content` text DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `comments`
--

INSERT INTO `comments` (`id`, `content`, `author_id`, `post_id`, `created_at`) VALUES
(1, 'hhhh', 4, 1, '2026-02-22 20:19:30'),
(2, 'Great consistency. Morning practice works best for me too.', 8, 2, '2026-03-09 23:56:55'),
(3, 'Same here. I also repeat signs in front of a mirror.', 9, 2, '2026-03-09 23:56:55'),
(4, 'Flashcards + short daily review helped me a lot.', 7, 3, '2026-03-09 23:56:55'),
(5, 'Try grouping signs by context (greetings, food, actions).', 9, 3, '2026-03-09 23:56:55'),
(6, 'Nice progress! Keep going.', 7, 4, '2026-03-09 23:56:55'),
(7, 'Great score. Next target 90%!', 8, 4, '2026-03-09 23:56:55'),
(8, 'PAK', 6, 1, '2026-03-10 00:03:36');

-- --------------------------------------------------------

--
-- Structure de la table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `courses`
--

INSERT INTO `courses` (`id`, `title`, `description`, `video_url`) VALUES
(1, 'Alphabet ASL', 'Learn the ASL fingerspelling alphabet.', 'https://www.youtube.com/embed/nHtF3bR5Dq4'),
(2, 'Salutations ASL', 'Essential signs to greet and introduce yourself.', 'https://www.youtube.com/embed/0FcwzMq4iWg'),
(3, 'Daily Conversation', 'Express common daily needs in ASL.', 'https://www.youtube.com/embed/6_gXiBe9y9A');

-- --------------------------------------------------------

--
-- Structure de la table `learning_item_progress`
--

CREATE TABLE `learning_item_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` varchar(100) NOT NULL,
  `item_id` varchar(200) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `learning_item_progress`
--

INSERT INTO `learning_item_progress` (`id`, `user_id`, `course_id`, `item_id`, `completed`, `updated_at`) VALUES
(1, 6, '1', 'objective_1', 1, NULL),
(2, 6, '1', 'objective_2', 1, NULL),
(3, 6, '1', 'objective_3', 1, NULL),
(4, 6, '1', 'lesson_1', 1, NULL),
(5, 6, '1', 'lesson_2', 1, NULL),
(6, 6, '1', 'lesson_3', 1, NULL),
(7, 6, '1', 'practice_1', 1, NULL),
(8, 6, '1', 'practice_2', 1, NULL),
(9, 6, '1', 'practice_3', 1, NULL),
(10, 6, '1', 'alphabet_A', 1, NULL),
(11, 6, '1', 'alphabet_B', 1, NULL),
(12, 6, '1', 'alphabet_C', 1, NULL),
(13, 6, '1', 'alphabet_D', 1, NULL),
(14, 6, '1', 'alphabet_E', 1, NULL),
(15, 6, '2', 'objective_1', 1, NULL),
(16, 6, '2', 'objective_2', 1, NULL),
(17, 6, '2', 'objective_3', 1, NULL),
(18, 6, '2', 'lesson_1', 1, NULL),
(19, 6, '2', 'lesson_2', 1, NULL),
(20, 6, '2', 'lesson_3', 1, NULL),
(21, 6, '2', 'practice_1', 1, NULL),
(22, 6, '2', 'practice_2', 1, NULL),
(23, 6, '2', 'practice_3', 1, NULL),
(24, 6, '2', 'vocab_hello', 1, NULL),
(25, 6, '2', 'vocab_goodbye', 1, NULL),
(26, 6, '2', 'vocab_nice_to_meet_you', 1, NULL),
(27, 6, '2', 'vocab_whats_your_name', 1, NULL),
(28, 6, '2', 'vocab_my_name_is', 1, NULL),
(29, 6, '2', 'vocab_how_are_you', 1, NULL),
(30, 6, '2', 'vocab_im_fine', 1, NULL),
(31, 6, '2', 'vocab_thank_you', 1, NULL),
(32, 6, '2', 'vocab_please', 1, NULL),
(33, 6, '2', 'dialogue_1', 1, NULL),
(34, 6, '2', 'dialogue_2', 1, NULL),
(35, 6, '2', 'dialogue_3', 1, NULL),
(36, 6, '2', 'dialogue_4', 1, NULL),
(37, 6, '2', 'dialogue_5', 1, NULL),
(38, 6, '2', 'video_1', 1, NULL),
(39, 6, '3', 'objective_1', 1, NULL),
(40, 6, '3', 'objective_2', 1, NULL),
(41, 6, '3', 'objective_3', 1, NULL),
(42, 6, '3', 'lesson_1', 1, NULL),
(43, 6, '3', 'lesson_2', 1, NULL),
(44, 6, '3', 'lesson_3', 1, NULL),
(45, 6, '3', 'practice_1', 1, NULL),
(46, 6, '3', 'practice_2', 1, NULL),
(47, 6, '3', 'practice_3', 1, NULL),
(48, 6, '3', 'daily_hungry', 1, NULL),
(49, 11, '1', 'objective_1', 1, NULL),
(50, 11, '1', 'objective_2', 1, NULL),
(51, 11, '1', 'objective_3', 1, NULL),
(52, 11, '1', 'alphabet_A', 1, NULL),
(53, 11, '1', 'alphabet_B', 1, NULL),
(54, 11, '1', 'alphabet_C', 1, NULL),
(55, 11, '1', 'alphabet_D', 1, NULL),
(56, 11, '1', 'alphabet_E', 1, NULL),
(57, 11, '1', 'alphabet_F', 1, NULL),
(58, 11, '1', 'alphabet_G', 1, NULL),
(59, 11, '1', 'alphabet_H', 1, NULL),
(60, 11, '1', 'alphabet_I', 1, NULL),
(61, 11, '1', 'alphabet_J', 1, NULL),
(62, 11, '1', 'alphabet_K', 1, NULL),
(63, 11, '1', 'alphabet_L', 1, NULL),
(64, 11, '1', 'alphabet_M', 1, NULL),
(65, 11, '1', 'alphabet_N', 1, NULL),
(66, 11, '1', 'alphabet_O', 1, NULL),
(67, 11, '1', 'alphabet_P', 1, NULL),
(68, 11, '1', 'alphabet_Q', 1, NULL),
(69, 11, '1', 'alphabet_R', 1, NULL),
(70, 11, '1', 'alphabet_S', 1, NULL),
(71, 11, '1', 'alphabet_T', 1, NULL),
(72, 11, '1', 'alphabet_U', 1, NULL),
(73, 11, '1', 'alphabet_V', 1, NULL),
(74, 11, '1', 'alphabet_W', 1, NULL),
(75, 11, '1', 'alphabet_X', 1, NULL),
(76, 11, '1', 'alphabet_Y', 1, NULL),
(77, 11, '1', 'alphabet_Z', 1, NULL),
(78, 11, '1', 'video_1', 1, NULL),
(79, 11, '2', 'objective_1', 1, NULL),
(80, 11, '2', 'objective_2', 1, NULL),
(81, 11, '2', 'objective_3', 1, NULL),
(82, 11, '2', 'vocab_hello', 1, NULL),
(83, 11, '3', 'objective_1', 1, NULL),
(84, 11, '3', 'objective_2', 1, NULL),
(85, 11, '3', 'objective_3', 1, NULL),
(86, 11, '3', 'daily_hungry', 1, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `learning_progress`
--

CREATE TABLE `learning_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `course_id` varchar(100) DEFAULT NULL,
  `progress` int(11) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `learning_progress`
--

INSERT INTO `learning_progress` (`id`, `user_id`, `course_id`, `progress`, `completed`, `last_accessed`) VALUES
(1, 4, 'python1', 0, 0, NULL),
(2, 4, 'web1', 0, 0, NULL),
(3, 4, 'asl_alpha', 0, 0, NULL),
(4, 4, 'asl_greetings', 0, 0, NULL),
(5, 6, 'asl_greetings', 0, 0, NULL),
(6, 6, 'asl_alpha', 0, 0, NULL),
(7, 6, 'asl_daily', 0, 0, NULL),
(8, 6, '1', 38, 0, '2026-03-10 00:15:43'),
(9, 6, '2', 100, 1, '2026-03-10 01:19:36'),
(10, 6, '3', 27, 0, '2026-03-10 01:54:59'),
(11, 11, '1', 100, 1, '2026-03-14 22:53:30'),
(12, 11, '2', 30, 0, '2026-03-14 22:54:08'),
(13, 11, '3', 17, 0, '2026-03-14 23:00:44');

-- --------------------------------------------------------

--
-- Structure de la table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `is_anonymous` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `title` varchar(255) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `image_url` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `content`, `is_anonymous`, `created_at`, `title`, `author_id`, `updated_at`, `image_url`) VALUES
(1, NULL, 'iojhbbk', 0, '2026-02-22 16:25:08', 'hhh', 4, NULL, NULL),
(2, NULL, 'I practice 20 minutes every morning with alphabet and greetings. It really helps with speed.', 0, '2026-03-09 23:56:55', 'My daily ASL routine', 7, NULL, NULL),
(3, NULL, 'I keep mixing up similar signs. Do you use flashcards, videos, or repetition drills?', 0, '2026-03-09 23:56:55', 'Best way to memorize signs?', 8, NULL, NULL),
(4, NULL, 'I completed the Daily Conversation course and got 86% on the quiz.', 0, '2026-03-09 23:56:55', 'Small win today', 9, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `quizzes`
--

CREATE TABLE `quizzes` (
  `id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `option1` varchar(255) DEFAULT NULL,
  `option2` varchar(255) DEFAULT NULL,
  `option3` varchar(255) DEFAULT NULL,
  `correct_answer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `quiz_questions`
--

CREATE TABLE `quiz_questions` (
  `id` int(11) NOT NULL,
  `prompt` varchar(512) NOT NULL,
  `prompt_media` varchar(512) DEFAULT NULL,
  `prompt_type` varchar(32) NOT NULL,
  `answer_index` int(11) NOT NULL,
  `options` text NOT NULL,
  `category` varchar(64) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `quiz_questions`
--

INSERT INTO `quiz_questions` (`id`, `prompt`, `prompt_media`, `prompt_type`, `answer_index`, `options`, `category`, `created_at`) VALUES
(1, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/A.gif', 'gif_to_label', 0, '[{\"label\": \"A\", \"gif\": \"/static/asl_gifs/alphabet/A.gif\"}, {\"label\": \"B\", \"gif\": \"/static/asl_gifs/alphabet/B.gif\"}, {\"label\": \"G\", \"gif\": \"/static/asl_gifs/alphabet/G.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(2, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/B.gif', 'gif_to_label', 1, '[{\"label\": \"A\", \"gif\": \"/static/asl_gifs/alphabet/A.gif\"}, {\"label\": \"B\", \"gif\": \"/static/asl_gifs/alphabet/B.gif\"}, {\"label\": \"C\", \"gif\": \"/static/asl_gifs/alphabet/C.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(3, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/C.gif', 'gif_to_label', 0, '[{\"label\": \"C\", \"gif\": \"/static/asl_gifs/alphabet/C.gif\"}, {\"label\": \"D\", \"gif\": \"/static/asl_gifs/alphabet/D.gif\"}, {\"label\": \"E\", \"gif\": \"/static/asl_gifs/alphabet/E.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(4, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/D.gif', 'gif_to_label', 0, '[{\"label\": \"D\", \"gif\": \"/static/asl_gifs/alphabet/D.gif\"}, {\"label\": \"F\", \"gif\": \"/static/asl_gifs/alphabet/F.gif\"}, {\"label\": \"H\", \"gif\": \"/static/asl_gifs/alphabet/H.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(5, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/F.gif', 'gif_to_label', 1, '[{\"label\": \"E\", \"gif\": \"/static/asl_gifs/alphabet/E.gif\"}, {\"label\": \"F\", \"gif\": \"/static/asl_gifs/alphabet/F.gif\"}, {\"label\": \"G\", \"gif\": \"/static/asl_gifs/alphabet/G.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(6, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/H.gif', 'gif_to_label', 1, '[{\"label\": \"G\", \"gif\": \"/static/asl_gifs/alphabet/G.gif\"}, {\"label\": \"H\", \"gif\": \"/static/asl_gifs/alphabet/H.gif\"}, {\"label\": \"I\", \"gif\": \"/static/asl_gifs/alphabet/I.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(7, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/L.gif', 'gif_to_label', 1, '[{\"label\": \"K\", \"gif\": \"/static/asl_gifs/alphabet/K.gif\"}, {\"label\": \"L\", \"gif\": \"/static/asl_gifs/alphabet/L.gif\"}, {\"label\": \"M\", \"gif\": \"/static/asl_gifs/alphabet/M.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(8, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/O.gif', 'gif_to_label', 0, '[{\"label\": \"O\", \"gif\": \"/static/asl_gifs/alphabet/O.gif\"}, {\"label\": \"P\", \"gif\": \"/static/asl_gifs/alphabet/P.gif\"}, {\"label\": \"Q\", \"gif\": \"/static/asl_gifs/alphabet/Q.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(9, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/R.gif', 'gif_to_label', 1, '[{\"label\": \"P\", \"gif\": \"/static/asl_gifs/alphabet/P.gif\"}, {\"label\": \"R\", \"gif\": \"/static/asl_gifs/alphabet/R.gif\"}, {\"label\": \"T\", \"gif\": \"/static/asl_gifs/alphabet/T.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(10, 'What letter does this ASL sign represent?', '/static/asl_gifs/alphabet/S.gif', 'gif_to_label', 1, '[{\"label\": \"R\", \"gif\": \"/static/asl_gifs/alphabet/R.gif\"}, {\"label\": \"S\", \"gif\": \"/static/asl_gifs/alphabet/S.gif\"}, {\"label\": \"T\", \"gif\": \"/static/asl_gifs/alphabet/T.gif\"}]', 'alphabet', '2026-03-11 03:02:40'),
(11, 'Which GIF shows the correct ASL sign for \"HELLO\"?', NULL, 'label_to_gif', 0, '[{\"label\": \"HELLO\", \"gif\": \"/static/asl_gifs/greetings/HELLO.mp4\"}, {\"label\": \"THANK YOU\", \"gif\": \"/static/asl_gifs/greetings/THANK_YOU.mp4\"}, {\"label\": \"GOODBYE\", \"gif\": \"/static/asl_gifs/greetings/GOODBYE.mp4\"}]', 'greetings', '2026-03-11 03:02:40'),
(12, 'Which GIF shows the correct ASL sign for \"THANK YOU\"?', NULL, 'label_to_gif', 0, '[{\"label\": \"THANK YOU\", \"gif\": \"/static/asl_gifs/greetings/THANK_YOU.mp4\"}, {\"label\": \"PLEASE\", \"gif\": \"/static/asl_gifs/greetings/PLEASE.mp4\"}, {\"label\": \"HELLO\", \"gif\": \"/static/asl_gifs/greetings/HELLO.mp4\"}]', 'greetings', '2026-03-11 03:02:40'),
(13, 'What word does this ASL sign represent?', '/static/asl_gifs/greetings/PLEASE.mp4', 'gif_to_label', 0, '[{\"label\": \"PLEASE\", \"gif\": \"/static/asl_gifs/greetings/PLEASE.mp4\"}, {\"label\": \"THANK YOU\", \"gif\": \"/static/asl_gifs/greetings/THANK_YOU.mp4\"}, {\"label\": \"HELLO\", \"gif\": \"/static/asl_gifs/greetings/HELLO.mp4\"}]', 'greetings', '2026-03-11 03:02:40'),
(14, 'What word does this ASL sign represent?', '/static/asl_gifs/greetings/GOODBYE.mp4', 'gif_to_label', 0, '[{\"label\": \"GOODBYE\", \"gif\": \"/static/asl_gifs/greetings/GOODBYE.mp4\"}, {\"label\": \"MY NAME IS\", \"gif\": \"/static/asl_gifs/greetings/MY_NAME_IS.mp4\"}, {\"label\": \"NICE TO MEET YOU\", \"gif\": \"/static/asl_gifs/greetings/NICE_TO_MEET_YOU.mp4\"}]', 'greetings', '2026-03-11 03:02:40'),
(15, 'What word does this ASL sign represent?', '/static/asl_gifs/daily/THIRSTY.mp4', 'gif_to_label', 0, '[{\"label\": \"THIRSTY\", \"gif\": \"/static/asl_gifs/daily/THIRSTY.mp4\"}, {\"label\": \"HUNGRY\", \"gif\": \"/static/asl_gifs/daily/HUNGRY.mp4\"}, {\"label\": \"WATER\", \"gif\": \"/static/asl_gifs/daily/WATER.mp4\"}]', 'daily', '2026-03-11 03:02:40'),
(16, 'What word does this ASL sign represent?', '/static/asl_gifs/daily/HUNGRY.mp4', 'gif_to_label', 0, '[{\"label\": \"HUNGRY\", \"gif\": \"/static/asl_gifs/daily/HUNGRY.mp4\"}, {\"label\": \"TIRED\", \"gif\": \"/static/asl_gifs/daily/TIRED.mp4\"}, {\"label\": \"FOOD\", \"gif\": \"/static/asl_gifs/daily/FOOD.mp4\"}]', 'daily', '2026-03-11 03:02:40'),
(17, 'Which GIF shows the correct ASL sign for \"WATER\"?', NULL, 'label_to_gif', 0, '[{\"label\": \"WATER\", \"gif\": \"/static/asl_gifs/daily/WATER.mp4\"}, {\"label\": \"SLEEP\", \"gif\": \"/static/asl_gifs/daily/SLEEP.mp4\"}, {\"label\": \"FOOD\", \"gif\": \"/static/asl_gifs/daily/FOOD.mp4\"}]', 'daily', '2026-03-11 03:02:40'),
(18, 'Which GIF shows the correct ASL sign for \"HELP\"?', NULL, 'label_to_gif', 0, '[{\"label\": \"HELP\", \"gif\": \"/static/asl_gifs/daily/HELP.mp4\"}, {\"label\": \"PLEASE\", \"gif\": \"/static/asl_gifs/daily/PLEASE.mp4\"}, {\"label\": \"TIRED\", \"gif\": \"/static/asl_gifs/daily/TIRED.mp4\"}]', 'daily', '2026-03-11 03:02:40'),
(19, 'Which GIF shows the correct ASL sign for \"BRUSH TEETH\"?', NULL, 'label_to_gif', 0, '[{\"label\": \"BRUSH TEETH\", \"gif\": \"/static/asl_gifs/daily_verbs/BRUSH_TEETH.mp4\"}, {\"label\": \"WASH\", \"gif\": \"/static/asl_gifs/daily_verbs/WASH.mp4\"}, {\"label\": \"SHOWER\", \"gif\": \"/static/asl_gifs/daily_verbs/SHOWER.mp4\"}]', 'daily_verbs', '2026-03-11 03:02:40'),
(20, 'What word does this ASL sign represent?', '/static/asl_gifs/daily_verbs/DRINK.mp4', 'gif_to_label', 0, '[{\"label\": \"DRINK\", \"gif\": \"/static/asl_gifs/daily_verbs/DRINK.mp4\"}, {\"label\": \"EAT\", \"gif\": \"/static/asl_gifs/daily_verbs/EAT.mp4\"}, {\"label\": \"WAKE UP\", \"gif\": \"/static/asl_gifs/daily_verbs/WAKE_UP.mp4\"}]', 'daily_verbs', '2026-03-11 03:02:40');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(100) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `created_at`, `username`, `full_name`, `hashed_password`, `is_active`, `is_admin`) VALUES
(1, NULL, 'test2@example.com', NULL, '2026-02-22 16:03:41', 'test2', NULL, '$pbkdf2-sha256$29000$c.7dG8PYu5fSWstZa20NQQ$rv50gf.OPdT4IpA8AGOOeGKgZt6vSy1h08guXDGLLNI', 1, 0),
(2, NULL, 'adil@gmail.com', NULL, '2026-02-22 16:05:26', 'adil', 'adil jeddi', '$pbkdf2-sha256$29000$xhhDqPX./9/b.//fm7PWug$lhi4cuGoHuK9a585ve3IFn/rzvS.QFoY46OA9l4gJm8', 1, 0),
(3, NULL, 'x3@example.com', NULL, '2026-02-22 16:05:54', 'x3', NULL, '$pbkdf2-sha256$29000$yjmH0BpjLAVgrJXynpPyHg$Lp55p1gR/mgmdoO3.bZfFjeBWMW5NYljdsmH/VLACX0', 1, 0),
(4, NULL, 'houda@gmail.com', NULL, '2026-02-22 16:08:25', 'houda', 'houda harbal', '$pbkdf2-sha256$29000$USplTMnZWwvhnDPm3HtvzQ$d5jhf3TRPiW/b0bnKyw7wVyHQ9/8OOe262MvXK4/ifE', 1, 0),
(5, NULL, 'harbalhiba1@gmail.com', NULL, '2026-02-22 19:24:08', 'hiba', 'harbal hiba', '$pbkdf2-sha256$29000$qzWGEEJojdFaC6G0FsKYUw$DR0CQM.tKCTTdBaGVRDquwziDS0AkSZnZNTgEP9yo9Q', 1, 0),
(6, NULL, 'AYABEN@gmail.com', NULL, '2026-03-06 02:43:17', 'aya', NULL, '$pbkdf2-sha256$29000$GQMgJCSk1BoD4HyPcY5xLg$u.2U2wf6WFW6yTbrp2UMznq/4EofC3tBs4xhMtaao0I', 1, 1),
(7, NULL, 'sarah.asl@example.com', NULL, '2026-03-09 23:56:55', 'sarah_asl', 'Sarah Miller', '$pbkdf2-sha256$29000$0fp/j/EegxCC8F5rTck5Jw$dqQ2K2Zj3QPytHiriQ/Qk9C6/7Qo9l39YYJc475.S3Y', 1, 0),
(8, NULL, 'mike.signs@example.com', NULL, '2026-03-09 23:56:55', 'mike_signs', 'Mike Brown', '$pbkdf2-sha256$29000$5hzDOIdw7t3bO8fY21vL.Q$lb.aWhKZRH6PLCF8VbubhsccLABnLvwooKJGHmJOkMo', 1, 0),
(9, NULL, 'lina.daily@example.com', NULL, '2026-03-09 23:56:55', 'lina_daily', 'Lina Davis', '$pbkdf2-sha256$29000$5vx/z1kLoZSSMsaYs9b6Pw$MxyOEld3m6iGvq7rTh/Y2A68mIxVrNg0C7u8j./e4Mw', 1, 0),
(10, NULL, 'admin@easyconnect.local', NULL, '2026-03-11 03:02:40', 'admin', 'Administrateur', '$pbkdf2-sha256$29000$WivF2FsrxdhbC.GcEyIkBA$vDnQe402yJA3Jj878smjYFDb/BbzoV7mhHZmkIlbDZo', 1, 1),
(11, NULL, 'AYAUSE@gmail.com', NULL, '2026-03-11 03:08:21', 'aya1', NULL, '$pbkdf2-sha256$29000$mzNGqLU25rzXGkPo/R9jjA$.TFOyliewQUMYgACGirupebTp/kDURbVwcG2ZijcMp8', 1, 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activity_history`
--
ALTER TABLE `activity_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_activity_logs_id` (`id`),
  ADD KEY `ix_activity_logs_user_id` (`user_id`);

--
-- Index pour la table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `ix_comments_id` (`id`);

--
-- Index pour la table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `learning_item_progress`
--
ALTER TABLE `learning_item_progress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_learning_item_progress` (`user_id`,`course_id`,`item_id`),
  ADD KEY `ix_learning_item_progress_user_id` (`user_id`),
  ADD KEY `ix_learning_item_progress_item_id` (`item_id`),
  ADD KEY `ix_learning_item_progress_course_id` (`course_id`),
  ADD KEY `ix_learning_item_progress_id` (`id`);

--
-- Index pour la table `learning_progress`
--
ALTER TABLE `learning_progress`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_learning_progress_course_id` (`course_id`),
  ADD KEY `ix_learning_progress_id` (`id`);

--
-- Index pour la table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `quizzes`
--
ALTER TABLE `quizzes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`);

--
-- Index pour la table `quiz_questions`
--
ALTER TABLE `quiz_questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_quiz_questions_id` (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `activity_history`
--
ALTER TABLE `activity_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT pour la table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `learning_item_progress`
--
ALTER TABLE `learning_item_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT pour la table `learning_progress`
--
ALTER TABLE `learning_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `quizzes`
--
ALTER TABLE `quizzes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `quiz_questions`
--
ALTER TABLE `quiz_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `activity_history`
--
ALTER TABLE `activity_history`
  ADD CONSTRAINT `activity_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`);

--
-- Contraintes pour la table `learning_item_progress`
--
ALTER TABLE `learning_item_progress`
  ADD CONSTRAINT `learning_item_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `learning_progress`
--
ALTER TABLE `learning_progress`
  ADD CONSTRAINT `learning_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `quizzes`
--
ALTER TABLE `quizzes`
  ADD CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
