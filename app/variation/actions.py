import os
import subprocess
from settings import basedir
from app.mail import send_mail
from app.db import DB

SNP_SCRIPT_DIR = '/public/script/snp_index_table'
SCRIPT_FILE = 'mergeSampleAlleSnpEff.py'
INPUT_TABLE = ''


def create_group_info(groupA, groupB, filename):
    groupA_name = filename.split('vs')[0]
    groupB_name = filename.split('vs')[1]
    with open(filename, 'w+') as f:
        for sample in groupA:
            f.write('\t'.join([sample, groupA_name]) + '\n')
        for sample in groupB:
            f.write('\t'.join([sample, groupB_name]) + '\n')


def run_snp_variations(group_info, user):
    group_name = group_info.keys()
    groupA = group_info[group_name[0]]
    groupB = group_info[group_name[1]]
    create_group_info(groupA, groupB, filename='vs'.join(group_name))
    cmd = "python {script} -i {input} -o {output} -g {group} -d {depth}".format(
        script=SCRIPT_FILE,
        input=INPUT_TABLE,
        output=os.path.join(basedir, 'app', 'static', 'variation_results', 'vs'.join(group_name) + '_table'),
        group=os.path.join(SNP_SCRIPT_DIR, 'vs'.join(group_name)),
        depth=''
    )
    subprocess.call(cmd, shell=True)
    db = DB()
    results = db.execute("select email from users where username='{0}'".format(user))
    if results[0][0]:
        to = results[0][0]
        send_mail(to, 'Snp Variation Results',
                  'mail/variation_results', user=user, href='')



