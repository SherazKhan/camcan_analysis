from os.path import join
from nipype.algorithms.confounds import CompCor
from camcan.datasets import load_camcan_rest
from joblib import Parallel, delayed

DATA_DIR = '/home/mehdi/data/camcan/camcan_preproc'
MASK = '/home/mehdi/data/camcan/camcan_smt_preproc/mask_camcan.nii.gz'
CAMCAN_CSV_FILE = '/home/mehdi/data/camcan/cc700-scored/participant_data.csv'
CAMCAN_PATIENTS_EXCLUDED = '/home/mehdi/data/camcan/camcan_preproc/'\
                           'excluded_subjects.csv'
dataset = load_camcan_rest(
    data_dir=DATA_DIR,
    patients_info_csv=CAMCAN_CSV_FILE,
    patients_excluded=CAMCAN_PATIENTS_EXCLUDED)


def _compcor_one_scan(func, subject_id, mask=MASK):
    print(subject_id)
    fname = 'cc_%s_task-Rest_bold.txt' % subject_id
    output_file = join(DATA_DIR, subject_id, 'func', fname)
    compcor = CompCor()
    compcor.inputs.components_file = output_file
    compcor.inputs.realigned_file = func
    compcor.inputs.mask_files = MASK
    compcor.inputs.num_components = 6
    output = compcor.run()
    return output.outputs.components_file

outputs = Parallel(n_jobs=10)(delayed(
    _compcor_one_scan)(func, subj)
    for func, subj in zip(dataset.func, dataset.subject_id))
