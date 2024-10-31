import app.main.util.exceptions.errors as errors

def register_handlers(api):
    @api.errorhandler(errors.NotFoundError)
    def handle_not_found(error):
        return {'message': error.message}, 404

    @api.errorhandler(errors.AlreadyExistsError)
    def handle_already_exists(error):
        return {'message': error.message}, 409

    @api.errorhandler(errors.BadInputError)
    def handle_bad_input(error):
        return {'message': error.message}, 400

    @api.errorhandler(rerors.TokenInvalidError)
    def handle_token_expired(error):
        return {'message': error.message}, 401
