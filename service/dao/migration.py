import alembic.config


def upgrade_db():
    """
    执行数据库升级
    """
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
