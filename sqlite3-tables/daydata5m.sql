/*
 Navicat SQLite Data Transfer

 Source Server         : conn1
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 17/08/2017 18:02:21
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for daydata5m
-- ----------------------------
DROP TABLE IF EXISTS "daydata5m";
CREATE TABLE "daydata5m" (
  "ID" integer NOT NULL,
  "stockCode" integer NOT NULL,
  "stockDate" integer NOT NULL,
  "stockOpen" real,
  "stockHigh" real,
  "stockLow" real,
  "stockClose" real,
  "stockVol" real,
  "stockAmount" real,
  PRIMARY KEY ("ID")
);

-- ----------------------------
-- Indexes structure for table daydata5m
-- ----------------------------
CREATE INDEX "_stockCode"
ON "daydata5m" (
  "stockCode" ASC
);
CREATE INDEX "_stockDate"
ON "daydata5m" (
  "stockDate" ASC
);

PRAGMA foreign_keys = true;
