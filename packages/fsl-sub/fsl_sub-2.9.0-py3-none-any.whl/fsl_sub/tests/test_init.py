#!/usr/bin/env python
import copy
import io
import getpass
import os
import pytest
import socket
import sys
import tempfile
import unittest
import fsl_sub
from ruamel.yaml import YAML
from unittest import skipIf
from unittest.mock import patch
from unittest.mock import MagicMock
from fsl_sub.exceptions import BadSubmission

YAML_CONF = '''---
method: sge
modulecmd: False
thread_control:
  - OMP_NUM_THREADS
preserve_modules: True
export_vars: []
method_opts:
    sge:
        queues: True
        large_job_split_pe: shmem
        has_parallel_envs: True
        copy_environment: True
        affinity_type: linear
        affinity_control: threads
        script_conf: True
        mail_support: True
        mail_modes:
            b:
                - b
            e:
                - e
            a:
                - a
            f:
                - a
                - e
                - b
            n:
                - n
        mail_mode: a
        map_ram: True
        thread_ram_divide: True
        notify_ram_usage: True
        ram_resources:
            - m_mem_free
            - h_vmem
        job_priorities: True
        min_priority: -1023
        max_priority: 0
        array_holds: True
        array_limit: True
        architecture: False
        job_resources: True
        projects: True
coproc_opts:
  cuda:
    resource: gpu
    classes: True
    class_resource: gputype
    class_types:
      K:
        resource: k80
        doc: Kepler. ECC, double- or single-precision workloads
        capability: 2
      P:
        resource: p100
        doc: >
          Pascal. ECC, double-, single- and half-precision
          workloads
        capability: 3
    default_class: K
    include_more_capable: True
    uses_modules: True
    uses_pe: False
    module_parent: cuda
    no_binding: True
queues:
  gpu.q:
    time: 18000
    max_size: 250
    slot_size: 64
    max_slots: 20
    copros:
      cuda:
        max_quantity: 4
        classes:
          - K
          - P
          - V
    map_ram: true
    parallel_envs:
      - shmem
    priority: 1
    group: 0
    default: true
  a.qa,a.qb,a.qc:
    time: 1440
    max_size: 160
    slot_size: 4
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 3
    group: 1
    default: true
  a.qa,a.qc:
    time: 1440
    max_size: 240
    slot_size: 16
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 2
    group: 1
    default: true
  a.qc:
    time: 1440
    max_size: 368
    slot_size: 16
    max_slots: 24
    map_ram: true
    parallel_envs:
      - shmem
    priority: 1
    group: 1
    default: true
  b.qa,b.qb,b.qc:
    time: 10080
    max_size: 160
    slot_size: 4
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 3
    group: 2
  b.qa,b.qc:
    time: 10080
    max_size: 240
    slot_size: 16
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 2
    group: 2
  b.qc:
    time: 10080
    max_size: 368
    slot_size: 16
    max_slots: 24
    map_ram: true
    parallel_envs:
      - shmem
    priority: 1
    group: 2
  t.q:
    time: 10080
    max_size: 368
    slot_size: 16
    max_slots: 24
    parallel_envs:
      - specialpe
    priority: 1
    group: 2

default_queues:
  - a.qa,a,qb,a.qc
  - a.qa,a.qc
  - a.qc

'''
USER_EMAIL = "{username}@{hostname}".format(
    username=getpass.getuser(),
    hostname=socket.gethostname()
)

real_read_config = fsl_sub.config.read_config


class FakePlugin(object):
    def submit(self):
        pass

    def qtest(self):
        pass

    def queue_exists(self):
        pass

    def plugin_version(self):
        pass

    def already_queued(self):
        return False


def ShellConfig_ltof():
    config = real_read_config()
    config['method'] = 'shell'
    config['method_opts']['shell']['log_to_file'] = True
    return config


@patch('fsl_sub.plugins.fsl_sub_plugin_shell.os.getpid', return_value=111)
@patch('fsl_sub.config.read_config', return_value=ShellConfig_ltof())
@patch(
    'fsl_sub.getq_and_slots', autospec=True,
    return_value=('vs.q', 2, ))
class ShellPluginSubmitTests(unittest.TestCase):
    def setUp(self):
        self.tempd = tempfile.TemporaryDirectory()
        self.here = os.getcwd()
        os.chdir(self.tempd.name)
        self.addCleanup(self.restore_dir)

    def restore_dir(self):
        os.chdir(self.here)
        self.tempd.cleanup()

    def test_basic_functionality(self, *arg):
        with io.StringIO() as text_trap:
            sys.stdout = text_trap
            fsl_sub.cmdline.main(['-q', 'vs.q', 'echo', 'hello'])
            sys.stdout = sys.__stdout__
            self.assertEqual(text_trap.getvalue(), '111\n')
        with open(
                os.path.join(
                    self.tempd.name, 'echo.o111'),
                mode='r') as ofile:
            output = ofile.read()
        self.assertEqual(output.strip(), 'hello')

    # doesn't work with Python 3.6!
    @skipIf(
        sys.version_info.major <= 3 and sys.version_info.minor < 8,
        'Requires python 3.8+')
    def test_set_fslsub_parallel(self, mock_gqas, mock_rc, mock_gp):
        with patch.dict('fsl_sub.os.environ', {}, clear=True) as mock_env:
            with patch(
                    'fsl_sub.cmdline.submit',
                    return_value=111) as mock_submit:
                with io.StringIO() as text_trap:
                    sys.stdout = text_trap
                    fsl_sub.cmdline.main(['-n', '-q', 'vs.q', '-t', 'mytasks'])
                    sys.stdout = sys.__stdout__
                    self.assertEqual(text_trap.getvalue(), '111\n')
            try:
                self.assertEqual('0', mock_env['FSLSUB_PARALLEL'])
            except KeyError:
                self.assertFail("FSLSUB_PARALLEL not set")
        mock_submit.assert_called()

    @skipIf(
        sys.version_info.major <= 3 and sys.version_info.minor < 8,
        'Requires python 3.8+')
    @patch(
        'fsl_sub.parallel.process_pe_def',
        autospec=True, return_value=('openmp', 2))
    def test_set_fslsub_parallel2(self, mock_ppd, mock_gqas, mock_rc, mock_gp):
        with patch.dict('fsl_sub.os.environ', {}, clear=True) as mock_env:
            with patch(
                    'fsl_sub.cmdline.submit', return_value=111) as mock_submit:
                with io.StringIO() as text_trap:
                    sys.stdout = text_trap
                    fsl_sub.cmdline.main(
                        [
                            '-n', '-q', 'vs.q',
                            '-s', 'openmp,2',
                            '-t', 'mytasks', ])
                    sys.stdout = sys.__stdout__
                    self.assertEqual(text_trap.getvalue(), '111\n')
            try:
                self.assertEqual('0', mock_env['FSLSUB_PARALLEL'])
            except KeyError:
                self.assertFail("FSLSUB_PARALLEL not set")
        mock_submit.assert_called()

    @skipIf(
        sys.version_info.major <= 3 and sys.version_info.minor < 8,
        'Requires python 3.8+')
    @patch(
        'fsl_sub.parallel.process_pe_def',
        autospec=True,
        return_value=('openmp', 2))
    def test_set_fslsub_parallel3(self, mock_ppd, mock_gqas, mock_rc, mock_gp):
        with patch.dict(
                'fsl_sub.os.environ',
                {'FSLSUB_PARALLEL': '4'},
                clear=True) as mock_env:
            with patch(
                    'fsl_sub.cmdline.submit', return_value=111) as mock_submit:
                with io.StringIO() as text_trap:
                    sys.stdout = text_trap
                    fsl_sub.cmdline.main(
                        [
                            '-n', '-q', 'vs.q',
                            '-s', 'openmp,2', '-t',
                            'mytasks', ])
                    sys.stdout = sys.__stdout__
                    self.assertEqual(text_trap.getvalue(), '111\n')
            try:
                self.assertEqual('4', mock_env['FSLSUB_PARALLEL'])
            except KeyError:
                self.assertFail("FSLSUB_PARALLEL not set")
        mock_submit.assert_called()


@pytest.fixture
def mock_submit(mocker):
    '''Fixture to mock all the functions called by submit()'''
    cf = YAML(typ='safe').load(YAML_CONF)
    plugins = {}

    plugins['fsl_sub_plugin_sge'] = FakePlugin()
    plugins['fsl_sub_plugin_sge'].submit = MagicMock(name='submit')
    plugins['fsl_sub_plugin_sge'].qtest = MagicMock(name='qtest')
    plugins['fsl_sub_plugin_sge'].qtest.return_value = '/usr/bin/qconf'
    plugins['fsl_sub_plugin_sge'].queue_exists = MagicMock(
        name='queue_exists')
    plugins['fsl_sub_plugin_sge'].queue_exists.return_value = True
    plugins['fsl_sub_plugin_sge'].BadSubmission = BadSubmission

    patches = {
        "coprocessors.read_config": mocker.patch(
            "fsl_sub.coprocessors.read_config",
            autospec=True,
            return_value=cf),
        "parallel.read_config": mocker.patch(
            "fsl_sub.parallel.read_config",
            autospec=True,
            return_value=cf),
        "shell_modules.read_config": mocker.patch(
            "fsl_sub.shell_modules.read_config",
            autospec=True,
            return_value=cf),
        "read_config": mocker.patch(
            "fsl_sub.read_config",
            autospec=True,
            return_value=cf),
        "config.read_config": mocker.patch(
            "fsl_sub.config.read_config",
            autospec=True,
            return_value=cf),
        "load_plugins": mocker.patch(
            'fsl_sub.load_plugins',
            autospec=True,
            return_value=plugins),
        "check_command": mocker.patch(
            'fsl_sub.command_exists',
            autospec=True),
        "projects.project_list": mocker.patch(
            'fsl_sub.projects.project_list',
            autospec=True,
            return_value=['a', 'b', ])
    }
    base_args = {
        'architecture': None,
        'array_hold': None,
        'array_limit': None,
        'array_specifier': None,
        'array_task': False,
        'coprocessor': None,
        'coprocessor_toolkit': None,
        'coprocessor_class': None,
        'coprocessor_class_strict': False,
        'coprocessor_multi': '1',
        'export_vars': [
            'OMP_NUM_THREADS=1',
            'FSLSUB_PARALLEL=1',
        ],
        'job_name': 'mycommand',
        'parallel_env': None,
        'queue': 'a.qa,a.qb,a.qc',
        'threads': 1,
        'jobhold': None,
        'jobram': None,
        'jobtime': None,
        'keep_jobscript': False,
        'logdir': None,
        'mail_on': 'a',
        'mailto': USER_EMAIL,
        'priority': None,
        'ramsplit': True,
        'requeueable': True,
        'resources': None,
        'usescript': False,
        'project': None,
        'extra_args': None,
    }

    return {
        'config': cf,
        'args': base_args,
        'mocks': patches,
        'plugins': plugins,
        }


def test_override_queue(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_OVERRIDE_QUEUE', 'a.qc')
    test_conf = copy.deepcopy(mock_submit['config'])
    test_conf['method_opts']['sge']['has_parallel_envs'] = False
    set_config(mock_submit, test_conf)

    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'a.qc'
    test_args['jobtime'] = 100000
    test_args['jobram'] = 100000
    test_args['threads'] = 1000
    test_args['export_vars'] = [
            f"OMP_NUM_THREADS={test_args['threads']}",
            f"FSLSUB_PARALLEL={test_args['threads']}",
        ]
    fsl_sub.submit(
        ['mycommand', ],
        jobtime=test_args['jobtime'],
        jobram=test_args['jobram'],
        threads=test_args['threads'])

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args)
    monkeypatch.delenv('FSLSUB_OVERRIDE_QUEUE')


def test_override_queue_unknown(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_OVERRIDE_QUEUE', 'unknown.q')
    test_conf = copy.deepcopy(mock_submit['config'])
    test_conf['method_opts']['sge']['has_parallel_envs'] = False
    set_config(mock_submit, test_conf)

    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'unknown.q'
    test_args['jobtime'] = 100000
    test_args['jobram'] = 100000
    test_args['threads'] = 1000
    test_args['export_vars'] = [
            f"OMP_NUM_THREADS={test_args['threads']}",
            f"FSLSUB_PARALLEL={test_args['threads']}",
        ]

    with pytest.warns(Warning) as record:
        fsl_sub.submit(
            ['mycommand', ],
            jobtime=test_args['jobtime'],
            jobram=test_args['jobram'],
            threads=test_args['threads'])
    assert record[0].message.args[0] == \
        "FSLSUB_OVERRIDE_QUEUE set to the name of an "\
        "unknown partition/queue"
    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args)
    monkeypatch.delenv('FSLSUB_OVERRIDE_QUEUE')


def test_extra_args(mock_submit):
    fsl_sub.submit(
        ['mycommand', ],
        queue='a.qc',
        extra_args=['--someoption=1'])
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'a.qc'
    test_args['extra_args'] = ['--someoption=1']
    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args)


def test_unknown_queue(mock_submit):
    fsl_sub.submit(['mycommand', ], queue='unconfigured.q')
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'unconfigured.q'
    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args)


def test_mem_env(mock_submit):
    fsl_sub.submit(['mycommand', ], jobram=None)

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **mock_submit['args']
        )


def test_no_memory(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_MEMORY_REQUIRED', '8G')
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'a.qa,a.qc'
    test_args['jobram'] = 8
    fsl_sub.submit(['mycommand', ], jobram=None)

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args
        )
    monkeypatch.delenv('FSLSUB_MEMORY_REQUIRED')


def test_mem_env_no_units(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_MEMORY_REQUIRED', '8')
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'a.qa,a.qc'
    test_args['jobram'] = 8
    fsl_sub.submit(['mycommand', ], jobram=None)

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args
        )
    monkeypatch.delenv('FSLSUB_MEMORY_REQUIRED')


def test_mem_env_small(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_MEMORY_REQUIRED', '32M')
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['queue'] = 'a.qa,a.qb,a.qc'
    test_args['jobram'] = 1
    fsl_sub.submit(['mycommand', ], jobram=None)

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args
        )


def test_stringcommand(mock_submit):
    fsl_sub.submit('mycommand arg1 arg2')

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', 'arg1', 'arg2', ],
            **mock_submit['args']
        )


def test_listcommand(mock_submit):
    fsl_sub.submit(['mycommand', 'arg1', 'arg2', ])

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', 'arg1', 'arg2', ],
            **mock_submit['args']
        )


def set_config(mock_submit, config):
    for mod in (
            'coprocessors.', 'parallel.',
            'shell_modules.', '', 'config.', ):
        mock_submit['mocks'][f'{mod}read_config'].\
            return_value = config


def test_multigpu_usespe(mock_submit):
    test_conf = copy.deepcopy(mock_submit['config'])

    test_conf['coproc_opts']['cuda']['uses_pe'] = 'shmem'
    set_config(mock_submit, test_conf)

    test_args = copy.deepcopy(mock_submit['args'])
    test_args['coprocessor'] = 'cuda'
    test_args['coprocessor_multi'] = '2'
    test_args['threads'] = 2
    test_args['parallel_env'] = 'shmem'
    test_args['queue'] = 'gpu.q'
    test_args['export_vars'] = [
        'OMP_NUM_THREADS=2',
        'FSLSUB_PARALLEL=2',
    ]
    fsl_sub.submit(
        ['mycommand', 'arg1', 'arg2', ],
        coprocessor='cuda',
        coprocessor_multi='2')

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', 'arg1', 'arg2', ],
            **test_args
        )


def test_multigpu_missingpe(mock_submit):
    test_conf = copy.deepcopy(mock_submit['config'])

    test_conf['coproc_opts']['cuda']['uses_pe'] = 'openmp'
    set_config(mock_submit, test_conf)

    with pytest.raises(BadSubmission) as eo:
        fsl_sub.submit(
            ['mycommand', 'arg1', 'arg2', ],
            coprocessor='cuda',
            coprocessor_multi='2')

    assert "uses_pe set but selected queue gpu.q "\
        "does not have PE openmp configured" in \
        str(eo.value)


def test_multigpu_toomanyslots(mock_submit):
    test_conf = copy.deepcopy(mock_submit['config'])

    test_conf['coproc_opts']['cuda']['uses_pe'] = 'shmem'
    test_conf['queues']['gpu.q']['max_slots'] = 2
    set_config(mock_submit, test_conf)

    with pytest.raises(BadSubmission) as eo:
        fsl_sub.submit(
            ['mycommand', 'arg1', 'arg2', ],
            coprocessor='cuda',
            coprocessor_multi='4')

    assert "More GPUs than queue slots have been requested" \
        in str(eo.value)


def test_multigpu_complex(mock_submit):
    test_conf = copy.deepcopy(mock_submit['config'])

    test_conf['coproc_opts']['cuda']['uses_pe'] = 'shmem'
    set_config(mock_submit, test_conf)

    with pytest.raises(BadSubmission) as eo:
        fsl_sub.submit(
            ['mycommand', 'arg1', 'arg2', ],
            coprocessor='cuda',
            coprocessor_multi='1,2')

    assert "Specified coprocessor_multi argument is a "\
        "complex value but cluster configured with 'uses_pe'"\
        " which requires a simple integer" in str(eo.value)


def test_fsl_sub_conf_var_set(mock_submit, monkeypatch):
    monkeypatch.setenv('FSLSUB_CONF', '/usr/local/etc/fsl_sub.yml')
    test_args = copy.deepcopy(mock_submit['args'])
    test_args['export_vars'].insert(
        0, 'FSLSUB_CONF=/usr/local/etc/fsl_sub.yml')
    fsl_sub.submit(['mycommand', ], jobram=None)

    mock_submit['plugins']['fsl_sub_plugin_sge'].\
        submit.assert_called_with(
            ['mycommand', ],
            **test_args
        )


class GetQTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conf_dict = YAML(typ='safe').load(YAML_CONF)

    def test_calc_slots(self):
        self.assertEqual(
            fsl_sub.calc_slots(64, 16, 2),
            4
        )
        self.assertEqual(
            fsl_sub.calc_slots(64, 16, 8),
            8
        )
        self.assertEqual(
            fsl_sub.calc_slots(32, None, 2),
            2
        )
        self.assertEqual(
            fsl_sub.calc_slots(None, None, 4),
            4
        )
        self.assertEqual(
            fsl_sub.calc_slots(None, None, 1),
            1
        )

    def test__slots_required(self):
        with self.subTest("Single q"):
            self.assertEqual(
                1,
                fsl_sub._slots_required(
                    'a.qa',
                    8,
                    self.conf_dict['queues'],
                    2
                ))
        with self.subTest("q and host"):
            self.assertEqual(
                1,
                fsl_sub._slots_required(
                    'a.qa@host',
                    8,
                    self.conf_dict['queues'],
                    2
                ))
        with self.subTest("Unconfigured q"):
            self.assertEqual(
                1,
                fsl_sub._slots_required(
                    'new.q',
                    100,
                    self.conf_dict['queues'],
                    1
                ))
        with self.subTest("Multi q"):
            self.assertEqual(
                13,
                fsl_sub._slots_required(
                    'a.qa,a.qc',
                    200,
                    self.conf_dict['queues'],
                    1
                ))

    def test_getq_and_slots(self):
        with self.subTest('All a queues'):
            self.assertTupleEqual(
                ('a.qa,a.qb,a.qc', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_time=1000)
            )
        with self.subTest('Default queue'):
            self.assertTupleEqual(
                ('a.qa,a.qb,a.qc', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'])
            )
        with self.subTest("More RAM"):
            self.assertTupleEqual(
                ('a.qa,a.qc', 13, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_time=1000,
                    job_ram=200)
            )
        with self.subTest("No time"):
            self.assertTupleEqual(
                ('a.qa,a.qc', 13, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_ram=200)
            )
        with self.subTest("More RAM"):
            self.assertTupleEqual(
                ('a.qc', 19, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_ram=300)
            )
        with self.subTest('Longer job'):
            self.assertTupleEqual(
                ('b.qa,b.qb,b.qc', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_time=2000)
            )
        simple_qs = {
            'long': {
                'time': 100, 'max_size': 1,
                'max_slots': 1, 'slot_size': 16,
                'priority': 1, 'group': 1, },
            'short': {
                'time': 10, 'max_size': 1,
                'max_slots': 1, 'slot_size': 16,
                'priority': 1, 'group': 1, },
        }
        with self.subTest('Shortest queue'):
            self.assertTupleEqual(
                ('short', 1, ),
                fsl_sub.getq_and_slots(
                    simple_qs,
                    job_time=10
                )
            )
        complex_qs = {
            'longa,longb': {
                'time': 100, 'max_size': 1,
                'max_slots': 2, 'slot_size': 16,
                'priority': 2, 'group': 1, },
            'longa': {
                'time': 100, 'max_size': 1,
                'max_slots': 2, 'slot_size': 16,
                'priority': 1, 'group': 1, },
            'longb': {
                'time': 100, 'max_size': 1,
                'max_slots': 1, 'slot_size': 16,
                'priority': 1, 'group': 1, },
            'short': {
                'time': 10, 'max_size': 1,
                'max_slots': 1, 'slot_size': 16,
                'priority': 1, 'group': 2, },
        }
        with self.subTest('Shortest queue (with groups)'):
            self.assertTupleEqual(
                ('short', 1, ),
                fsl_sub.getq_and_slots(
                    complex_qs,
                    job_time=10
                )
            )
        with self.subTest('Shortest queue (with groups) 2'):
            self.assertTupleEqual(
                ('longa,longb', 1, ),
                fsl_sub.getq_and_slots(
                    complex_qs,
                    job_time=20
                )
            )
        with self.subTest('Too long job'):
            self.assertRaises(
                fsl_sub.BadSubmission,
                fsl_sub.getq_and_slots,
                self.conf_dict['queues'],
                job_time=200000
            )
        with self.subTest("2x RAM"):
            self.assertRaises(
                fsl_sub.BadSubmission,
                fsl_sub.getq_and_slots,
                self.conf_dict['queues'],
                job_ram=600
            )
        with self.subTest('PE'):
            self.assertTupleEqual(
                ('t.q', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    ll_env="specialpe")
            )
        with self.subTest('PE missing'):
            self.assertRaises(
                fsl_sub.BadSubmission,
                fsl_sub.getq_and_slots,
                self.conf_dict['queues'],
                ll_env="unknownpe"
            )
        with self.subTest('GPU'):
            self.assertTupleEqual(
                ('gpu.q', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    coprocessor='cuda')
            )
        with self.subTest("job ram is none"):
            self.assertTupleEqual(
                ('a.qa,a.qb,a.qc', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_ram=None)
            )
        with self.subTest("job time is none"):
            self.assertTupleEqual(
                ('a.qa,a.qb,a.qc', 1, ),
                fsl_sub.getq_and_slots(
                    self.conf_dict['queues'],
                    job_time=None)
            )
        with self.subTest("No || env queues queues"):
            tq = {
                'gp_q':
                    {
                        'time': 100,
                        'max_slots': 1,
                        'max_size': 1,
                        'slot_size': 1,
                    },
            }
            with self.assertRaises(BadSubmission) as eo:
                fsl_sub.getq_and_slots(tq, ll_env='openmp')
            self.assertEqual(
                str(eo.exception),
                "No queues with requested parallel environment found")
        with self.subTest("Exclusive copro queues"):
            tq = {
                'gp_q':
                    {
                        'copros': {
                            'cuda': {
                                'exclusive': True,
                                'max_quantity': 1, }, },
                        'time': 100,
                        'max_slots': 1,
                        'max_size': 1,
                        'slot_size': 1,
                    },
            }
            with self.assertRaises(BadSubmission) as eo:
                fsl_sub.getq_and_slots(tq)
            self.assertEqual(
                str(eo.exception),
                "No queues found without co-processors defined that are non-exclusive")  # noqa E501
        with self.subTest("non-Exclusive copro queues"):
            tq = {
                'gp_q':
                    {
                        'copros': {
                            'cuda': {
                                'exclusive': False,
                                'max_quantity': 1, }, },
                        'time': 100,
                        'max_slots': 1,
                        'max_size': 1,
                        'slot_size': 1,
                    },
            }
            self.assertTupleEqual(
                fsl_sub.getq_and_slots(tq, coprocessor='cuda'),
                ('gp_q', 1, )
            )
            with self.subTest("No copro queues"):
                tq = {
                    'gp_q':
                        {
                            'time': 100,
                            'max_slots': 1,
                            'max_size': 1,
                            'slot_size': 1,
                        },
                }
                with self.assertRaises(BadSubmission) as eo:
                    fsl_sub.getq_and_slots(tq, coprocessor='cuda')
                self.assertEqual(
                    str(eo.exception),
                    "No queues with requested co-processor found")


class ExtraVars(unittest.TestCase):
    def test_extra_vars(self):
        with self.subTest('simple arguments'):
            environment = {
                'FSLSUB_EXTRA_QOS': "--qos=1",
                'FSLSUB_EXTRA_NOTHING': "--nothing", }
            extra_args = ['--qos=2', '--something', '--somethingelse=4']
            self.assertEqual(
                ['--qos=2', '--nothing', '--something', '--somethingelse=4'],
                fsl_sub._process_extra_args(extra_args, env=environment)
            )
        with self.subTest('= in arguments'):
            environment = {
                'FSLSUB_EXTRA_QOS': "--qos=1",
                'FSLSUB_EXTRA_NOTHING': "--nothing='something=1'", }
            extra_args = ['--qos=2', '--something', '--somethingelse=4']
            self.assertEqual(
                [
                    '--qos=2', "--nothing='something=1'",
                    '--something', '--somethingelse=4'],
                fsl_sub._process_extra_args(extra_args, env=environment)
            )


if __name__ == '__main__':
    unittest.main()
