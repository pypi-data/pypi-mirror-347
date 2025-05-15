# fsl_sub python module
# Copyright (c) 2018-2021 University of Oxford (Duncan Mortimer)

import logging
import sys
import warnings
from collections import defaultdict
from fsl_sub.config import (
    coprocessor_config,
    read_config,
    method_config,
    queue_config,
    has_queues,
)
from fsl_sub.exceptions import (
    BadConfiguration,
    BadSubmission,
    UnrecognisedModule,
    NoModule,
)
from fsl_sub.shell_modules import (
    get_modules,
    load_module,
)


def list_coprocessors():
    '''Return a list of coprocessors found in the queue definitions'''
    # Are there any queues defined?
    avail_cops = []
    if has_queues():
        for q in queue_config().values():
            try:
                avail_cops.extend(q['copros'].keys())
            except KeyError:
                pass
    return avail_cops


def max_coprocessors(coprocessor):
    '''Return the maximum number of coprocessors per node from the
    queue definitions'''

    num_cops = 0

    for q in queue_config().values():
        if 'copros' in q:
            try:
                num_cops = max(
                    num_cops,
                    q['copros'][coprocessor]['max_quantity'])
            except KeyError:
                pass

    return num_cops


def coproc_classes(coprocessor):
    '''Return whether a coprocessor supports multiple classes of hardware.
    Classes are sorted by capability'''
    classes = defaultdict(lambda: 1)
    copro_opts = coprocessor_config(coprocessor)
    for q in queue_config().values():
        if 'copros' in q:
            try:
                for c in q['copros'][coprocessor]['classes']:
                    classes[c] = copro_opts['class_types'][c]['capability']
            except KeyError:
                continue
    if not classes:
        return None
    return sorted(classes.keys(), key=classes.get)


def coproc_toolkits(coprocessor):
    '''Return list of coprocessor toolkit versions.'''
    copro_conf = coprocessor_config(coprocessor)
    # Check that we have queues configured for this coproceesor
    if not all([q for q in queue_config() if (
            'copros' in q and coprocessor in q['copros'])]):
        raise BadConfiguration(
            "Coprocessor {} not available in any queues".format(
                coprocessor
            )
        )
    if not copro_conf['uses_modules']:
        return None
    try:
        cp_mods = get_modules(copro_conf['module_parent'])
    except NoModule:
        return None
    return cp_mods


def coproc_class(coproc_class, coproc_classes):
    try:
        for c, i in enumerate(coproc_classes):
            if c['shortcut'] == coproc_class:
                break
    except KeyError:
        raise BadConfiguration(
            "Co-processor class {} not configured".format(coproc_class),
            file=sys.stderr)
    return coproc_classes[:i]


def coproc_load_module(coproc, module_version):
    coproc = coprocessor_config(coproc)
    if coproc['uses_modules']:
        modules_avail = get_modules(coproc['module_parent'])
        if modules_avail:
            if module_version not in modules_avail:
                raise UnrecognisedModule(module_version)
            else:
                load_module("/".join(
                    (coproc['module_parent'], module_version)))


def coproc_get_module(coproc, module_version):
    copro_conf = coprocessor_config(coproc)
    module_name = None
    if copro_conf['uses_modules']:
        modules_avail = get_modules(copro_conf['module_parent'])
        if modules_avail:
            if module_version not in modules_avail:
                raise UnrecognisedModule(
                    '/'.join(
                        (copro_conf['module_parent'], module_version)))
            else:
                module_name = "/".join(
                    (copro_conf['module_parent'], module_version))
        else:
            raise UnrecognisedModule(copro_conf['module_parent'])
    return module_name


def coproc_info():
    available_coprocessors = list_coprocessors()
    coprocessor_classes = []
    coprocessor_toolkits = []
    for c in available_coprocessors:
        cp_classes = coproc_classes(c)
        cp_tkits = coproc_toolkits(c)
        if cp_classes is not None:
            coprocessor_classes.extend(cp_classes)
        if cp_tkits is not None:
            coprocessor_toolkits.extend(cp_tkits)
    if not available_coprocessors:
        available_coprocessors = None
    if not coprocessor_classes:
        coprocessor_classes = None
    if not coprocessor_toolkits:
        coprocessor_toolkits = None

    # Collapse to single copies of each type
    if available_coprocessors:
        available_coprocessors = sorted(list(set(available_coprocessors)))
    if coprocessor_classes:
        coprocessor_classes = sorted(list(set(coprocessor_classes)))
    if coprocessor_toolkits:
        coprocessor_toolkits = sorted(list(set(coprocessor_toolkits)))
    return {
        'available': available_coprocessors,
        'classes': coprocessor_classes,
        'toolkits': coprocessor_toolkits,
    }


def configure_coprocessor(
        queue=None, threads=1, parallel_env=None,
        coprocessor=None, coprocessor_multi="1",
        coprocessor_toolkit=None):
    logger = logging.getLogger(__name__)
    config = read_config()
    mconfig = method_config(config['method'])

    if coprocessor is not None:
        if mconfig['queues']:
            # If coprocessor resource is in Scheduling multiple GPUS...
            # PE as first port of call, do we need a separate way of
            # specifying gpu qty
            if isinstance(coprocessor_multi, int):
                coprocessor_multi = str(coprocessor_multi)
            if coprocessor_multi != '1':
                try:
                    if int(coprocessor_multi) > max_coprocessors(coprocessor):
                        raise BadSubmission(
                            "Unable to provide {} coprocessors for job".format(
                                coprocessor_multi
                            ))

                except ValueError:
                    # Complex coprocessor_multi passed - do not validate
                    pass
                usepe = coprocessor_config(coprocessor).get('uses_pe', False)
                if usepe:
                    try:
                        if usepe not in config['queues'][queue]['parallel_envs']:  # noqa E501
                            raise KeyError()
                    except KeyError:
                        raise BadSubmission(
                            f"uses_pe set but selected queue {queue} does not have PE {usepe} configured")  # noqa E501
                    parallel_env = usepe
                    try:
                        gpus_req = int(coprocessor_multi)
                    except ValueError:
                        raise BadSubmission(
                            "Specified coprocessor_multi argument is a "
                            "complex value but cluster configured with "
                            "'uses_pe' which requires a simple integer"
                        )
                    if gpus_req > threads:
                        if gpus_req > config['queues'][queue]['max_slots']:
                            raise BadSubmission(
                                "More GPUs than queue slots have been "
                                "requested")
                        threads = gpus_req

        if coprocessor_toolkit:
            logger.debug("Looking for coprocessor toolkit")
            logger.debug(":".join((coprocessor, coprocessor_toolkit)))
            try:
                coproc_load_module(coprocessor, coprocessor_toolkit)
            except UnrecognisedModule as e:
                raise BadSubmission(
                    "Unable to load coprocessor toolkit " + str(e)
                )
    elif (
            mconfig['queues']
            and queue is not None
            and queue in config['queues']
            and 'copros' in config['queues'][queue]):
        if mconfig.get('warn_missing_coprocessor', True):
            warnings.warn(
                "Queue with coprocessor defined requested but no "
                "--coprocessor option specified")

    return (threads, parallel_env)
