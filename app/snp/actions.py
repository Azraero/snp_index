import os
import glob
import subprocess
from settings import basedir
from app.utils import get_db_tables

SNP_INDEX_PATH = os.path.join(basedir, 'app', 'static', 'snp_results')
RENDER_PATH = '/static/snp_results'
PLOT_SCRIPT_DIR = '/public/script/snp_index_plot'

def get_select_group_info(select_group):
    plot_path = 'vs'.join(select_group.split('_')) + '_plot'
    select_group_path = os.path.join(SNP_INDEX_PATH, select_group, plot_path)
    plot_files = glob.glob(select_group_path + '/*.png')
    plot_files = [os.path.join(RENDER_PATH, select_group, plot_path, each.rsplit('/', 1)[1]) for each in plot_files]
    return plot_files


def get_snp_info(user, rm_len=3):
    tables = get_db_tables(user, type='snp')
    groups = os.listdir(SNP_INDEX_PATH)
    # rm group dir when > 3
    if len(groups) > rm_len:
        rm_groups = groups[rm_len:]
        for dir in rm_groups:
            subprocess.call('rm -rf {0}'.format(os.path.join(SNP_INDEX_PATH,
                                                                dir)), shell=True)
    return tables, groups


def run_snpplot_script(filepath, outdir):
    # run bash&R script for snp index
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    runCmd = 'python {run_snp_index_file} --bedfile {bedfile} --filepath {filepath} --outdir {outdir}'.format(
        run_snp_index_file=os.path.join(PLOT_SCRIPT_DIR, 'run_snp_index.py'),
        bedfile=os.path.join(PLOT_SCRIPT_DIR, 'w2k'),
        filepath=filepath,
        outdir=outdir
    )
    subprocess.call(runCmd, shell=True)
    return 'done'