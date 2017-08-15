/*
 Navicat SQLite Data Transfer

 Source Server         : conn1
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 15/08/2017 09:57:16
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for daydata5m
-- ----------------------------
DROP TABLE IF EXISTS "daydata5m";
CREATE TABLE "daydata5m" (
  "ID" integer NOT NULL,
  "stockCode" integer NOT NULL,
  "stockDate" text NOT NULL,
  "stockOpen" real,
  "stockHigh" real,
  "stockLow" real,
  "stockClose" real,
  "stockVol" real,
  "stockAmount" real,
  PRIMARY KEY ("ID")
);

PRAGMA foreign_keys = true;
