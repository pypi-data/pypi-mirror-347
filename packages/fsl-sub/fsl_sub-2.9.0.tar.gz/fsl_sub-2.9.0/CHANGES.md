# Change List

## 2.9.0

- Environment variable added to switch off auto-queue select and the application of time/memory and thread limits
- Add queue option to ensure that even numbers of threads are always requested when running with SMT enabled on SLURM
- Warning about submitting to a CUDA queue without requesting a coprocessor
- Coprocessor module loading fixed
- Begin transition to pytest
- Update to new setuptools system
- Code cleanup/refactoring to make testing easier
- Clarification of --extra usage
- Drop support for Python 3.8
- Add support for Python 3.13

## 2.8.4

- Ignore trailing semi-colons in first command read from command files run with
  `fsl_sub -t commands.txt`

## 2.8.3

- Return shell plugin's default output control to log to file

## 2.8.2

- Add license file
- Change to release status

## 2.8.1

- Fix some test failures on Linux

## 2.8.0

- Make the shell plugin send it's output to the controlling shell by default - option to turn on old behaviour added
- Improve handling of multi-thread requests on SLURM

## 2.7.5

- Fix issue with config validator with SLURM clusters

## 2.7.4

- Improve handling of warning messages
- Improve handling of missing has_parallel_envs
- Check configuration for incorrect setting of modulecmd

## 2.7.3

- Avoid crash if method configuration does not specify has_parallel_envs

## 2.7.2 (shell plugin 2.0.2)

- Improved auto-queue selection ensuring shortest useable queue/partition is selected
- Shell plugin no longer crashes when running self-submitting non-array tasks
- Add configuration checks for parallel environments vs auto-split of large memeory jobs
- Don't crash if user's ~/.fsl_sub.yml is an empty file

## 2.7.1

- Further correction to submission of extra arguments to the grid backend
- Fix multi-slot support for SLURM and improve specification of slots required
- Add support for SLURM (or other plugins) providing coprocessor configurations

## 2.7.0

- Deprecate the `fsl_sub_plugin` and `fsl_sub_update` commands, as they won't
  be supported for newer conda-based FSL releases.

## 2.6.1

- Correction to submission of extra arguments to the grid backend

## 2.6.0

- Allow user local configuration file (~/.fsl_sub.yml) to contain mimimal
  changes to the system configuration.
- Add support for passing of scheduler specific arguments through to a
  plugin ('--extra', 'FSLSUB_EXTRA_*' and 'extra_args' submit() method
  argument).
- Report version number for all plugins.
- Improve error reporting in fsl_sub_plugin command when fsl_sub is installed separate from FSL

## 2.5.9

- Add support for Lmod environment modules
- Improve environment module handling

## 2.5.8

- Fixes for co-processor module detection on systems with many modules/complex module names

## 2.5.7

- Add support for setting environment variables for the 'submitted' job only
- Fix handling of complex shell commands

## 2.5.6

- Fixes tests on older python versions

## 2.5.5

- Fixes to plugin installer/updater
- Clarify installation instructions

## 2.5.4

- Adjusted parsing of command files so that commands can be contained
  within quotes, and command paths with spaces are interpeted (as long
  as the spaces are escaped within the command file).

## 2.5.3 First Public Release
