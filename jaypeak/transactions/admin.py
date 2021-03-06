from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_security import current_user

from .models import User, Role, Transaction, RecurringTransaction
from ..extensions import admin


class UserAdmin(ModelView):
    column_display_pk = True
    column_searchable_list = ('id', 'yodlee_user_id', 'email')
    column_list = ('id', 'yodlee_user_id', 'email')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('transaction.login', next=request.url))

    def create_model(self, form):
        user = super(UserAdmin, self).create_model(form)
        user.save()
        return user


class RoleAdmin(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('transactions.login', next=request.url))


class TransactionAdmin(ModelView):
    column_display_pk = True
    column_searchable_list = ('description', 'amount', 'account_id')
    column_list = ('id', 'description', 'amount',
                   'date', 'account_id', 'user')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('transactions.login', next=request.url))


class MyInlineModelForm(InlineFormAdmin):
    form_columns = ('id', 'description', 'amount', 'date', 'account_id', 'user')  # nopep8


class RecurringTransactionAdmin(ModelView):
    column_display_pk = True
    inline_models = (MyInlineModelForm(Transaction),)

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('transactions.login', next=request.url))


def configure_transactions_admin(app, db):
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(TransactionAdmin(Transaction, db.session))
    admin.add_view(RecurringTransactionAdmin(RecurringTransaction, db.session))  # nopep8
