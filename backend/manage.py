from asyncio import subprocess
import sys
import unittest

import coverage

from flask.cli import FlaskGroup

from app.apps import create_app, db

app = create_app()

cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include="app/*",
    omit=[
        "app/tests/*",
    ],
)

COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """
    Runs the unit tests without test coverage
    """

    tests = unittest.TestLoader().discover("app/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        sys.exit(0)

    else:
        sys.exit(1)


@cli.command()
def cov():
    """
    Runs the unit tests with coverage
    """

    tests = unittest.TestLoader().discover("app/tests", "test*.py")
    results = unittest.TextTestRunner().run(tests)

    if results.wasSuccessful():
        COV.stop()
        COV.save()

        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command
def flake():
    """
    Runs flake8 on the project
    """

    subprocess.run(["flake8", "app"])


if __name__ == "__main__":
    cli()
