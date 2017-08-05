#!/usr/bin/env python
# -*- encoding=utf-8 -*-

########################################
# Copyright (c) 2017 Shanghai Kimstars #
########################################

import os
import json
import logging
import random
import datetime

# wrtnode.__name__
logger = logging.getLogger('wrtnode.' + __name__)


def dt_to_strftime(dt, randomsecond=False):
    """
    @brief      format datetime to string in '%Y-%m-%d %H:%M:%S.%f'

    @param      utcdt  The utcdt

    @return     { description_of_the_return_value }
    """
    if not isinstance(dt, datetime.datetime):
        return None

    if randomsecond:
        randomsecond = dt.second + random.randint(0, 2)
    else:
        randomsecond = dt.second

    strftime = '%0.4d-%0.2d-%0.2d %0.2d:%0.2d:%0.2d' % (dt.year,
                                                        dt.month,
                                                        dt.day,
                                                        dt.hour,
                                                        dt.minute,
                                                        randomsecond)
    return strftime


def read_json_file(path):
    #######################
    # read JSON file
    #######################
    json_string = ""
    file_error = False
    try:
        jfile = open(path, "r")
        lines = jfile.readlines()
    except IOError as err:
        logger.error('read_json_file: ' + str(err))
        file_error = True
    else:
        for line in lines:
            json_string = json_string + line.strip()
        # allow comma in the last line
        json_string = json_string.replace(',}', '}')
    finally:
        if 'jfile' in locals():
            jfile.close()

    if file_error:
        return None

    try:
        jsonObject = json.loads(json_string)
    except Exception as e:
        jsonObject = None
        logger.error('read_json_file: ' + str(e))

    return jsonObject


def read_txt_file(path):
    #######################
    # read txt file
    # real all lines
    #######################
    json_string = ""
    file_error = False
    try:
        jfile = open(path, "r")
        lines = jfile.read()
    except IOError as err:
        logger.error('read_txt_file: ' + str(err))
        file_error = True
    finally:
        if 'jfile' in locals():
            jfile.close()

    if file_error:
        return None
    else:
        return lines


def write_json_file(path, contentOject):
    # json_string = json.dumps(contentOject, 'utf-8')
    json_string = json.dumps(contentOject, sort_keys=True, indent=4,
                             ensure_ascii=False)
    try:
        config_file = open(path, "w")
        config_file.write(json_string)
        r = True
    except IOError as err:
        errorStr = 'File Error:' + str(err)
        logger.error(errorStr)
        r = False
    finally:
        if 'config_file' in locals():
            config_file.close()
    return r


def check_key_types(jsonObject, key, types):
    """
    @brief      check the dict key and type
    @param      jsonObject  The json object
    @param      key         The key
    @param      types       tuple of types
    @return     True/False
    """
    if not isinstance(jsonObject, dict):
        return False

    if not (key in jsonObject):
        # s = "%s not found in jsonObject" % key
        # logger.debug(s)
        return False

    if not isinstance(jsonObject[key], types):
        # s = "jsonObject['%s'] is not in types %s" % (key, str(types))
        # logger.debug(s)
        return False

    return True


def list_files(path=None, postfix=None):
    if path is None:
        path = '.'

    files = []
    postfix_list = []

    if isinstance(postfix, str):
        postfix_list.append(postfix)
    elif isinstance(postfix, tuple):
        for item in postfix:
            postfix_list.append(item)
    elif postfix is None:
        postfix_list = None

    for file in os.listdir(path):
        if postfix_list is None:
            files.append(file)
        else:
            s = file.split('.')
            if len(s) > 1 and s[1] in postfix_list:
                files.append(file)

    return files


def check_mqtt_config(jsonObject):
    if not isinstance(jsonObject, dict):
        return False

    if not check_key_types(jsonObject, 'host', str):
        err = "key 'host' error"
        logger.error(err)
        return False

    if not check_key_types(jsonObject, 'port', (int, float)):
        err = "key 'port' error"
        logger.error(err)
        return False

    if not check_key_types(jsonObject, 'keepalive', (int, float)):
        err = "key 'keepalive' error"
        logger.error(err)
        return False

    if not check_key_types(jsonObject, 'topicPrefix', str):
        err = "key 'topicPrefix' error"
        logger.error(err)
        return False

    if not check_key_types(jsonObject, 'useTLS', bool):
        err = "key 'useTLS' error"
        logger.error(err)
        return False

    return True
