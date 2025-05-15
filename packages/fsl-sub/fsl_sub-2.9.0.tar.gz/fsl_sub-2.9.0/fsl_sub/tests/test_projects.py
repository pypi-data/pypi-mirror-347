#!/usr/bin/env python
import unittest
import fsl_sub.projects
import fsl_sub.exceptions

from unittest.mock import patch


class FakePlugin(object):
    def __init__(self, projects=[]):
        self.projects = projects

    def project_list(self):
        return self.projects


class TestConfig(unittest.TestCase):
    @patch(
        'fsl_sub.projects.read_config',
        return_value={'method': 'slurm', })
    def test_project_list(self, mock_rc):
        project_list = ['myproject', ]
        fp = FakePlugin(projects=project_list)
        with patch(
                'fsl_sub.projects.load_plugins',
                return_value={'fsl_sub_plugin_slurm': fp, }):
            self.assertEqual(
                fsl_sub.projects.project_list(),
                project_list
            )

            mock_rc.return_value = {'method': 'ge'}
            self.assertRaises(
                fsl_sub.exceptions.BadConfiguration,
                fsl_sub.projects.project_list
            )

            mock_rc.return_value = {'method': 'shell'}
            self.assertIsNone(
                fsl_sub.projects.project_list()
            )

    @patch('fsl_sub.projects.project_list', autospec=True)
    def test_project_exists(self, mock_project_list):
        mock_project_list.return_value = ['aproject', 'bproject', ]

        self.assertTrue(fsl_sub.projects.project_exists('aproject'))
        self.assertFalse(fsl_sub.projects.project_exists('cproject'))

    @patch('fsl_sub.projects.project_list', autospec=True)
    def test_projects(self, mock_project_list):
        mock_project_list.return_value = ['aproject', 'bproject', ]

        with self.subTest("Test get from environment 1"):
            with patch.dict(
                    'fsl_sub.projects.os.environ',
                    {'FSLSUB_PROJECT': 'AB'}, clear=True):
                self.assertEqual('AB', fsl_sub.projects.get_project_env(None))
        with self.subTest("Test get from environment 2"):
            with patch.dict(
                    'fsl_sub.projects.os.environ',
                    {'FSLSUB_PROJECT': 'AB'}, clear=True):
                self.assertEqual('CD', fsl_sub.projects.get_project_env('CD'))
        with self.subTest("Test environment is empty"):
            with patch.dict('fsl_sub.projects.os.environ', {}, clear=True):
                self.assertIsNone(fsl_sub.projects.get_project_env(None))
