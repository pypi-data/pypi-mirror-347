from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q, F
from ..utils import translate as _
from .base import BaseModelWitDateNotFiscalDelete, BaseModelContentType, BaseStructure
from .choices import Choices
from django.contrib.auth import get_user_model

User = get_user_model()

class Workflow(BaseModelWitDateNotFiscalDelete):
    name = models.CharField(max_length=100, verbose_name="workflow_name")
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    content_type_wf = models.ForeignKey(ContentType, verbose_name=_('related model'), on_delete=models.CASCADE)
    transition_status = models.ForeignKey(Choices, verbose_name=_('transition status'), on_delete=models.CASCADE,
                                         limit_choices_to=Q(choice_title="transition_status"))

    def __str__(self):
        return f'{self.name}--{self.content_type_wf.model}'

    @property
    def urls(self):
        urls = {
            'create_url': f'/workflows/{self.id}/{self.name}/create/1',
            'update_url': f'/workflows/{self.id}/{self.name}/update/{self.pk}',
            'delete_url': f'/workflows/{self.id}/{self.name}/delete/{self.pk}',
            'get_url': f'/workflows/{self.id}/{self.name}/get/{self.pk}',
        }
        url = urls.get('create_url')

        return url, urls


class WorkflowState(BaseModelWitDateNotFiscalDelete):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="workflow")
    name = models.CharField(max_length=100, verbose_name=_("WorkflowState_name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    can_transition_to = models.ManyToManyField('self', blank=True, verbose_name=_("can_transition_to"))
    next_state = models.ForeignKey('self', on_delete=models.CASCADE, related_name="self_next_state",
                                   verbose_name=_("next_state"), blank=True, null=True)
    previous_state = models.ForeignKey('self', on_delete=models.CASCADE, related_name="self_previous_state",
                                       verbose_name=_("previous_state"), blank=True, null=True)
    form_struct = models.JSONField(verbose_name=_("form_struct"), default=list)
    extra_data = models.JSONField(verbose_name=_("extra_data"), default=dict, null=True, blank=True)
    order_number = models.IntegerField(verbose_name=_("order_number"), default=0)
    get_single_form = models.BooleanField(default=False, verbose_name=_("get_single_form"))

    def __str__(self):
        return f'{self.id}:{self.name}'

    def get_transition_options(self, user):
        accessible_states = []
        for state in self.can_transition_to.all():
            if user.has_perm('can_transition', state):
                accessible_states.append(state)
            else:
                raise PermissionDenied("You don't have permission to auto-transition states.")
        return accessible_states

    def is_first_state(self):
        first_state = WorkflowState.objects.filter(workflow_id=self.workflow.id).order_by('order_number').first()
        return first_state and first_state.id == self.id, first_state

    def is_last_state(self):
        last_state = WorkflowState.objects.filter(workflow_id=self.workflow.id).order_by('-order_number').first()
        return last_state and last_state.id == self.id, last_state

    def get_next_state(self):
        return WorkflowState.objects.filter(
            workflow=self.workflow,
            order_number__gt=self.order_number
        ).annotate(distance=F('order_number') - self.order_number).order_by('distance').first()

    def get_previous_state(self):
        return WorkflowState.objects.filter(
            workflow=self.workflow,
            order_number__lt=self.order_number
        ).annotate(distance=self.order_number - F('order_number')).order_by('distance').first()

    def auto_transition(self, direction='next'):
        if direction == 'next':
            func_res = self.call_transition_method('next_state_func')
            return func_res if func_res else (None if self.is_last_state()[0] else self.get_next_state().id)

        elif direction == 'previous':
            func_res = self.call_transition_method('previous_state_func')
            return func_res if func_res else (None if self.is_first_state()[0] else self.get_previous_state().id)

    @staticmethod
    def execute_action_from_function(method, **kwargs):
        method_func = globals()[method]
        if callable(method_func):
            return method_func(state=kwargs.pop('state'), **kwargs)

    def call_transition_method(self, func_name=None, **kwargs):
        if func_name:
            check_transition_method = self.extra_data.get(func_name, {})
            if check_transition_method:
                method_func = self.execute_action_from_function(check_transition_method, state=self, **kwargs)
                return method_func
        return dict()

    def check_transition(self, *args, **kwargs):
        res = dict()
        can_transition_to_names = list(
            self.can_transition_to.values_list('name', flat=True)) if self.can_transition_to else []

        target_state = kwargs.get('target_state')
        state_choices = kwargs.get('wf_form', {}).fields_schema.get('last_state_id', {}).get('choices')
        current_choice = next(
            (choice for choice in state_choices if
             target_state and choice['id'] == int(target_state) and choice['enable'] == 'True'),
            None
        )
        if target_state:
            if current_choice and current_choice.get('name') in can_transition_to_names or int(
                    target_state) == kwargs.get('current_state').id:
                res = {'public_data': {'message': 'ok'}}
            else:
                res = {'public_data': {'errors': f'you dont have access to state ({target_state})'}}
        func_res = self.call_transition_method(func_name='check_transition_func', **kwargs)
        if func_res:
            res['public_data'].update(func_res)
        return res


class WorkflowHistory(BaseModelContentType):
    TYPE = (
        ('update', _('Update')),
        ('create', _('Create'))
    )
    workflow = models.ForeignKey(Workflow, on_delete=models.DO_NOTHING, related_name="workflow_histories")
    last_state = models.ForeignKey(WorkflowState, on_delete=models.DO_NOTHING, related_name="state_histories",
                                   null=True, blank=True)
    action_type = models.CharField(max_length=100, choices=TYPE, verbose_name=_("action_type")
                                   ,default='update', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_histories",
                             verbose_name=_("creator user"))
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_histories",
                                verbose_name=_("assign to user"), null=True, blank=True)
    additional_data = models.JSONField(default=dict, blank=True, verbose_name=_("additional data"))
    description = models.CharField(max_length=255, verbose_name=_("description"), null=True, blank=True)
    deadline = models.DateTimeField(verbose_name=_("deadline"), null=True, blank=True)

    @staticmethod
    def get_allowed_states(latest_history, workflow_id):
        if latest_history:
            all_states = list(latest_history.workflow.workflow.values('id', 'name', 'order_number'))
            tran_status = latest_history.workflow.transition_status.choice_value
            last_state = latest_history.last_state
        else:
            all_states = list(
                WorkflowState.objects.filter(workflow__id=workflow_id).values('id', 'name', 'order_number'))
            last_state = WorkflowState.objects.filter(workflow__id=workflow_id).order_by('order_number').first()
            tran_status = last_state.workflow.transition_status.choice_value
        all_states.sort(key=lambda x: x['order_number'])

        allowed_states = {state['id']: state for state in
                          last_state.can_transition_to.values('id', 'name', 'order_number')}


        def calculate_enable(state):
            if tran_status == "enable":
                return 'True' if state['id'] in allowed_states else 'False'
            elif tran_status == "next_enable":
                return 'True' if state['id'] in allowed_states and state[
                    'order_number'] > last_state.order_number else 'False'
            elif tran_status == "previous_enable":
                return 'True' if state['id'] in allowed_states and state[
                    'order_number'] < last_state.order_number else 'False'
            return 'False'

        final_states = [
            {**state,   'verbose_name': _(state['name']), 'enable': calculate_enable(state)}
            for state in all_states
        ]

        return final_states


    @classmethod
    def get_serializer(cls, struct_name='default', method='get', **kwargs):

        serializer_name = cls.serializer_name(method, struct_name)
        struct_objects = kwargs.pop('struct_object', None)

        if serializer_name not in cls.serializer_classes().keys():
            serializer_base_class = BaseStructure.get_serializer_base_class(struct_name)

            return super()._get_model_serializer(struct_name=struct_name, method=method,
                                                 serializer_base_class=serializer_base_class, **kwargs)
        return super().get_serializer(method=method, struct_name=struct_name, **kwargs)

    def __str__(self):
        return f'{self.last_state} : {self.description}'

    def save(self, *args, **kwargs):
        if not self.action_type:
            self.action_type = 'create'
        super().save(*args, **kwargs)
