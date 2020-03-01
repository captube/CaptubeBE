import argparse

import boto3

argsParser = argparse.ArgumentParser()
args = argsParser.parse_args()
profile_name = args['profile'] if args.__contains__('profile') else 'dev'
session = boto3.Session(profile_name=profile_name)