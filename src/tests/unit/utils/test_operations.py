import pytest
from django.db import transaction
from django.test import TestCase

from queenbees.core.content import models as content_models
from queenbees.core.utils import operations


class SomeException(Exception):
    pass


class TestOperations(TestCase):
    @operations.operation(atomic=False)
    def operation(self, side_effect: Exception | None) -> bool:
        if side_effect:
            raise side_effect

        return True

    def test_operations_happy_path(self) -> None:
        with self.assertLogs(level="DEBUG") as logs:
            assert self.operation(None)

            assert logs.output[0].startswith("DEBUG:")
            assert logs.output[1].startswith("DEBUG:")

    def test_operations_failed(self) -> None:
        with self.assertLogs(level="DEBUG") as logs:
            with self.assertRaises(SomeException):
                self.operation(SomeException())

            assert logs.output[0].startswith("DEBUG:")
            assert logs.output[1].startswith("ERROR:")


class TestAtomicOperations:
    @operations.operation(atomic=True)
    def operation(self, side_effect: Exception | None, article: content_models.Article) -> bool:
        article.name = "updated"
        article.save()

        if side_effect:
            raise side_effect

        return True

    @pytest.mark.django_db
    def test_operation_happy_path(self, article: content_models.Article) -> None:
        self.operation(None, article)

        article_from_db = content_models.Article.objects.all().first()
        assert article_from_db.name == "updated"

    @pytest.mark.django_db
    def test_operation_failed(self, article: content_models.Article) -> None:
        initial_name = article.name

        with pytest.raises(SomeException), transaction.atomic():
            self.operation(SomeException(), article)

        article_from_db = content_models.Article.objects.all().first()
        assert article_from_db.name == initial_name

    @pytest.mark.django_db
    def test_operation_transaction_failed(self, article: content_models.Article) -> None:
        initial_name = article.name

        class Rollback(Exception):
            pass

        with pytest.raises(Rollback), transaction.atomic():
            self.operation(None, article)

            raise Rollback()

        article_from_db = content_models.Article.objects.all().first()
        assert article_from_db.name == initial_name
