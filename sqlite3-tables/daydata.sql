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
DROP TABLE IF EXISTS "daydata";
CREATE TABLE "daydata" (
  "ID" integer NOT NULL,
  "stockCode" integer NOT NULL,
  "stockDate" integer NOT NULL,
  "stockOpen" real,
  "stockHigh" real,
  "stockLow" real,
  "stockClose" real,
  "stockVol" real,
  "stockAmount" real,
  "stockAvg" real,
  PRIMARY KEY ("ID")
);

-- ----------------------------
-- Indexes structure for table daydata5m
-- ----------------------------
CREATE INDEX "_stockCode"
ON "daydata" (
  "stockCode" ASC
);
CREATE INDEX "_stockDate"
ON "daydata" (
  "stockDate" ASC
);

PRAGMA foreign_keys = true;
