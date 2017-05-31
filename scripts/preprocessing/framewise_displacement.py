from os.path import join
from camcan.datasets import load_camcan_rest
from nipype.algorithms.confounds import FramewiseDisplacement
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


def _get_avg_fd(rp_file):
    fd = FramewiseDisplacement()
    fd.inputs.in_file = rp_file
    fd.inputs.parameter_source = 'SPM'
    out = fd.run()
    return out.outputs.fd_average


def _fd_one_scan(rp_file, subject_id):
    print(subject_id)
    fname = 'fd_%s_task-Rest_bold.txt' % subject_id
    output_file = join(DATA_DIR, subject_id, 'func', fname)
    fd = FramewiseDisplacement()
    fd.inputs.in_file = rp_file
    fd.inputs.out_file = output_file
    fd.inputs.parameter_source = 'SPM'
    out = fd.run()
    return out.outputs.fd_average


fd_subjects = Parallel(n_jobs=10, verbose=1)(delayed(
    _fd_one_scan)(m, s) for m, s in zip(dataset.motion, dataset.subject_id))
