from charms.reactive import (
    when,
    when_not,
    set_flag,
)

from charmhelpers.core.host import (
    adduser,
)

from charmhelpers.core import unitdata

from charmhelpers.core.hookenv import log

from charms.layer import status

from charms.layer.spark_base import (
    SPARK_WORK_DIR,
    SPARK_LOG_DIR,
    get_spark_version,
    provision_spark_resource,
    init_spark_perms,
    render_spark_env_sh,
)


KV = unitdata.kv()


@when('apt.installed.scala',
      'apt.installed.openjdk-8-jre-headless')
@when_not('spark.apt.deps.available')
def apt_deps_available():
    """Spark deps available.
    """
    set_flag('spark.apt.deps.available')


@when_not('spark.user.available')
def create_spark_user():
    """Create spark user.
    """
    adduser('spark', system_user=True)
    set_flag('spark.user.available')


@when_not('spark.dirs.available')
def create_spark_dirs():
    """Create spark log and work directories.
    """
    for directory in [SPARK_WORK_DIR, SPARK_LOG_DIR]:
        if not directory.exists():
            directory.mkdir(parents=True)
    set_flag('spark.dirs.available')


@when('spark.apt.deps.available')
@when_not('spark.resource.available')
def provision_spark():
    """Proivision spark resource.
    """
    log("PROVISIONING SPARK RESOURCE")
    status.maint("PROVISIONING SPARK RESOURCE")

    spark_resource_provisioned = provision_spark_resource()

    if not spark_resource_provisioned:
        status.blocked("TROUBLE PROVISIONING SPARK RESOURCE, PLEASE DEBUG")
        log("TROUBLE PROVISIONING SPARK RESOURCE, PLEASE DEBUG")
        return

    log("SPARK RESOURCE {} ready".format(get_spark_version()))
    status.maint("SPARK RESOURCE {} ready".format(get_spark_version()))

    KV.set('spark_version', get_spark_version())
    set_flag('spark.resource.available')


@when('spark.user.available',
      'spark.dirs.available',
      'spark.resource.available')
@when_not('spark.base.config.available')
def render_spark_sane_config():
    render_spark_env_sh(template='spark-base-env.sh')
    set_flag('spark.base.config.available')


@when('spark.base.config.available')
@when_not('spark.permissions.available')
def apply_perms():
    init_spark_perms()
    set_flag('spark.permissions.available')


@when('spark.permissions.available')
@when_not('spark.base.available')
def set_spark_base_complete():
    set_flag('spark.base.available')
