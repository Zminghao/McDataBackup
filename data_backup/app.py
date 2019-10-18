# -*- coding: utf-8 -*-
import os

from qcloud_cos import CosConfig, CosS3Client

import configparser

from data_backup import tools, copyfile

if __name__ == '__main__':
    cf = configparser.ConfigParser()
    tools.print_a('开始进行文件备份')
    try:
        if "SERVICE_ENV" in os.environ:
            config = os.environ["SERVICE_ENV"]
        else:
            config = "CopyConfig.ini"
        cf.read(config, "utf-8")
        file_list = cf.get("copyfile", "SourceFiles")
        folder_name = cf.get("copyfile", "DestFolder")
        zipAndDel = cf.getint("copyfile", "zipAndDel")
        folderAddNow = cf.getint("copyfile", "FolderAddNow")
        dst_folder_name = copyfile.copy_and_zip(file_list, folder_name, zipAndDel, folderAddNow)

        tools.print_a('开始上传压缩文件')
        secret_id = cf.get("cossetting", "secret_id")
        secret_key = cf.get("cossetting", "secret_key")
        region = cf.get("cossetting", "region")
        token = cf.get("cossetting", "token")
        scheme = cf.get("cossetting", "scheme")
        cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        bucket = cf.get("cossetting", "bucket")
        client = CosS3Client(cos_config)
        response = client.upload_file(
            Bucket=bucket,
            LocalFilePath=dst_folder_name,
            Key='McDataBackup',
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        tools.print_i(response['ETag'])
    except Exception as e:
        tools.print_e(e)
    tools.print_d('文件备份成功')
