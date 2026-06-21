import datetime

import click

from .config import get_config
from .email import Email
from .firefly import EmailReport
from .setup_logging import config_logger, ERROR_CODES
import sys
import traceback
from time import perf_counter

def handle_uncaught_exception(exc_type,exc_value,exc_traceback):
    tb = traceback.extract_tb(exc_traceback)
    error_filename, lineno, funcname, code_error = tb[-1]
    # TODO: This won't work as db_logger is not a global variable
    db_logger.critical(
            message="Uncaught exception, will terminate.",
            details=dict(
                error_type=str(exc_type),
                error_value=str(exc_value),
                error_line_number=str(lineno),
                error_filename=str(error_filename),
                error_function=str(funcname),
                )
            )
    db_logger.save_log()

sys.excepthook = handle_uncaught_exception

@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--start_date",
    default=f"{datetime.date.today() - datetime.timedelta(days=7)}",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--end_date",
    default=f"{datetime.date.today()}",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
def main(config_file, start_date, end_date):
    start_timer = perf_counter()
    config = get_config(config_file)
    db_logger = config_logger(config=config["logging"])
    db_logger.info(
        message="Starting program",
        details=dict(
            config_file=str(config_file),
            start_date=str(start_date),
            end_date=str(end_date),
            database=config["logging"]["database"],
            )
        )
    db_logger.save_log()
    db_logger.debug(
            message="Config loaded.",
            details=dict(
                duration=(perf_counter() - start_timer),
                ),
            )

    report = EmailReport(
        url=config["firefly"]["url"],
        access_token=config["firefly"]["access_token"],
        start_date=start_date,
        end_date=end_date,
    )
    
    try:
        email_report = report.create_report()
    except Exception as err:
        db_logger.error(
                message="Unable to create report",
                details=dict(
                    traceback=str(err),
                    error_code=4,
                    error_message=ERROR_CODES.get(4,9),
                    ),
                )
        db_logger.save_log()
        sys.exit(4)

    db_logger.debug(
            message="Report created.",
            details=dict(
                duration=(perf_counter() - start_timer),
                ),
            )
    db_logger.save_log()

    email_message = Email(
        email_to=config["email"]["to"],
        email_from=config["email"]["from"],
        subject=f"Firefly Report {start_date.date()} to {end_date.date()}",
        body=email_report,
        smtp_server=config["email"]["server"],
        smtp_port=config["email"]["port"],
        smtp_starttls=config["email"]["starttls"],
        smtp_user=config["email"]["user"],
        smtp_password=config["email"]["password"],
        smtp_authentication=config["email"]["authentication"],
    )

    #email_message.send_email()

    db_logger.info(
            message="Report sent, complete!",
            details=dict(
                duration=(perf_counter() - start_timer),
                ),
            )
    db_logger.save_log()
    breakpoint()


if __name__ == "__main__":
    main()
