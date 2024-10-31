from flask import current_app
import traceback
import app.main.util.exceptions.errors as errors

def register_handlers(api):
    @api.errorhandler(errors.NotFoundError)
    def handle_not_found(error):
        current_app.logger.error(traceback.format_exc())
        current_app.logger.error(str(error))
        return {'message': str(error)}, 404

    @api.errorhandler(errors.AlreadyExistsError)
    def handle_already_exists(error):
        current_app.logger.error(traceback.format_exc())
        return {'message': str(error)}, 409

    @api.errorhandler(errors.BadInputError)
    def handle_bad_input(error):
        current_app.logger.error(traceback.format_exc())
        return {'message': str(error)}, 400

    @api.errorhandler(errors.TokenInvalidError)
    def handle_token_expired(error):
        current_app.logger.error(traceback.format_exc())
        return {'message': str(error)}, 401
