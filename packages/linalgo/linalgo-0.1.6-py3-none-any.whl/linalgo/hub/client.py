# pylint: skip-file
import io
import os
from typing import List
import warnings
from enum import Enum

from contextlib import closing
import csv
import requests
import zipfile

from linalgo.annotate.models import (
    Annotation, Annotator, Corpus, Document, Entity, Task, Schedule
)
from linalgo.annotate import models, serializers
from linalgo.annotate.serializers import AnnotationSerializer, \
    EntitySerializer, DocumentSerializer, TaskSerializer
from linalgo.annotate.utils import SoftDeleteSet
from linalgo.config import get_config


class Error400(Exception):
    """400 error."""


class AssignmentType(Enum):
    REVIEW = 'R'
    LABEL = 'A'


class AssignmentStatus(Enum):
    ASSIGNED = 'A'
    COMPLETED = 'C'


class LinalgoClient:

    endpoints = {
        'annotators': 'annotators',
        'annotations': 'annotations',
        'corpora': 'corpora',
        'documents': 'documents',
        'entities': 'entities',
        'tasks': 'tasks',
        'annotations-export': 'annotations/export',
        'documents-export': 'documents/export',
        'organizations': 'organizations'
    }

    def __init__(
        self,
        token=None,
        api_url=None,
        organization=None,
        verbose=True
    ):
        url_default = 'http://localhost:8000/v1'
        
        # Check for configuration inconsistencies
        env_url = os.getenv('LINHUB_URL')
        config_url = get_config('hub.server_url')
        if env_url and config_url and env_url != config_url:
            warnings.warn("Warning: Environment variable LINHUB_URL "
                          f"({env_url}) differs from config file ({config_url})")
        
        env_token = os.getenv('LINHUB_TOKEN')
        config_token = get_config('hub.token')
        if env_token and config_token and env_token != config_token:
            warnings.warn("Warning: Environment variable LINHUB_TOKEN differs "
                          "from config file")
        
        env_org = os.getenv('LINHUB_ORG')
        config_org = get_config('hub.organization')
        if env_org and config_org and env_org != config_org:
            warnings.warn("Warning: Environment variable LINHUB_ORG "
                          f"({env_org}) differs from config file ({config_org})")
        
        # Set client properties with precedence: explicit args > env vars > config file > defaults
        self.api_url = api_url or os.getenv('LINHUB_URL') or get_config('hub.server_url', url_default)
        self.access_token = token or os.getenv('LINHUB_TOKEN') or get_config('hub.token')
        self.organization = organization or os.getenv('LINHUB_ORG') or get_config('hub.organization')
        self.verbose = verbose

    def get(self, url, query_params={}):
        headers = {'Authorization': f"Token {self.access_token}"}
        res = requests.get(url, headers=headers, params=query_params)
        if res.status_code == 401:
            raise Exception(f"Authentication failed. Please check your token.")
        if res.status_code == 404:
            raise Exception(f"{url} not found.")
        elif res.status_code != 200:
            raise Exception(
                f"Request returned status {res.status_code}, {res.content}")
        return res.json()

    def post(self, url, data=None, files=None, json=None):
        headers = {'Authorization': f"Token {self.access_token}"}
        res = requests.post(url, data=data, json=json,
                            files=files, headers=headers)
        if 200 <= res.status_code < 300:
            return res
        if res.status_code == 401:
            raise Exception(f"Authentication failed. Please check your token.")
        elif res.status_code == 404:
            raise Exception(f"{url} not found.")
        elif 400 <= res.status_code < 500:
            print(res, res._content)
            raise Error400(res.json())
        else:
            raise Exception(
                f"Request returned status {res.status_code}, {res.content}")

    def request_csv(self, url, query_params={}):
        headers = {'Authorization': f"Token {self.access_token}"}
        with closing(requests.get(url, stream=True,
                                  headers=headers, params=query_params)) as res:
            if res.status_code == 401:
                raise Exception(
                    f"Authentication failed. Please check your token.")
            if res.status_code == 404:
                raise Exception(f"{url} not found.")
            elif res.status_code != 200:
                raise Exception(f"Request returned status {res.status_code}")
            root = zipfile.ZipFile(io.BytesIO(res.content))
            f = root.namelist()
            if len(f):
                d = csv.DictReader(io.TextIOWrapper(root.open(f[0]), 'utf-8'))
            else:
                d = []
            return d

    def get_current_annotator(self):
        """Returns the current annotator."""
        url = f"{self.api_url}/{self.endpoints['annotators']}/me/"
        return Annotator(**self.get(url))

    def create_corpus(self, corpus: Corpus):
        """Creates a new corpus.

        Parameters
        ----------
        corpus: Corpus

        Returns
        -------
        Corpus
        """
        if self.verbose:
            print(f"Creating {corpus}...", end=' ')
        try:
            url = f"{self.api_url}/{self.endpoints['corpora']}/"
            serializer = serializers.CorpusSerializer(corpus)
            data = serializer.serialize()
            data['organization'] = self.organization
            res = self.post(url, data=data)
            if self.verbose:
                print("OK.")
            return models.Corpus(**res.json())
        except Error400 as e:
            if self.verbose:
                print(f"failed. ({e})")
            return e

    def add_documents(self, documents: List[models.Document]):
        """Add the documents provided"""
        if self.verbose:
            print(f"Adding {len(documents)} documents...", end=' ')
        try:
            url = f"{self.api_url}/{self.endpoints['documents']}/import_documents/"
            serializer = serializers.DocumentSerializer(documents)
            f = io.StringIO()
            keys = ['id', 'uri', 'content', 'corpus_id']
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
            writer.writerows(serializer.serialize())
            csv_content = f.getvalue()
            files = {'fileKey': (
                'data.csv', csv_content.encode('utf-8'), 'text/csv')}
            res = self.post(url, files=files)
            if self.verbose:
                print("OK.")
        except Error400 as e:
            if self.verbose:
                print(f"failed. ({e})")
            return e

    def get_next_document(self, task_id: str):
        url = f"{self.api_url}/tasks/{task_id}/next_document/"
        return Document(**self.get(url))

    def get_corpora(self):
        res = self.get(self.endpoints['corpora'])
        corpora = []
        for js in res['results']:
            corpus_id = js['id']
            corpus = self.get_corpus(corpus_id)
            corpora.append(corpus)
        return corpora

    def get_organizations(self):
        url = f"{self.api_url}/{self.endpoints['organizations']}/"
        orgs = []
        for data in self.get(url)['results']:
            org = models.Organization(**data)
            orgs.append(org)
        return self.get(url)['results']

    def get_organization(self, org_id: str):
        url = f"{self.api_url}/{self.endpoints['organizations']}/{org_id}/"
        data = self.get(url)
        return models.Organization(**data)

    def get_corpus(self, corpus_id):
        url = f"{self.api_url}/{self.endpoints['corpora']}/{corpus_id}/"
        res = self.get(url)
        corpus = Corpus.from_dict(res)
        # corpus = Corpus(name=res['name'], description=res['description'])
        documents = self.get_corpus_documents(corpus_id)
        corpus.documents = documents
        return corpus

    def get_corpus_documents(self, corpus_id):
        url = f"{self.api_url}/documents/?page_size=1000&corpus={corpus_id}"
        res = self.get(url)
        documents = []
        for d in res['results']:
            document = Document.from_dict(d)
            documents.append(document)
        return documents

    def create_entities(self, entities):
        if self.verbose:
            print(f"Creating {len(entities)} entities...", end=' ')
        try:
            url = f"{self.api_url}/{self.endpoints['entities']}/"
            data = EntitySerializer(entities).serialize()
            res = self.post(url, json=data)
            if self.verbose:
                print("OK.")
            return res
        except Error400 as e:
            if self.verbose:
                print(f"failed. ({e})")
            return e

    def create_task(self, task: models.Task):
        url = f"{self.api_url}/{self.endpoints['tasks']}/"
        data = TaskSerializer(task).serialize()
        for corpus in task.corpora:
            self.create_corpus(corpus)
        documents = set()
        for corpus in task.corpora:
            for doc in corpus.documents:
                documents.add(doc)
        self.add_documents(documents)
        self.create_entities(task.entities)
        data['organization'] = self.organization
        data['corpora'] = [c.id for c in task.corpora]
        data['entities'] = [e.id for e in task.entities]
        try:
            if self.verbose:
                print(f"Creating {task}...", end=' ')
                print(data)
            res = self.post(url, json=data)
            if self.verbose:
                print("OK.")
                print(res.status_code)
            return Task(**res.json())
        except Error400 as e:
            if self.verbose:
                print(f"failed. ({e})")
            return e

    def get_tasks(self, task_ids=[]):
        url = f"{self.api_url}/{self.endpoints['tasks']}/"
        tasks = []
        res = self.get(url)
        if len(task_ids) == 0:
            for js in res['results']:
                task_ids.append(js['id'])
        for task_id in task_ids:
            task = self.get_task(task_id)
            tasks.append(task)
        return tasks

    def get_task_documents(self, task_id):
        query_params = {
            'task_id': task_id,
            'output_format': 'zip',
            'only_documents': True
        }
        api_url = "{}/{}/".format(
            self.api_url, self.endpoints['documents-export'])
        records = self.request_csv(api_url, query_params)
        data = SoftDeleteSet(Document.from_dict(row) for row in records)
        return data

    def get_task_annotations(self, task_id):
        query_params = {'task_id': task_id, 'output_format': 'zip'}
        api_url = f"{self.api_url}/{self.endpoints['annotations-export']}/"
        records = self.request_csv(api_url, query_params)
        data = SoftDeleteSet(Annotation.from_dict(row) for row in records)
        return data

    def get_task(self, task_id, verbose=False, lazy=False):
        task_url = "{}/{}/{}/".format(
            self.api_url, self.endpoints['tasks'], task_id)
        if verbose:
            print(f'Retrivieving task with id {task_id}...')
        task_json = self.get(task_url)
        task = Task.from_dict(task_json)
        if lazy:
            return task
        if verbose:
            print('Retrieving annotators...', end=' ')
        task.annotators = self.get_annotators(task)
        if verbose:
            print(f'({len(task.annotators)} found)')
        if verbose:
            print('Retrieving entities...', end=' ')
        params = {'tasks': task.id, 'page_size': 1000}
        if verbose:
            print(f'({len(task.entities)} found)')
        entities_url = "{}/{}".format(self.api_url, self.endpoints['entities'])
        entities_json = self.get(entities_url, params)
        task.entities = [Entity.from_dict(e) for e in entities_json['results']]
        if verbose:
            print('Retrieving documents...', end=' ')
        task.documents = self.get_task_documents(task_id)
        if verbose:
            print(f'({len(task.documents)} found)')
        if verbose:
            print('Retrieving annotations...', end=' ')
        task.annotations = self.get_task_annotations(task_id)
        if verbose:
            print(f'({len(task.annotations)} found)')
        n = len([a for d in task.documents for a in d.annotations])
        if len(task.annotations) != n:
            warnings.warn('Some annotations have no associated document.')
        return task

    def get_annotators(self, task):
        if isinstance(task, str):
            task = Task(unique_id=task)
        params = {'tasks': task.id, 'page_size': 1000}
        annotators_url = "{}/{}/".format(
            self.api_url, self.endpoints['annotators'])
        res = self.get(annotators_url, params)
        annotators = []
        for a in res['results']:
            annotator = Annotator.from_dict(a)
            annotators.append(annotator)
        return annotators

    def create_annotator(self, annotator):
        url = "{}/{}/".format(self.api_url, self.endpoints['annotators'])
        annotator_json = {
            'id': annotator.id,
            'name': annotator.name,
            'model': str(annotator.model),
            'owner': annotator.owner
        }
        res = self.post(url, json=annotator_json)
        if res.status_code != 201:
            raise Exception(res.content)
        res = res.json()
        annotator.annotator_id = res['id']
        annotator.owner = res['owner']
        return annotator

    def add_annotators_to_task(self, annotators, task):
        endpoint = self.endpoints['tasks']
        url = f"{self.api_url}/{endpoint}/{task.id}/add_annotators/"
        payload = [annotator.id for annotator in annotators]
        return self.post(url, json=payload)

    def create_annotations(self, annotations, task=None):
        url = f"{self.api_url}/{self.endpoints['annotations']}/"
        if task is not None:
            for annotation in annotations:
                annotation.task = task
        serializer = AnnotationSerializer(annotations)
        payload = serializer.serialize()
        res = self.post(url, json=payload)
        return res

    def delete_annotations(self, annotations):
        url = f"{self.api_url}/{self.endpoints['annotations']}/bulk_delete/"
        headers = {'Authorization': f"Token {self.access_token}"}
        annotations_ids = [annotation.id for annotation in annotations]
        res = requests.delete(url, json=annotations_ids, headers=headers)
        if res.status_code != 204:
            raise Exception(res.content)
        return res

    def assign(
        self,
        document: Document,
        annotator: Annotator,
        task: Task,
        reviewee=None,
        assignment_type=AssignmentType.LABEL.value
    ):
        doc_status = {
            'status': AssignmentStatus.ASSIGNED.value,
            'type': assignment_type,
            'document': document.id,
            'annotator': annotator.id,
            'task': task.id,
            'reviewee': reviewee
        }
        url = self.api_url + '/document-status/'
        res = self.post(url, data=doc_status)
        return res

    def unassign(self, status_id):
        headers = {'Authorization': f"Token {self.access_token}"}
        url = f"{self.api_url}/document-status/{status_id}/"
        res = requests.delete(url, headers=headers)
        return res

    def get_schedule(self, task):
        query_params = {'task': task.id, 'page_size': 1000}
        schedules = []
        next_url = f"{self.api_url}/document-status/"
        while next_url:
            res = self.get(next_url, query_params=query_params)
            next_url = res['next']
            schedules.extend(Schedule(**s) for s in res['results'])
        return schedules

    def add_corpora(self, corpora: List[Corpus], task: Task):
        url = f"{self.api_url}/tasks/{task.id}/add_corpora/"
        payload = [{'id': corpus.id} for corpus in corpora]
        return self.post(url, json=payload)

    def add_document(self, doc: Document, corpus: Corpus):
        url = f"{self.api_url}/corpora/{corpus.id}/add_document/"
        payload = DocumentSerializer(doc).serialize()
        return self.post(url, data=payload)

    def complete_document(self, doc, task):
        endpoint = self.endpoints['tasks']
        url = f"{self.api_url}/{endpoint}/{task.id}/complete_document/"
        return self.post(url, data={'document': doc.id})


__all__ = ['LinalgoClient']
