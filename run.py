import argparse
import logging
import os

import openpyxl

from logit import Logit

logger = logging.getLogger('LOGIT')


def run():
    option = get_option()
    setup_logger(option.log_level)

    logit = Logit()
    logger.debug('Open Excel File: {}'.format(option.output_path))
    wb = openpyxl.Workbook()
    ws = wb.create_sheet(os.path.basename(option.target_dir))
    ws.append(['Path', 'Hash', 'Author', 'Email', 'Date', 'Message'])
    file_list = list_dir(option.target_dir)
    logger.info('Saving git commit logs ({} file(s))'.format(len(file_list)))
    for p in file_list:
        logger.debug('Log: {}'.format(p))
        commits = logit.log(option.base_dir, p)
        for commit in commits:
            logger.debug('Excel append row: {}'.format(p))
            ws.append([p, commit['hash'], commit['author'], commit['email'], commit['date'], commit['message']])
    logger.debug('Save Excel File: {}'.format(option.output_path))
    wb.save(option.output_path)
    wb.close()
    logger.info('Done!')


def list_dir(path):
    result = []
    for p in os.listdir(path):
        full_path = os.path.join(path, p)
        if os.path.isdir(full_path):
            result.extend(list_dir(full_path))
        else:
            result.append(full_path)
    return result


def get_option():
    parser = argparse.ArgumentParser(description='Git Commit Log to Excel')
    parser.add_argument('-b', '--base-dir', type=str, required=True, help='Path of base git directory')
    parser.add_argument('-t', '--target-dir', type=str, required=True, help='Path of target directory')
    parser.add_argument('-o', '--output-path', type=str, required=True, help='Path of output excel file')
    parser.add_argument('-l', '--log-level', type=str, default='INFO', help='Log level')
    return parser.parse_args()


def setup_logger(log_level):
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    run()
