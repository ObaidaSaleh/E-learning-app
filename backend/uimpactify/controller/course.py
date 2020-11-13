# packages
from bson.objectid import ObjectId
from bson.errors import InvalidId

# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist

# project resources
from uimpactify.models.courses import Courses
from uimpactify.controller.errors import forbidden

from uimpactify.models.users import Users

from uimpactify.utils.mongo_utils import convert_query, convert_doc, convert_embedded_doc, convert_embedded_query
from uimpactify.controller.errors import unauthorized, bad_request, conflict, not_found
from uimpactify.controller.dont_crash import dont_crash, user_exists

class CoursesApi(Resource):
    """
    Flask-resftul resource for returning db.course collection.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def get(self) -> Response:
        """
        GET response method for all documents in course collection.
        JSON Web Token is required.

        """
        authorized: bool = True #Users.objects.get(id=get_jwt_identity()).access.admin


        if authorized:
            query = Courses.objects()

            fields = {
                'id',
                'name',
                'objective',
                'learningOutcomes',
                'published',
            }

            res = convert_query(query, include=fields)
            return jsonify(res)
        else:
            return forbidden()

    @jwt_required
    @user_exists
    @dont_crash
    def post(self) -> Response:
        """
        POST response method for creating a course.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        """
        authorized: bool = True #Users.objects.get(id=get_jwt_identity()).access.admin
        if authorized:
            data = request.get_json()
            # get the instructor id based off of jwt token identity
            data['instructor'] = get_jwt_identity()
            print(get_jwt_identity())
            try:
                course = Courses(**data).save()
            except ValidationError as e:
                return bad_request(e.to_dict())
            output = {'id': str(course.id)}
            return jsonify(output)
        else:
            return forbidden()


class CourseApi(Resource):
    """
    Flask-resftul resource for returning db.course collection.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def get(self, course_id: str) -> Response:
        """
        GET response method for single documents in course collection.

        :return: JSON object
        """

        course = Courses.objects.get(id=course_id)
        fields = {
            'id',
            'name',
            'objective',
            'learningOutcomes',
            'published',
        }
        return jsonify(convert_doc(course, include=fields))


    @jwt_required
    @user_exists
    @dont_crash
    def put(self, course_id: str) -> Response:
        """
        PUT response method for updating a course.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        """
        data = request.get_json()
        try:
            res = Courses.objects.get(id=course_id).update(**data)
        except ValidationError as e:
            return bad_request(e.message)
        return jsonify(res)


    @jwt_required
    @user_exists
    @dont_crash
    def delete(self, course_id: str) -> Response:
        """
        DELETE response method for deleting single course.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)

        """
        authorized: bool = True #Users.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Courses.objects(id=course_id).delete()
            return jsonify(output)
        else:
            return forbidden()


class CourseByInstructorApi(Resource):
    """
    Flask-resftul resource for returning courses with the same instructor id.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def get(self) -> Response:
        """
        GET response method for single documents in course collection.

        :return: JSON object
        """
        query = Courses.objects(instructor=get_jwt_identity())
        fields = {
            'id',
            'name',
            'objective',
            'learningOutcomes',
            'published',
        }
        values = convert_query(query, fields)
        return jsonify(values)

class CourseEnrollmentApi(Resource):
    """
    Flask-resftul resource for enrolling in courses.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def post(self) -> Response:
        """
        POST response method for enrolling in a course.

        :return: JSON object
        """
        data = request.get_json()
        user_id=get_jwt_identity()

        if Courses.objects(id=data["courseId"], students=ObjectId(user_id)):
            return conflict("You cannot enrol in the same course twice!")

        try:
            enroll = Courses.objects(id=data["courseId"]).update(push__students=ObjectId(user_id))
            if enroll == 0:
                return not_found("404 Error: The requested course does not exist")
        except InvalidId as e:
            print(e.__class__.__name__)
            print(dir(e))
            return bad_request(str(e))
        except ValidationError as e:
            return bad_request(e.message)
        
        output = {'id': user_id}
        return jsonify(output)

class CourseDisenrollmentApi(Resource):
    @jwt_required
    @user_exists
    @dont_crash
    def delete(self, course_id: str) -> Response:
        """
        DELETE response method for disenrolling in a course.

        :return: JSON object
        """
        user_id=get_jwt_identity()
        try:
            disenroll = Courses.objects(id=course_id).update(pull__students=ObjectId(user_id))
            if disenroll == 0:
                return not_found("404 Error: The requested course does not exist")
        except InvalidId as e:
            print(e.__class__.__name__)
            print(dir(e))
            return bad_request(str(e))
        except ValidationError as e:
            return bad_request(e.message)

        output = {'id': user_id}
        return jsonify(output)

class CoursesWithStudentApi(Resource):
    """
    Flask-resftul resource for returning courses containing the same student.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def get(self) -> Response:
        """
        GET response method for single documents in course collection.

        :return: JSON object
        """
        student_id=get_jwt_identity()
        output = Courses.objects(students=student_id)
        fields = { 'id', 'name' }
        converted = convert_query(output, fields)
        return jsonify(converted)


class PublishedCoursesApi(Resource):
    """
    Flask-resftul resource for returning all published courses.

    """
    @dont_crash
    def get(self) -> Response:
        """
        GET response method for all documents in course collection with published=true.

        :return: JSON object
        """
        output = Courses.objects(published=True)
        fields = {
            'id',
            'name',
            'objective'
            }
        embedded = {'instructor': {'name': 'instructor'}}
        converted = convert_embedded_query(output, fields, embedded)
        return jsonify(converted)

class PublishedCourseApi(Resource):
    """
    Flask-resftul resource for returning a specified published courses.

    """
    @dont_crash
    def get(self, course_id: str) -> Response:
        """
        GET response method for a specific course in course collection with published=true.
        Returns a 404 error if the course is not published or doesn't exist.

        :return: JSON object
        """
        try:
            output = Courses.objects.get(id=course_id)
        except DoesNotExist:
            return not_found()
        if output.published == False:
            return not_found()
        fields = {
            'id',
            'name',
            'objective',
            'learningOutcomes'
            }
        embedded = {'instructor': {'name': 'instructor'}}
        converted = convert_embedded_doc(output, fields, embedded)
        return jsonify(converted)


class CourseEndorsementApi(Resource):
    """
    Flask-resftul resource for endorsing courses.

    """
    @jwt_required
    @user_exists
    @dont_crash
    def post(self) -> Response:
        """
        POST response method for endorsing a course.

        :return: JSON object
        """
        data = request.get_json()
        user_id=get_jwt_identity()
        course_id = data["courseId"]

        authorized: bool = Users.objects.get(id=user_id).roles.organization
        if authorized:
            # don't let an organization endorse the same course twice
            if Courses.objects(id=course_id, endorsedBy=ObjectId(user_id)):
                return conflict("You already endorsed this course!")

            # add the organization the course's endorsedBy list
            try:
                endorse = Courses.objects(id=course_id).update(push__endorsedBy=ObjectId(user_id))
                if endorse == 0:
                    return not_found("404 Error: The requested course does not exist")
            except InvalidId as e:
                print(e.__class__.__name__)
                print(dir(e))
                return bad_request(str(e))
            except ValidationError as e:
                return bad_request(e.message)
            
            output = {'id': user_id}
            return jsonify(output)
        else:
            return forbidden()


class CourseEndorsedByApi(Resource):
    """
    Flask-resftul resource for returning a list of organizations endorsing a course.

    """
    @dont_crash
    def get(self, course_id: str) -> Response:
        """
        GET response method a list of organizations endorsing a course.

        :return: JSON object
        """
        try:
            doc = Courses.objects().get(id=course_id)
        except DoesNotExist:
            return not_found("404 Error: The requested course does not exist")
        endorsedBy = getattr(doc, 'endorsedBy')
        return jsonify(endorsedBy)
