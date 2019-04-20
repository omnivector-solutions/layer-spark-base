from pathlib import Path
import re
from time import sleep

from subprocess import check_call

from charmhelpers.core.hookenv import resource_get
from charmhelpers.core.templating import render

from charmhelpers.core.host import chownr

from charms.layer import status


SPARK_HOME = Path('/opt/spark')
SPARK_RELEASE = SPARK_HOME / 'RELEASE'
SPARK_WORK_DIR = Path('/srv/spark/work')
SPARK_LOG_DIR = Path('/var/log/spark')
SPARK_DEFAULTS = SPARK_HOME / 'conf' / 'spark-defaults.conf'
SPARK_ENV_SH = SPARK_HOME / 'conf' / 'spark-env.sh'


def provision_spark_resource():
    """Unpack the Spark tarball resource.
    """

    # Provision spark resource
    spark_tarball = resource_get('spark-tarball')

    if not spark_tarball:
        status.blocked("Could not find resource 'spark-tarball'")
        return

    if SPARK_HOME.exists():
        check_call(['rm', '-rf', str(SPARK_HOME)])

    check_call(['mkdir', '-p', str(SPARK_HOME)])

    check_call(
        ['tar', '-xzf', spark_tarball, '--strip=1', '-C', str(SPARK_HOME)])

    while not SPARK_RELEASE.exists():
        sleep(1)

    return True


def get_spark_version():
    """Return the Spark version.
    """

    with open(str(SPARK_RELEASE), 'r') as f:
        regex = re.compile(r'Spark (\S+)')
        spark_version = re.findall(regex, f.read())[0]
    return spark_version


def init_spark_perms():
    """Set permissions on the things the spark process needs access to.
    """

    # Note: We need to set the standard for what all of the
    # file and directory permissions need to be here.

    # Set spark ownership on the home, log, and work dir
    for directory in [SPARK_HOME, SPARK_LOG_DIR, SPARK_WORK_DIR]:
        chownr(str(directory), 'spark', 'spark', chowntopdir=True)

    # Open up the work dir 777 (do we need to  make it this open?)
    check_call(['chmod', '-R', '777', str(SPARK_WORK_DIR)])


def render_spark_init_config(ctxt=None):
    """Render the spark initial config.
    """

    if ctxt:
        context = ctxt
    else:
        context = {}

    if SPARK_ENV_SH.exists():
        SPARK_ENV_SH.unlink()
    render('spark-base-env.sh', str(SPARK_ENV_SH),
           context=context, perms=0o755)
