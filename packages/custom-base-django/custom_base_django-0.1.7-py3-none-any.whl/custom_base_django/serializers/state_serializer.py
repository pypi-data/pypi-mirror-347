from os import access
from django.apps import apps
from ..models.workflow import WorkflowState
from ..models.base import CustomGenericRelation

class StateSerializer:
    workflow_state:WorkflowState = None
    nested_serializer_classes= dict()
    serializers = list()

    @staticmethod
    def get_name(struct_name, method):
        return

    @classmethod
    def set_nested_serializers(cls, state, method="get"):
        # _dict = self.workflow_state.f
        _dict = {"choice": {"model": "custom_base_django.choice", "to_field": "pk", "access_list":
                {[{"groups":[], "users":[], "access_mode":{"readonly":[], "drop":[], "hidden":[], "required":[]}, "nesteds":{"nested1":{"readonly":[], "drop":[], "hidden":[], "required":[]}}}]}},
                 "product": { }
                 }
        _access = {"choice"}
        for key, item in _dict.items():
            app_label, model_name = item.pop("model","").split(".")
            model = apps.get_model(app_label, model_name)
            class_serializer = model.get_serializer(method, item.get("struct_name", "default"))
            class_serializer.access_list = item.get("access_list", [])
            cls.nested_serializer_classes[key] = {"queryset": CustomGenericRelation(model,**item),
                                                  "class_serializer": class_serializer}

    def __init__(self, pk=None, user=None, data=None):
        self.pk = pk
        self.serializers = list()
        self.errors = {}
        self._data = data


    def run_validation(self, data):
        _errors = {}
        self.serializers = list()
        for key, item in self.nested_serializer_classes.items():
            instances = item['queryset']
            class_serializer = item['class_serializer']
            _data = data.get(key)
            i = 0
            _serializer_errors = dict()
            for instance_data in _data:
                pk_field = class_serializer.pk_field
                if instance_data.get(pk_field) and not self.pk:
                    _serializer_errors.update({"invalid_data_pk": f"pk not valid for create request!!"})
                    continue
                if not instance  and instance_data.get(pk_field):
                    _serializer_errors.update({"invalid_data_pk": f"This data has invalid pk for this request ({instance_data[pk_field]})!!"})
                    continue
                instance = instances.filter(**{pk_field: instance_data[pk_field]}) if instance_data.get(
                    class_serializer.pk_field) else None
                _serializer = class_serializer(instance=instance, data=instance_data, )
                if _serializer.is_valid():
                    self.serializers.append(_serializer)
                else:
                    _serializer_errors.update({i: {'validation': _serializer._errors}})
                self.serializers.append(_serializer)

                i += 1
            if _serializer_errors:
                _errors.update({key: _serializer_errors})

        if _errors:
            self.errors = _errors
            # raise ValidationError(_errors)
        self.data = data
        return data

    def is_valid(self):
        if not self.serializers:
            self.run_validation(self._data)
        return not self.errors

    def to_representation(self, **kwargs):
      data = {}
      for key in self.nested_serializer_classes.keys():
          instances = self.nested_serializer_classes[key]['queryset'].all()
          serializer_class = self.nested_serializer_classes[key]['class_serializer']
          data[key] = list()
          for instance in instances:
              serializer = serializer_class(instance=instance)
              data[key].append(serializer.data)
      return data

    def save(self, **kwargs):
        if self.is_valid():
            for serializer in self.serializers:
                serializer.save(**kwargs)

















