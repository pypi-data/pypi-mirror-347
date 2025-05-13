from typing import List, Optional
from geovisio.utils import auth, db
from geovisio.utils.annotations import AnnotationCreationParameter, creation_annotation, get_annotation, update_annotation
from geovisio.utils.tags import SemanticTagUpdate
from geovisio.web.utils import accountIdOrDefault
from geovisio.utils.params import validation_error
from geovisio import errors
from pydantic import BaseModel, ValidationError
from uuid import UUID
from flask import Blueprint, current_app, request, url_for
from flask_babel import gettext as _


bp = Blueprint("annotations", __name__, url_prefix="/api")


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>/annotations", methods=["POST"])
@auth.login_required()
def postAnnotation(collectionId, itemId, account):
    """Create an annotation on a picture.

    The geometry can be provided as a bounding box (a list of 4 integers, minx, miny, maxx, maxy) or as a geojson geometry.
    All coordinates must be in pixel, starting from the top left of the picture.

    If an annotation already exists on the picture with the same shape, it will be used.
        ---
        tags:
            - Editing
            - Semantics
        parameters:
            - name: collectionId
              in: path
              description: ID of collection to retrieve
              required: true
              schema:
                type: string
            - name: itemId
              in: path
              description: ID of item to retrieve
              required: true
              schema:
                type: string
        requestBody:
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioPostAnnotation'
        security:
            - bearerToken: []
            - cookieAuth: []
        responses:
            200:
                description: the annotation metadata
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/GeoVisioAnnotation'
    """

    account_id = UUID(accountIdOrDefault(account))

    pic = db.fetchone(
        current_app,
        "SELECT 1 FROM sequences_pictures WHERE seq_id = %(seq)s AND pic_id = %(pic)s",
        {"seq": collectionId, "pic": itemId},
    )
    if not pic:
        raise errors.InvalidAPIUsage(_("Picture %(p)s wasn't found in database", p=itemId), status_code=404)

    if request.is_json and request.json is not None:
        try:
            params = AnnotationCreationParameter(**request.json, account_id=account_id, picture_id=itemId)
        except ValidationError as ve:
            raise errors.InvalidAPIUsage(_("Impossible to create an annotation"), payload=validation_error(ve))
    else:
        raise errors.InvalidAPIUsage(_("Parameter for creating an annotation should be a valid JSON"), status_code=415)

    annotation = creation_annotation(params)

    return (
        annotation.model_dump_json(exclude_none=True),
        200,
        {
            "Content-Type": "application/json",
            "Access-Control-Expose-Headers": "Location",  # Needed for allowing web browsers access Location header
            "Location": url_for(
                "annotations.getAnnotation", _external=True, annotationId=annotation.id, collectionId=collectionId, itemId=itemId
            ),
        },
    )


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>/annotations/<uuid:annotationId>", methods=["GET"])
def getAnnotation(collectionId, itemId, annotationId):
    """Get an annotation

    ---
    tags:
        - Semantics
    parameters:
        - name: collectionId
          in: path
          description: ID of collection
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item
          required: true
          schema:
            type: string
        - name: annotationId
          in: path
          description: ID of annotation
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the annotation metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioAnnotation'
    """
    with db.conn(current_app) as conn:

        annotation = get_annotation(conn, annotationId)
        if not annotation or annotation.picture_id != itemId:
            raise errors.InvalidAPIUsage(_("Annotation %(p)s not found", p=itemId), status_code=404)

        return annotation.model_dump_json(exclude_none=True), 200, {"Content-Type": "application/json"}


class AnnotationPatchParameter(BaseModel):
    """Parameters used to update an annotation"""

    semantics: Optional[List[SemanticTagUpdate]] = None
    """Tags to update on the annotation. By default each tag will be added to the annotation's tags, but you can change this behavior by setting the `action` parameter to `delete`.

    If you want to replace a tag, you need to first delete it, then add it again.

    Like:
[
    {"key": "some_key", "value": "some_value", "action": "delete"},
    {"key": "some_key", "value": "some_new_value"}
]
    """


@bp.route("/collections/<uuid:collectionId>/items/<uuid:itemId>/annotations/<uuid:annotationId>", methods=["PATCH"])
@auth.login_required()
def patchAnnotation(collectionId, itemId, annotationId, account):
    """Patch an annotation

    Note that if the annotation has no associated tags anymore, it will be deleted.
    ---
    tags:
        - Semantics
    parameters:
        - name: collectionId
          in: path
          description: ID of collection
          required: true
          schema:
            type: string
        - name: itemId
          in: path
          description: ID of item
          required: true
          schema:
            type: string
        - name: annotationId
          in: path
          description: ID of annotation
          required: true
          schema:
            type: string
    security:
        - bearerToken: []
        - cookieAuth: []
    responses:
        200:
            description: the annotation metadata
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioAnnotation'
        204:
            description: The annotation was empty, it has been correctly deleted
    """
    if request.is_json and request.json is not None:
        try:
            params = AnnotationPatchParameter(**request.json)
        except ValidationError as ve:
            raise errors.InvalidAPIUsage(_("Impossible to patch annotation, invalid parameters"), payload=validation_error(ve))
    else:
        raise errors.InvalidAPIUsage(_("Parameter for updating an annotation should be a valid JSON"), status_code=415)

    with db.conn(current_app) as conn:

        annotation = get_annotation(conn, annotationId)
        if not annotation or annotation.picture_id != itemId:
            raise errors.InvalidAPIUsage(_("Annotation %(p)s not found", p=itemId), status_code=404)

        a = update_annotation(annotation, params.semantics, account.id)
        if a is None:
            return "", 204
        return a.model_dump_json(exclude_none=True), 200, {"Content-Type": "application/json"}
