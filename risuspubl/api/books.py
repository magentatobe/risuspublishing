#!/home/kmfahey/Workspace/NuCampFolder/Python/2-SQL/week3/venv/bin/python3

from werkzeug.exceptions import NotFound

from datetime import date

from flask import abort, Blueprint, jsonify, request, Response

from risuspubl.api.commons import *
from risuspubl.api.endpfact import delete_class_obj_by_id_factory, update_class_obj_by_id_factory
from risuspubl.dbmodels import *


blueprint = Blueprint('books', __name__, url_prefix='/books')


@blueprint.route('', methods=['GET'])
def index():
    """
    Implements a GET /books endpoint. All rows in the books table are loaded
    and output as a JSON list.

    :return:    A flask.Response object.
    """
    try:
        result = [book_obj.serialize() for book_obj in Book.query.all()]
        return jsonify(result) # return JSON response
    except Exception as exception:
        status = 400 if isinstance(exception, ValueError) else 500
        return (Response(f"{exception.__class__.__name__}: {exception.args[0]}", status=status)
                if len(exception.args) else abort(status))


@blueprint.route('/<int:book_id>', methods=['GET'])
def show_book(book_id: int):
    """
    Implements a GET /books/<id> endpoint. The row in the books table with the
    given book_id is loaded and output in JSON.

    :book_id: The book_id of the row in the books table to load and
              display.
    :return:  A flask.Response object.
    """
    try:
        book_obj = Book.query.get_or_404(book_id)
        return jsonify(book_obj.serialize())
    except Exception as exception:
        if isinstance(exception, NotFound):
            raise exception from None
        status = 400 if isinstance(exception, ValueError) else 500
        return (Response(f"{exception.__class__.__name__}: {exception.args[0]}", status=status)
                if len(exception.args) else abort(status))


# A Create endpoint is deliberately not implemented, because without
# a way to specify the author or authors to attach the book to, no
# entry in the authors_books table would be created and the book
# would an orphan in the database. /authors/<author_id>/books and
# /authors/<author1_id>/<author2_id>/books already accept Create actions and
# when done that way associations with an author or authors can be created
# appropriately.


book_by_id_updater = update_class_obj_by_id_factory(Book, 'book_id')


@blueprint.route('/<int:book_id>', methods=['PATCH', 'PUT'])
def update_book_by_id(book_id: int):
    """
    Implements a PATCH /books/<id> endpoint. The row in the books table with
    that book_id is updated from the CGI parameters.

    :book_id: The book_id of the row in the books table to update.
    :return:  A flask.Response object.
    """
    return book_by_id_updater(book_id, request.json)


book_by_id_deleter = delete_class_obj_by_id_factory(Book, 'book_id')


@blueprint.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    """
    Implements a DELETE /books/<id> endpoint. The row in the books table with
    that book_id is deleted.

    :book_id: The book_id of the row in the books table to delete.
    :return:  A flask.Response object.
    """
    return book_by_id_deleter(book_id)
