# pylint: disable=too-few-public-methods
"""A collection of classes to transform an annotation task into as ML task"""
from abc import ABC, abstractmethod
from typing import List, Iterable, Union
from collections import Counter

from .models import Document, Entity, Task
from .utils import SoftDeleteSet


class Transformer(ABC):
    """A helper class to transform an annotation task into an ML task."""

    @abstractmethod
    def transform(self, task: Task):
        """The actual transformation."""
        raise NotImplementedError()


class Pipeline:
    """Chain several `Transformer` together.

    Attributes
    ----------
    transformers: List[Transformer]
        A list of transformers to chain together
    """

    def __init__(self, transformers: List[Transformer]):
        self.transformers = transformers

    def transform(self, task: Union[Task, List[Document]]):
        """Chain transformers one after another

        Parameters
        ----------
        task : Union[Task, List[Document]]
            The task/documents to transform.

        Returns
        -------
        task: Union[Task, List[Document]]
            The transformed task/documents.
        """
        for transformer in self.transformers:
            task = transformer.transform(task)
        return task


class Filter(Transformer):
    """Filter annotations from a Task or Document.

    The annotations filtered out are not really deleted but rather they are
    marked with a `deleted = True` attribute.

    Attributes
    ----------
    include_fn: Callable[Union[Task, Document], Union[Task | Document]]
        A function specifying which annotations to keep.
    exclude: Callable[Task, Task]
        A function specifying which annotations to filter out.
    """

    def __init__(
        self,
        include_annotation_fn=None,
        exclude_annotation_fn=None,
        include_document_fn=None,
        exclude_document_fn=None
    ):
        self.include_annotation_fn = include_annotation_fn
        self.exclude_annotation_fn = exclude_annotation_fn
        self.include_document_fn = include_document_fn
        self.exclude_document_fn = exclude_document_fn

    def transform(self, task: Task):
        """Filter annotations from a Task or Document.

        Parameters
        ----------
        task : Union[Task, Document, List[Document]]
            The task/documents to filter.

        Returns
        -------
        task: Union[Task, SoftDeleteSet[Document]]
            The filtered task/documents.
        """
        if isinstance(task, Task):
            documents = task.documents
        elif isinstance(task, Document):
            documents = SoftDeleteSet(task)
        elif hasattr(task, '__len__'):
            documents = SoftDeleteSet(task)
        else:
            raise ValueError(f"{type(task)} is not supported")
        for doc in documents:
            if ((self.exclude_document_fn is not None) and
                    self.exclude_document_fn(doc)):
                documents.remove(doc)
                doc.corpus.remove(doc)
            if ((self.include_document_fn is not None) and
                    (not self.include_document_fn(doc))):
                documents.remove(doc)
                doc.corpus.remove(doc)
            for a in doc.annotations:
                if ((self.exclude_annotation_fn is not None) and
                        self.exclude_annotation_fn(a)):
                    a.document.remove(a)
                if ((self.include_annotation_fn is not None) and
                        (not self.include_annotation_fn(a))):
                    a.document.remove(a)
        return task


class BinaryTransformer(Transformer):
    """Transform a task into a binary classification problem.

    Parameters
    ----------
    pos_labels: List[Entity]
        The entities to classify as positive. All other entities will be
        classified as negative.
    """

    def __init__(self, pos_labels: List[Entity]):
        self.positive = pos_labels

    def transform(self, task: Task):
        """The actual transformation.

        Parameters
        ----------
        task: Task
            The task to transform.

        Returns
        -------
        texts: List[str]
            The content of the documents.
        labels: List[int], {0, 1}
            The classification of the documents.
        """
        texts, labels = [], []
        for doc in task.documents:
            if len(doc.annotations) > 0:
                texts.append(doc.content)
                labels.append(max(l in doc.entities for l in self.positive))
        return texts, labels


class MultiClassTransformer(Transformer):
    """Transform a task into a multi-class classification problem."""

    def transform(
        self,
        task: Task,
        strategy='latest',
        ignore=None,
        keep_ids=False
    ):
        """The actual transformation of the task into a multi-class problem.

        Parameters
        ----------
        task: Task
            The task to transform.

        Returns
        -------
        texts: List[str]
            The content of the documents.
        labels: List[str]
            The classification of the documents.
        """
        if strategy not in ('latest', 'majority'):
            raise NotImplementedError(f'{strategy} is not a valid strategy.')
        if ignore is None:
            ignore = []
        texts, labels, doc_ids = [], [], []
        for doc in task.documents:
            aa = [a for a in doc.annotations if a.task == task]
            aa = [a for a in aa if a.entity not in ignore]
            if len(aa) > 0:
                annotations = sorted(aa, key=lambda a: a.created, reverse=True)
                doc_ids.append(doc.id)
                texts.append(doc.content)
                labels.append(annotations[0].entity.name)
        if keep_ids:
            return doc_ids, texts, labels
        return texts, labels


class MultiLabelTransformer(Transformer):
    """Transform a task into a multi-label classification problem."""

    def transform(self, task: Task, strategy='keep-all'):
        """Transforms the task into a multi-label classification problem.

        Parameters
        ----------
        task: Task
            The task to transform.
        strategy: str, {'keep-all', 'keep-last-by-annotator'}
            The strategy to use for label creation.

        Returns
        -------
        texts: List[str]
            The content of the documents.
        labels: List[dict]
            The classification of the documents.
        """
        if strategy not in ('keep-all', 'keep-last-by-annotator'):
            raise NotImplementedError(f'{strategy} is not a valid strategy.')
        texts, labels = [], []
        # pylint: disable=too-many-nested-blocks
        for doc in task.documents:
            if len(doc.annotations) > 0:
                texts.append(doc.content)
                if strategy == 'keep-last-by-annotator':
                    d = {}
                    for a in doc.annotations:
                        try:
                            if d[a.annotator.id].created > a.created:
                                d[a.annotator.id] = a
                        except KeyError:
                            d[a.annotator.id] = a
                    labels.append({v.entity.name for k, v in d.items()})
                elif strategy == 'keep-all':
                    labels.append({e.name for e in doc.entities})
                else:
                    raise NotImplementedError("This strategy does not exist.")
        return texts, labels


class Sequence2SequenceTransformer(Transformer):
    """Transform a task into a sequence-to-sequence classification problem.

    Attributes
    ----------
    tokenizer: Tokenizer
        The tokenizer to use to split the content of each documents into a
        sequence of tokens.
    strategy: str, {"all", "majority"}
        The strategy to use for label creation.
    keep: str, {"body", "entity"}
        The strategy to use for label creation.
    """

    def __init__(self, tokenize_fn, strategy="majority", keep="body"):
        self.tokenize = tokenize_fn
        self.strategy = strategy
        self.keep = keep

    def get_majority(self, items: Iterable):
        """Return the majority label of a list of annotations.

        Parameters
        ----------
        items: Iterable[Iterable]
            A list of items.

        Returns
        -------
        majority: str
            The majority item.
        """
        if len(items) < 1:
            return None
        c = Counter(items)
        majority = c.most_common(1)
        return majority[0][0]

    def transform(self, task: Union[Task, Iterable[Document]]):
        # pylint: disable=too-many-locals
        """Tranforms a task into a sequence-to-sequence classification problem.

        Parameters
        ----------
        task: Task
            The task to transform.

        Returns
        -------
        input_sequence: List[List[str]]
            The content of the documents.
        output_sequence: List[[any]]
            The classification of the documents.
        """
        if self.strategy not in ('all', 'majority'):
            raise NotImplementedError(
                f'{self.strategy} is not a valid strategy.')
        documents = task
        if isinstance(task, Task):
            documents = task.documents
        input_sequences, output_sequences = [], []
        for doc in documents:
            in_seq, out_seq = [], []
            for idx, token in self.tokenize(doc.content):
                start, end = idx, idx + len(token) - 1
                labels = []
                for a in doc.annotations:
                    if hasattr(a, 'deleted') and a.deleted:
                        continue
                    contains_start = a.start <= start <= a.end - 1
                    contains_end = a.start <= end <= a.end - 1
                    if contains_start or contains_end:
                        if self.keep == "body":
                            labels.append(a.body)
                        elif self.keep == "entity":
                            labels.append(a.entity.name)
                idx += len(token)
                in_seq.append(token)
                if self.strategy == "majority":
                    labels = self.get_majority(labels)
                elif self.strategy == "all":
                    labels = tuple(set(labels))
                out_seq.append(labels)
            input_sequences.append(in_seq)
            output_sequences.append(out_seq)

        return input_sequences, output_sequences


__all__ = [
    'Transformer',
    'Filter',
    'Pipeline',
    'BinaryTransformer',
    'MultiClassTransformer',
    'MultiLabelTransformer',
    'Sequence2SequenceTransformer'
]
