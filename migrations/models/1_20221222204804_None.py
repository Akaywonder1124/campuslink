from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "role" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "role" VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS "school" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "school_email" VARCHAR(50) NOT NULL UNIQUE,
    "school_domain" VARCHAR(50) NOT NULL UNIQUE,
    "country" VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "full_name" VARCHAR(100) NOT NULL,
    "username" VARCHAR(30) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "about" TEXT,
    "profile_pic" VARCHAR(100),
    "date_of_birth" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "hashed_password" VARCHAR(128) NOT NULL,
    "member_since" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "restricted" INT NOT NULL  DEFAULT 0,
    "is_verified" INT NOT NULL  DEFAULT 0,
    "school_id" INT NOT NULL REFERENCES "school" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "interest" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "interest_name" VARCHAR(100) NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "interest_admin_id" INT REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "event" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "event_name" VARCHAR(100) NOT NULL,
    "event_status" VARCHAR(50) NOT NULL  DEFAULT 'Upcoming',
    "event_stus" VARCHAR(50) NOT NULL  DEFAULT 'Upcoming',
    "description" TEXT NOT NULL,
    "venue" TEXT NOT NULL,
    "event_date" TIMESTAMP NOT NULL,
    "is_appproved" INT NOT NULL  DEFAULT 0,
    "event_category_id" INT NOT NULL REFERENCES "interest" ("id") ON DELETE CASCADE,
    "event_creator_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_event" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "event_id" INT NOT NULL REFERENCES "event" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_user" (
    "user_rel_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_interest" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "interest_id" INT NOT NULL REFERENCES "interest" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
