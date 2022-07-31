CREATE TABLE `journal_entries` (
`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`concept`   TEXT NOT NULL,
`entry` TEXT NOT NULL,
`mood_id`    INTEGER NOT NULL,
`date`  DATE NOT NULL,
FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `moods` (
`id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`label` TEXT NOT NULL
);

CREATE TABLE `tag` (
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`name` TEXT NOT NULL 
);

CREATE TABLE `entry_tag` (
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`entry_id` INTEGER NOT NULL,
`tag_id` INTEGER NOT NULL,
FOREIGN KEY (`entry_id`) REFERENCES `journal_entries`(`id`),
FOREIGN KEY(`tag_id`) REFERENCES `tags`(`id`)
);

INSERT INTO `journal_entries` VALUES (null, "JavaScript", "I learned about loops today. They can be a lot of fun.",1 , 20220612);
INSERT INTO `journal_entries` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 4, 20220424);
INSERT INTO `journal_entries` VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 3, 20221008);
INSERT INTO `journal_entries` VALUES (null, "JavaScript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, 20221212);

INSERT INTO `moods` VALUES (null, "Happy");
INSERT INTO `moods` VALUES (null, "Sad");
INSERT INTO `moods` VALUES (null, "Angry");
INSERT INTO `moods` VALUES (null, "Ok");

INSERT INTO `tag` VALUES (null, "Chimachanga");
INSERT INTO `tag` VALUES (null, "Pickles");
INSERT INTO `tag` VALUES (null, "Rasta");

INSERT INTO `entry_tag` VALUES (null, 1, 2);
INSERT INTO `entry_tag` VALUES (null, 2, 1);

