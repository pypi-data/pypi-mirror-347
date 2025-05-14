from typing import Any

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import JSONField, Model
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
    OneToOneField,
    OneToOneRel,
)
from fastapi import HTTPException
from pydantic import BaseModel

from fango.adapters.types import PK
from fango.log import log_params
from fango.schemas import AURAdapter, CRUDAdapter
from fango.utils import get_model_field_safe

__all__ = ["PydanticAdapter"]

ForwardRel = ForeignKey | OneToOneField | OneToOneRel
MultipleRel = ManyToOneRel | ManyToManyField | ManyToManyRel


class AdapterError(Exception):
    pass


class PydanticAdapter(Model):
    """
    A base class for creating Django model instances from Pydantic schemas.

    """

    @classmethod
    @sync_to_async(thread_sensitive=False)
    @transaction.atomic
    def save_from_schema(cls, schema_instance: BaseModel, pk: PK | None = None) -> Model:
        """
        Creates or updates a Django model instance from a Pydantic schema.

        """
        try:
            return _save_orm_instance(cls, schema_instance, pk=pk)
        except (ObjectDoesNotExist, ValidationError) as exc:
            raise HTTPException(status_code=400, detail=getattr(exc, "message", str(exc)))

    class Meta:
        abstract = True


@log_params("PoetryAdapter")
def _save_orm_instance(
    model: type[Model],
    schema_instance: BaseModel,
    remote_field: ForwardRel | MultipleRel | None = None,
    rel_pk: PK | None = None,
    pk: PK | None = None,
) -> Model:
    """
    Adapts data from a Pydantic schema instance to a Django model instance.

    """
    instance = _get_or_create_instance(model, remote_field, rel_pk, pk)
    handlers, rel_handlers = _get_handlers(instance, model, schema_instance)

    for handler, args in handlers:
        handler(*args)

    instance.clean()
    instance.save()

    for rel_handler, args in rel_handlers:
        rel_handler(*args)

    return instance


def _get_or_create_instance(
    model: type[Model],
    remote_field: ForwardRel | MultipleRel | None = None,
    rel_pk: PK | None = None,
    pk: PK | None = None,
):
    """
    Get or create Django ORM instance of object with actual data.

    """
    relation = {}

    if remote_field and rel_pk is not None:
        if isinstance(remote_field, ForeignKey | OneToOneField):
            relation[remote_field.get_attname()] = rel_pk

        elif isinstance(remote_field, OneToOneRel):
            if remote_instance := remote_field.related_model.objects.filter(pk=rel_pk).first():
                relation[remote_field.name] = remote_instance
            else:
                relation[remote_field.name] = None

    if instance := model.objects.filter(pk=pk).first():
        for attr, value in relation.items():
            setattr(instance, attr, value)
    else:
        instance = model(pk=pk, **relation)

    return instance


def _get_handlers(instance: Model, model: type[Model], schema_instance: BaseModel) -> tuple[list, list]:
    """
    Get handler for each field in schema.

    """
    handlers, rel_handlers = [], []

    for key, value in schema_instance:
        if isinstance(getattr(model, key), property):
            continue

        field = get_model_field_safe(model, key)
        args = (instance, field, key, value)

        if isinstance(field, OneToOneRel):
            rel_handlers.append((_handle_forward_relation, args))

        elif isinstance(field, ForwardRel):
            handlers.append((_handle_forward_relation, args))

        elif isinstance(field, MultipleRel):
            rel_handlers.append((_handle_multiple_relation, args))

        elif isinstance(field, JSONField) and isinstance(value, BaseModel):
            handlers.append((setattr, (instance, key, value.model_dump(mode="json"))))

        else:
            handlers.append((setattr, (instance, key, value)))

    return handlers, rel_handlers


@log_params("PoetryAdapter")
def _handle_forward_relation(instance: Model, field: ForwardRel, key: str, value: Any) -> None:
    """
    Assigns a related object or ID to a ForeignKey and OneToOne field in the instance of a model.

    """
    setattr(instance, key, _get_or_create_relation(instance, field, key, value))


@log_params("PoetryAdapter")
def _handle_multiple_relation(instance: Model, field: MultipleRel, key: str, value: Any) -> None:
    """
    Manages ManyToOne and ManyToMany relationship for model instances.

    """
    relation_set = getattr(instance, key)

    if value is None:
        relation_set.set([])

    elif isinstance(value, CRUDAdapter):
        _handle_crud_adapter(instance, field, key, value)

    elif isinstance(value, AURAdapter):
        _handle_aur_adapter(instance, field, key, value)

    elif isinstance(value, list):
        data = []
        for item in value:
            data.append(_get_or_create_relation(instance, field, key, item))

        relation_set.set(data)
    else:
        raise AdapterError


@log_params("PoetryAdapter")
def _get_or_create_relation(instance: Model, field: ForwardRel | MultipleRel, key: str, value: Any) -> Model | None:
    """
    Get or create relation model instance.

    """
    if value is None:
        return None

    elif key.endswith("_id"):
        return value

    elif isinstance(value, BaseModel):
        rel_pk = None

        if isinstance(field, ForwardRel):
            if rel := getattr(instance, key, None):
                rel_pk = rel.pk

        elif isinstance(field, MultipleRel):
            rel_pk = getattr(value, "id", None)

        rel_instance = _save_orm_instance(
            model=field.related_model,
            schema_instance=value,
            remote_field=field.remote_field,
            rel_pk=instance.pk,
            pk=rel_pk,
        )
        try:
            getattr(instance, field.name).add(rel_instance)
        except AttributeError:
            setattr(instance, field.name, rel_instance)

        return rel_instance

    elif isinstance(value, Model):
        value.clean()
        value.save()

        try:
            getattr(instance, field.name).add(value)
        except AttributeError:
            setattr(instance, field.name, value)

        return value

    elif isinstance(value, PK):
        return field.related_model.objects.get(pk=value)

    else:
        raise AdapterError


@log_params("PoetryAdapter")
def _handle_crud_adapter(instance: Model, field: MultipleRel, key: str, value: Any) -> None:
    """
    Manages CRUD adapter.

    """
    relation_set = getattr(instance, key)

    for item in value.create:
        if item.id:
            raise ValidationError(f"Attribute {key}.create data has id.")

        _get_or_create_relation(instance, field, key, item)

    for item in value.update:
        if not item.id:
            raise ValidationError(f"Attribute {key}.update data has no id.")

        _get_or_create_relation(instance, field, key, item)

    for pk in value.delete:
        relation = relation_set.get(pk=pk)
        relation.delete()


@log_params("PoetryAdapter")
def _handle_aur_adapter(instance: Model, field: MultipleRel, key: str, value: Any) -> None:
    """
    Manages AURAdapter.

    """
    relation_set = getattr(instance, key)

    for pk in value.add:
        relation_set.add(relation_set.model.objects.get(pk=pk))

    for item in value.update:
        if not item.id:
            raise ValidationError(f"Attribute {key}.update data has no id.")

        _get_or_create_relation(instance, field, key, item)

    for pk in value.remove:
        if relation_set.__class__.__name__ == "ManyRelatedManager":
            relation_set.remove(relation_set.model.objects.get(pk=pk))
        elif relation_set.__class__.__name__ == "RelatedManager":
            relation = relation_set.get(pk=pk)
            relation.delete()
        else:
            raise AdapterError

    instance.clean()
    instance.save()
