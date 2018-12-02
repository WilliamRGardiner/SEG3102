from database.Repository import Repository

class PersistenceValidator():

    NO_FIELD = "N/A"

    def checkExists(cEntity, id):
        session = Repository.Session()
        entity = session.query(cEntity).filter_by(id=id).one_or_none()
        isExists = (entity is not None)
        session.rollback()
        return isExists

    def checkField(errors, cEntity, account, field, value, originalValue=None):
        session = Repository.Session()
        if originalValue is None or (not value == originalValue):
            existing = session.query(cEntity).filter_by(**{field : (value)}).one_or_none()
            if existing is not None:
                errors.append(PersistenceValidator.uniqueConstraintViolation(field, value))
        session.rollback()
        return errors

    def uniqueConstraintViolation(field, value):
        return {"field": field, "msg": "Value, " + value + ", is already in use for " + field}

    def entityDoesNotExist(entity, field, value):
        return {"field": PersistenceValidator.NO_FIELD, "msg": "No " + entity + " exists for " + field + ": " + value}

    def entityActive(entity, entityId):
        return {"field": PersistenceValidator.NO_FIELD, "msg": entity + ": " + entityId + " is still active"}

    def subEntitiesExist(entity, subentity, number):
        return {"field": PersistenceValidator.NO_FIELD, "msg": "Cannot delete " + entity + " with " + str(number) + " " + subentity}

    def activeSubEntitiesExist(entity, subentity, number):
        return {"field": PersistenceValidator.NO_FIELD, "msg": "Cannot delete " + entity + " with " + str(number) + " active " + subentity}

    def linkedDomainNotFoundError(entity, subentity, entityId, subentityId):
        return {"field": PersistenceValidator.NO_FIELD, "msg": subentity + ": " + subentityId + " not found for " + entity + ": " + entityId}
