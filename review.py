# -*- coding: utf-8 -*-
"""Python review task."""

import pyres

import flake
from settings import settings

q = pyres.ResQ(
    '{0}:{1}'.format(settings['host'], settings['port']),
    settings['password'],
)

class PythonReviewJob(object):

    queue = 'python_review'

    @staticmethod
    def perform(attributes):
        commit_sha = attributes["commit_sha"]
        config = attributes["config"]
        content = attributes["content"]
        filename = attributes["filename"]
        patch = attributes["patch"]
        pull_request_number = attributes["pull_request_number"]

        results = flake.check(config, content, filename)
        violations = [
            {'line': v.row, 'message': v.text}
            for v in results
        ]
        payload = {
            'class': 'CompletedFileReviewJob',
            'args': [{
                'filename': filename,
                'commit_sha': commit_sha,
                'pull_request_number': pull_request_number,
                'patch': patch,
                'violations': violations,
            }],
        }
        q.push('high', payload)
