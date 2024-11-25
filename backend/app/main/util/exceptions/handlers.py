import logging
import traceback

import app.main.util.exceptions.errors as errors

logger = logging.getLogger("errors")


def register_handlers(api):
    @api.errorhandler(errors.NotFoundError)
    def handle_not_found(error):
        logger.debug(traceback.format_exc())
        output = {"message": str(error)}, 404
        logger.error(output)
        return output

    @api.errorhandler(errors.AlreadyExistsError)
    def handle_already_exists(error):
        logger.debug(traceback.format_exc())
        output = {"message": str(error)}, 409
        logger.error(output)
        return output

    @api.errorhandler(errors.BadInputError)
    def handle_bad_input(error):
        logger.debug(traceback.format_exc())
        output = {"message": str(error)}, 400
        logger.error(output)
        return output

    @api.errorhandler(errors.TokenInvalidError)
    def handle_token_expired(error):
        logger.debug(traceback.format_exc())
        output = {"message": str(error)}, 401
        logger.error(output)
        return output

    @api.errorhandler(errors.UnavailableError)
    def handle_unavailable(error):
        logger.debug(traceback.format_exc())
        output = {"message": str(error)}, 503
        logger.error(output)
        return output
