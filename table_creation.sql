-- Table will contain meals of users and their nutritional values
CREATE TABLE `food_intake` (
  `user_id` integer,
  `meal_name` varchar(255),
  `calories` integer,
  `protein` integer,
  `carbs` integer,
  `fats` integer,
  `fiber` integer,
  `day` timestamp
);

-- Table will contain user information and their daily nutritional values
CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `username` varchar(255),
  `password` varchar(255),
  `weight` integer,
  `bodyfat` integer,
  `daily_calories` integer,
  `daily_protein` integer,
  `daily_carbs` integer,
  `daily_fats` integer
  `daily_fiber` integer
);

-- Table will contain standard meals of users and their nutritional values
CREATE TABLE `standard_meals` (
  `user_id` integer PRIMARY KEY,
  `meal_name` varchar(255),
  `calories` integer,
  `protein` integer,
  `carbs` integer,
  `fats` integer,
  `fiber` integer
);


-- Relations
ALTER TABLE `food_intake` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `standard_meals` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
