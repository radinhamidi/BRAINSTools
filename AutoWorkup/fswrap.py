# Standard library imports
import os
import sys

# Local imports
from nipype.interfaces.base import (TraitedSpec, Directory, File, traits, InputMultiPath, OutputMultiPath, isdefined)
from nipype.utils.filemanip import split_filename
from nipype.interfaces.base import CommandLine, CommandLineInputSpec


class FSScriptInputSpec(CommandLineInputSpec):
    T1_files = File(argstr='--T1image %s', exists=True, desc='Original T1 image')
    brainmask = File(argstr='--BrainLabel %s', exists=True,
                     desc='The normalized T1 image with the skull removed. Normalized 0-110 where white matter=110.')
    wm_prob = File(argstr='--WMProb %s', exists=True, desc='')
    subject_id = traits.Str(argstr='--SubjID %s', desc='Subject_Session')
    subjects_dir = Directory(argstr='--FSSubjDir %s', desc='FreeSurfer subjects directory')
#TODO:    fs_env_script = traits.Str(argstr='--FSSource %s', default='${FREESURFER_HOME}/FreeSurferEnv.sh',
#TODO:                           desc='')
#TODO:    fs_home = Directory(argstr='--FSHomeDir %s',
#TODO:                         desc='Location of FreeSurfer (differs for Mac and Linux environments')

class FSScriptOutputSpec(TraitedSpec):
    T1_out = File(exist=True, desc='brain.mgz')
    label1_out = File(exist=True, desc='aparc+aseg.nii.gz')
    label2_out = File(exist=True, desc='aparc.a2009+aseg.nii.gz')

class FSScript(CommandLine):
    """
    Examples
    --------
    """

    import inspect, os
    this_file=inspect.getfile(inspect.currentframe()) # script filename (usually with path)
    this_path=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script)

    _cmd = '{0} {1}'.format(sys.executable, os.path.join(this_path,'fsscript.py'))
#_cmd = 'fsscript.py'
    input_spec = FSScriptInputSpec
    output_spec = FSScriptOutputSpec

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['T1_out'] = os.path.join(os.getcwd(), 'mri', 'brain.mgz')
        outputs['label1_out'] = os.path.join(os.getcwd(), 'mri_nifti', 'aparc+aseg.nii.gz')
        outputs['label2_out'] = os.path.join(os.getcwd(), 'mri_nifti', 'aparc.a2009+aseg.nii.gz')
        return outputs
